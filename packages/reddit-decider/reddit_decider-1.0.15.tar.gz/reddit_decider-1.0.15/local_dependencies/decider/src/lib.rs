extern crate crypto;
use self::crypto::digest::Digest;
use self::crypto::sha1::Sha1;
use num_bigint::BigUint;
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::HashMap;
use std::fmt;
use std::fs::File;
use std::io::BufReader;
// Decider is a library for determining whether a given feature should be available
// in a given context.  It supports a very expressive set of operations for determining
// which features should be available (and in what variant, if more than one is desired)
// in a context.

// A context captures the relevant state in which we want to find out whether a feature
// should be available.
#[derive(Serialize, Deserialize, Debug)]
pub struct Context {
    pub user_id: String,
    /* IETF language tag representing the preferred locale for
     * the client, used for providing localized content. Consists of
     * an ISO 639-1 primary language subtag and an optional
     * ISO 3166-1 alpha-2 region subtag separated by an underscore.
     * e.g. en, en_US
     */
    pub locale: Option<String>,
    pub country_code: Option<String>, // A two-character ISO 3166-1 country code
    pub device_id: Option<String>,
    pub origin_service: Option<String>,
    pub user_is_employee: Option<bool>,
    pub logged_in: Option<bool>,
    pub app_name: Option<String>,
    pub build_number: Option<i32>,
    pub authentication_token: Option<String>, // FIXME: this is almost surely a security concern.  We should remove it.
    pub request_url: Option<String>,
    pub cookie_created_timestamp: Option<f64>,
}

impl Context {
    fn get_field(&self, field: &str) -> Option<Value> {
        match field {
            "user_id" => Some(self.user_id.to_string()),
            "device_id" => self.device_id.clone(),
            "locale" => self.locale.clone(),
            "country_code" => self.country_code.clone(),
            "origin_service" => self.origin_service.clone(),
            "app_name" => self.app_name.clone(),
            "request_url" => self.request_url.clone(),
            _ => None,
        }
        .map(Value::from)
    }

    fn get_bucketing_field(&self, bucket_val: &BucketVal) -> Result<String, DeciderFailType> {
        match bucket_val {
            BucketVal::UserId => Ok(self.user_id.clone()),
            BucketVal::DeviceId => match &self.device_id {
                Some(d_id) => Ok(d_id.to_string()),
                None => Err(DeciderFailType::MissingBucketVal("device_id".to_string())),
            }, // todo: BucketVal::CanonicalUrl
        }
    }

    fn cmp(&self, field: &str, value: &Value) -> bool {
        // FIXME: make this return Result to signal missing fields
        match self.get_field(field) {
            None => false,
            Some(v) => value_eq(v, value.clone()).unwrap(),
        }
    }

    fn cmp_op(&self, comp: Comp, field: &str, value: i64) -> Result<bool, String> {
        // GT/LT and friends only really make sense on Numbers
        match self.get_field(field) {
            None => Err("missing field".to_string()), // TODO: add which field was missing
            Some(v) => match v {
                Value::Number(n) => match n.as_i64() {
                    None => Err("failed to get int".to_string()),
                    Some(int) => match comp {
                        Comp::GT => Ok(int > value),
                        Comp::LT => Ok(int < value),
                        Comp::GE => Ok(int >= value),
                        Comp::LE => Ok(int <= value),
                    },
                },
                Value::String(s) => match s.parse::<i64>() {
                    Err(_) => Err("failed to parse string to int".to_string()),
                    Ok(int) => match comp {
                        Comp::GT => Ok(int > value),
                        Comp::LT => Ok(int < value),
                        Comp::GE => Ok(int >= value),
                        Comp::LE => Ok(int <= value),
                    },
                },
                _ => Err("type_mismatch".to_string()),
            },
        }
    }
}

fn value_eq(x: Value, y: Value) -> Result<bool, String> {
    // will take in 2 Value objects, possibly of different Value::variants,
    // and do an equality test on them.  does string-> number conversion.
    match (&x, &y) {
        (Value::Null, _) => Ok(y.is_null()),
        (Value::Bool(b1), Value::Bool(b2)) => Ok(b1 == b2),
        (Value::String(s1), Value::String(s2)) => Ok(s1 == s2),
        (Value::String(s1), Value::Number(n2)) => Ok(s1 == &n2.to_string()),
        (Value::Number(n1), Value::Number(n2)) => Ok(n1 == n2),
        (Value::Number(n1), Value::String(s2)) => Ok(s2 == &n1.to_string()),
        _ => Err(format!("cannot compare '{:#?}' vs. '{:#?}'", x, y)),
    }
}

// Features represent a unit of controllable code, that we might want to turn off, make
// available only to some users, etc..  This is what FeatureFlags/AB tests control.
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Feature {
    id: u32,
    name: String,
    enabled: bool,
    version: u32,
    platform_bitmask: u64, //TODO: should this be made a vec for unbounded size?
    value: Option<Value>,
    targeting: Option<TargetingTree>,
    overrides: Option<HashMap<String, TargetingTree>>,
    variant_set: Option<VariantSet>,
}

// VariantSet contains an experiment's variants, and all other fields not in common with
// dynamic config json.
#[derive(Serialize, Deserialize, Debug, Clone)]
struct VariantSet {
    start_ts: u64, // TODO: consider whether this should just be created_at
    stop_ts: u64,  // TODO: should we get rid of a version by creating a new one?
    shuffle_version: u32,
    bucket_val: BucketVal,
    variants: Vec<Variant>,
    holdout: Option<FeatureGroup>,
    mutex_group: Option<FeatureGroup>,
}

// FeatureGroups are used for holdouts, mutex groups, etc.
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct FeatureGroup {
    id: u32,
    name: String,
    enabled: bool,
    start_ts: u64, // TODO: consider whether this should just be created_at
    stop_ts: u64,  // TODO: should we get rid of a version by creating a new one?
    version: u32,
    shuffle_version: u32,
    variants: Vec<Variant>,
    platform_bitmask: u64, //TODO: should this be made a vec for unbounded size?
    targeting: Option<TargetingTree>,
    overrides: Option<HashMap<String, TargetingTree>>,
}

// Variants are primarily used for fractional availability, where, eg., 10% of users
// are exposed to a given version of a feature.
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Variant {
    name: String,
    #[serde(rename = "range_start")] // TODO change to alias and remove
    lo: f32, // consider changing away from floats.
    #[serde(rename = "range_end")]
    hi: f32,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct EqStruct {
    field: String,
    value: Option<Value>,
    values: Option<Vec<Value>>,
}

impl EqStruct {
    fn eval(&self, ctx: &Context) -> bool {
        // FIXME: this makes values trump value, which is gross.
        return match &self.values {
            Some(vl) => vl.iter().any(|x| ctx.cmp(&self.field, x)),
            None => match &self.value {
                None => true, // if there is no values and no value, it's malformed.
                Some(v) => ctx.cmp(&self.field, v),
            },
        };
    }
}

// The TargetingTree allows for arbitrary targeting operations, which can be used to
// limit an experiment to employees, or users from new zealand, only to iOS users, or
// to users in New Zealand, etc..
#[derive(Serialize, Deserialize, Debug, Clone)]
pub enum TargetingTree {
    ALL(Vec<TargetingTree>),
    ANY(Vec<TargetingTree>),
    NOT(Box<TargetingTree>),
    //#[serde(flatten)]
    EQ(EqStruct),
    GT { field: String, value: i64 },
    LT { field: String, value: i64 },
    GE { field: String, value: i64 },
    LE { field: String, value: i64 },
    NE { field: String, value: Value },
}

enum Comp {
    GT,
    LT,
    GE,
    LE,
}

impl TargetingTree {
    fn eval(&self, ctx: &Context) -> bool {
        match self {
            TargetingTree::ALL(xs) => xs.iter().all(|x| x.eval(ctx)),
            TargetingTree::ANY(xs) => xs.iter().any(|x| x.eval(ctx)),
            TargetingTree::NOT(x) => !x.eval(ctx),
            TargetingTree::EQ(es) => es.eval(ctx),
            TargetingTree::GT { field, value } => ctx.cmp_op(Comp::GT, field, *value).unwrap(),
            TargetingTree::LT { field, value } => ctx.cmp_op(Comp::LT, field, *value).unwrap(),
            TargetingTree::GE { field, value } => ctx.cmp_op(Comp::GE, field, *value).unwrap(),
            TargetingTree::LE { field, value } => ctx.cmp_op(Comp::LE, field, *value).unwrap(),
            TargetingTree::NE { field, value } => !ctx.cmp(field, value),
        }
    }
}

/*
Decider determines feature availability by chaining together simple
decisionmaker functions to enable complicated logic to be expressed as a
composition of simple, testable functions. Those compositions are tested
against features, an abstsraction for bits of code that enabling feature
flagging, AB testing, etc..
*/
pub struct Decider {
    features: Vec<Feature>,
    decisionmakers: Vec<Decisionmaker>,
}

impl fmt::Debug for Decider {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Decider: {:#?}", self.features)
    }
}

impl Decider {
    pub fn choose(
        &self,
        feature_name: String,
        ctx: &Context,
    ) -> Result<Option<Decision>, DeciderFailType> {
        let f = self.feature_by_name(feature_name)?;
        self.decide(&f, ctx)
    }

    pub fn get_bool(&self, feature_name: String, ctx: &Context) -> Result<bool, DeciderFailType> {
        let f = self.feature_by_name(feature_name)?;
        let res = self.decide(&f, ctx);
        match self.validate_dc_value(res) {
            Ok(value) => match value {
                Value::Bool(b) => Ok(b),
                _ => Err(DeciderFailType::DcTypeMismatch),
            },
            Err(e) => Err(e),
        }
    }

    pub fn get_int(&self, feature_name: String, ctx: &Context) -> Result<i64, DeciderFailType> {
        let f = self.feature_by_name(feature_name)?;
        let res = self.decide(&f, ctx);
        match self.validate_dc_value(res) {
            Ok(value) => match value {
                Value::Number(b) => match b.as_i64() {
                    Some(int) => Ok(int),
                    _ => Err(DeciderFailType::NumberDeserializationError),
                },
                _ => Err(DeciderFailType::DcTypeMismatch),
            },
            Err(e) => Err(e),
        }
    }

    pub fn get_float(&self, feature_name: String, ctx: &Context) -> Result<f64, DeciderFailType> {
        let f = self.feature_by_name(feature_name)?;
        let res = self.decide(&f, ctx);
        match self.validate_dc_value(res) {
            Ok(value) => match value {
                Value::Number(b) => match b.as_f64() {
                    Some(float) => Ok(float),
                    _ => Err(DeciderFailType::NumberDeserializationError),
                },
                _ => Err(DeciderFailType::DcTypeMismatch),
            },
            Err(e) => Err(e),
        }
    }

    pub fn get_string(
        &self,
        feature_name: String,
        ctx: &Context,
    ) -> Result<String, DeciderFailType> {
        let f = self.feature_by_name(feature_name)?;
        let res = self.decide(&f, ctx);
        match self.validate_dc_value(res) {
            Ok(value) => match value {
                Value::String(s) => Ok(s),
                _ => Err(DeciderFailType::DcTypeMismatch),
            },
            Err(e) => Err(e),
        }
    }

    pub fn get_map(
        &self,
        feature_name: String,
        ctx: &Context,
    ) -> Result<serde_json::Map<String, Value>, DeciderFailType> {
        let f = self.feature_by_name(feature_name)?;
        let res = self.decide(&f, ctx);
        match self.validate_dc_value(res) {
            Ok(value) => match value {
                Value::Object(obj) => Ok(obj),
                _ => Err(DeciderFailType::DcTypeMismatch),
            },
            Err(e) => Err(e),
        }
    }

    fn validate_dc_value(
        &self,
        res: Result<Option<Decision>, DeciderFailType>,
    ) -> Result<Value, DeciderFailType> {
        match res {
            Ok(decision) => match decision {
                Some(Decision {
                    name: _,
                    value,
                    emit_event: _,
                    bucket: _,
                }) => Ok(value),
                _ => Err(DeciderFailType::InvalidFeature),
            },
            Err(e) => Err(e),
        }
    }

    pub fn feature_by_name(&self, feature_name: String) -> Result<Feature, DeciderFailType> {
        match self.features.iter().find(|f| f.name == feature_name) {
            None => Err(DeciderFailType::FeatureNotFoundWithName(feature_name)),
            Some(feature) => Ok(feature.clone()),
        }
    }

    fn decide(&self, f: &Feature, ctx: &Context) -> Result<Option<Decision>, DeciderFailType> {
        // TODO: decide whether decide should return a Result<Option<Decision>>, to
        // account for ill-defined Features or missing data on the Context. Probably
        // yes, but currently Decision also has an option on name/bucketing.  Maybe
        // decide should return a Result<Decision>?
        for fun in &self.decisionmakers {
            let res = fun(f, ctx)?; // Should I let errors bubble up?  probably not.
            match res {
                DecisionmakerResult::None => return Ok(None),
                DecisionmakerResult::Pass(_s) => (),
                DecisionmakerResult::Decided(d) => {
                    return Ok(Some(d));
                }
            }
        }
        Ok(None) // default open (just return nothing)
    }
}

impl VariantSet {
    fn bucketing_string(&self, id: &u32, name: &str, identifier: &str) -> String {
        format!("{}.{}.{}{}", id, name, self.shuffle_version, identifier)
    }
}

fn darkmode(f: &Feature, _ctx: &Context) -> Result<DecisionmakerResult, DeciderFailType> {
    if f.enabled {
        Ok(DecisionmakerResult::Pass("darkmode:enabled".to_string()))
    } else {
        Ok(DecisionmakerResult::None)
    }
}

fn locale(f: &Feature, _ctx: &Context) -> Result<DecisionmakerResult, DeciderFailType> {
    if !f.enabled {
        // TODO: add locales to Feature, compare ctx.locale to that
        Ok(DecisionmakerResult::Pass("locale:fixme".to_string()))
    } else {
        Ok(DecisionmakerResult::Pass("locale:fixme2".to_string()))
    }
}

fn fractional_availability(
    f: &Feature,
    ctx: &Context,
) -> Result<DecisionmakerResult, DeciderFailType> {
    match &f.variant_set {
        None => Ok(DecisionmakerResult::Pass(
            "frac_avail:no variant_set".to_string(),
        )),
        Some(vs) => match ctx.get_bucketing_field(&vs.bucket_val) {
            Ok(id) => {
                let bs = vs.bucketing_string(&f.id, &f.name, &id);
                bucket_or_pass(vs, &bs)
            }
            Err(e) => Err(e),
        },
    }
}

fn bucket_or_pass(
    vs: &VariantSet,
    bucketing_string: &str,
) -> Result<DecisionmakerResult, DeciderFailType> {
    let i = bucket(bucketing_string.to_string());
    let flt = (i as f32) / 1000.0;
    let v = vs.variants.iter().find(|x| x.lo <= flt && x.hi > flt);
    match v {
        None => Ok(DecisionmakerResult::Pass(
            "frac_avail:not in variants".to_string(),
        )),
        Some(variant) => Ok(DecisionmakerResult::Decided(Decision {
            name: variant.name.clone(),
            bucket: Some(i),
            emit_event: false,
            value: Value::Null,
        })),
    }
}

fn overrides(f: &Feature, ctx: &Context) -> Result<DecisionmakerResult, DeciderFailType> {
    match &f.overrides {
        None => Ok(DecisionmakerResult::Pass(
            "overrides:none_found".to_string(),
        )),
        Some(hm) => {
            for (name, tt) in hm.iter() {
                if tt.eval(ctx) {
                    return Ok(DecisionmakerResult::Decided(Decision {
                        // FIXME: check to make sure this is a variant name
                        name: name.clone(),
                        emit_event: false,
                        bucket: None,
                        value: Value::String(name.clone()),
                    }));
                }
            }
            Ok(DecisionmakerResult::Pass(
                "overrides:none_found".to_string(),
            ))
        }
    }
}

fn targeting(f: &Feature, ctx: &Context) -> Result<DecisionmakerResult, DeciderFailType> {
    match &f.targeting {
        None => Ok(DecisionmakerResult::Pass(
            "targeting:none_found".to_string(),
        )),
        Some(tt) => {
            let b = tt.eval(ctx);
            match b {
                true => Ok(DecisionmakerResult::Pass("targeting:targeted".to_string())),
                false => Ok(DecisionmakerResult::None),
            }
        }
    }
}

fn value(f: &Feature, _ctx: &Context) -> Result<DecisionmakerResult, DeciderFailType> {
    match &f.value {
        None => Ok(DecisionmakerResult::None),
        Some(value) => match value {
            Value::Null | Value::Array(_) => {
                Ok(DecisionmakerResult::Pass("value:null_or_array".to_string()))
            }
            _ => Ok(DecisionmakerResult::Decided(Decision {
                name: f.name.clone(),
                emit_event: false,
                bucket: None,
                value: value.clone(),
            })),
        },
    }
}

#[derive(Serialize, Deserialize, Debug)]
pub enum DecisionmakerResult {
    // TODO: find a better nome
    Pass(String),      // I didn't make a decision because...
    None,              // response is nothing
    Decided(Decision), // actual decision.
}

#[derive(Debug)]
pub enum DeciderFailType {
    FeatureNotFound,
    FeatureNotFoundWithName(String),
    InvalidFeature,
    MissingBucketVal(String),
    DcTypeMismatch,
    NumberDeserializationError,
    MapDeserializationError(String),
    InvalidDecisionMaker(String),
    IoError(std::io::Error),
    SerdeError(serde_json::Error),
}

impl fmt::Display for DeciderFailType {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match &*self {
            DeciderFailType::FeatureNotFound => write!(f, "Feature not found."),
            DeciderFailType::FeatureNotFoundWithName(name) => {
                write!(f, "Feature {:#?} not found.", name.to_string())
            }
            DeciderFailType::InvalidFeature => write!(f, "Invalid Feature configuration."),
            DeciderFailType::MissingBucketVal(bucket_val) => write!(
                f,
                "Missing {:#?} in context for bucket_val = {:#?}",
                bucket_val, bucket_val
            ),
            DeciderFailType::DcTypeMismatch => {
                write!(f, "Dynamic Configuartion Feature type mismatch.")
            }
            DeciderFailType::NumberDeserializationError => {
                write!(f, "Number deserialization failed.")
            }
            DeciderFailType::MapDeserializationError(err_str) => {
                write!(f, "Map deserialization failed: {:#?}", err_str.clone())
            }
            DeciderFailType::InvalidDecisionMaker(err_str) => {
                write!(f, "Invalid DecisionMaker: {:#?}", err_str.clone())
            }
            DeciderFailType::SerdeError(serde_json_error) => {
                write!(f, "Json error: {:#?}", serde_json_error.to_string())
            }
            DeciderFailType::IoError(std_io_error) => {
                write!(f, "Std io error: {:#?}", std_io_error.to_string())
            }
        }
    }
}

impl From<std::io::Error> for DeciderFailType {
    fn from(e: std::io::Error) -> DeciderFailType {
        DeciderFailType::IoError(e)
    }
}

impl From<serde_json::Error> for DeciderFailType {
    fn from(e: serde_json::Error) -> DeciderFailType {
        DeciderFailType::SerdeError(e)
    }
}

#[derive(PartialEq, Eq, Serialize, Deserialize, Debug)]
pub struct Decision {
    pub name: String,
    pub emit_event: bool,
    pub value: Value,
    bucket: Option<i32>,
}

fn bucket(bucketing_str: String) -> i32 {
    // FIXME: take in number of buckets as a param.
    let mut hasher = Sha1::new();
    hasher.input_str(&bucketing_str);
    let bigint = BigUint::parse_bytes(hasher.result_str().as_bytes(), 16);
    let res = match bigint {
        Some(v) => v % 1000u32,
        None => BigUint::from(9999u32), // FIXME: don'T use sentinel out-of-range values to indicate error.
    };
    let n_as_i32: i32 = res.try_into().unwrap(); // FIXME: get rid of the unwrap
    n_as_i32
}

type Decisionmaker = fn(f: &Feature, ctx: &Context) -> Result<DecisionmakerResult, DeciderFailType>;

fn name_to_decisionmaker(name: &str) -> Result<Decisionmaker, String> {
    return match name {
        "darkmode" => Ok(darkmode),
        "locale" => Ok(locale),
        "fractional_availability" => Ok(fractional_availability),
        "targeting" => Ok(targeting),
        "overrides" => Ok(overrides),
        "value" => Ok(value),
        _ => Err(format!("Invalid decisionmaker name: {:?}", name)),
    };
}

fn string_to_decisionmakers(cfg: String) -> Result<Vec<Decisionmaker>, String> {
    // we get a result of a vec because we want any single error in
    // decisionmaker names to fail the whole thing (no silent errors
    // causing unexpected behavior).  Got the technique from:
    // https://stackoverflow.com/questions/26368288/how-do-i-stop-iteration-and-return-an-error-when-iteratormap-returns-a-result
    let dml: Result<Vec<Decisionmaker>, String> = cfg
        .split_whitespace()
        .map(name_to_decisionmaker)
        .take(5)
        .collect();
    dml
}

pub fn init(cfg: String, features: Vec<Feature>) -> Result<Decider, DeciderFailType> {
    match string_to_decisionmakers(cfg) {
        Ok(decisionmakers) => Ok(Decider {
            features,
            decisionmakers,
        }),
        Err(s) => Err(DeciderFailType::InvalidDecisionMaker(s)),
    }
}

// This section is legacy code to deal with reddit's existing experiment format.
pub fn init_decider(cfg: String, filepath: String) -> Result<Decider, DeciderFailType> {
    let file = File::open(filepath)?;
    let reader = BufReader::new(file);
    let ec: ExperimentConfig = serde_json::from_reader(reader)?;
    let fl = experiment_config_to_features(ec)?;
    init(cfg, fl)
}

fn experiment_config_to_features(ec: ExperimentConfig) -> Result<Vec<Feature>, DeciderFailType> {
    let ec2 = ec.clone();
    let fl: Vec<Feature> = ec
        .into_values()
        .map(|exp| experiment_to_feature(&exp, &ec2))
        .collect();
    Ok(fl)
}

type ExperimentConfig = HashMap<String, Experiment>;

#[derive(Serialize, Deserialize, Debug, Clone)]
struct Experiment {
    id: u32,
    name: String,
    enabled: bool,
    version: String,
    #[serde(rename = "type")]
    experiment_type: ExperimentType,
    #[serde(default)]
    start_ts: u64,
    #[serde(default)]
    stop_ts: u64,
    value: Option<Value>, // used by dynamic_config
    parent_meg_name: Option<String>,
    parent_hg_name: Option<String>,
    experiment: InnerExperiment,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
#[serde(rename_all(deserialize = "snake_case"))]
enum ExperimentType {
    DynamicConfig,
    RangeVariant,
    FeatureRollout, // FIXME: get rid of this after the great RangeVariant takeover.
}

#[derive(Serialize, Deserialize, Debug, Clone)]
#[serde(rename_all(deserialize = "snake_case"))]
enum BucketVal {
    #[serde(rename = "user_id")]
    UserId,
    #[serde(rename = "device_id")]
    DeviceId,
    // todo: CanonicalUrl
}

impl Default for BucketVal {
    fn default() -> Self {
        BucketVal::UserId
    }
}

#[derive(Serialize, Deserialize, Debug, Clone)]
struct InnerExperiment {
    // FIXME: better name, plzkkthxbai?
    experiment_version: u32,
    #[serde(default)]
    variants: Vec<Variant>, // TODO: figure out how to make a variable-length array in a struct, maybe?
    #[serde(default)]
    shuffle_version: u32,
    #[serde(default)]
    bucket_val: BucketVal,
    overrides: Option<HashMap<String, TargetingTree>>,
    targeting: Option<TargetingTree>,
}

fn experiment_to_feature(exp: &Experiment, ec: &ExperimentConfig) -> Feature {
    let holdout = match &exp.parent_hg_name {
        None => None,
        Some(name) => ec.get(name).map(experiment_to_feature_group),
    };

    let mutex_group = match &exp.parent_meg_name {
        None => None,
        Some(name) => ec.get(name).map(experiment_to_feature_group),
    };

    let variant_set = match exp.experiment_type {
        ExperimentType::DynamicConfig => None,
        _ => Some(VariantSet {
            start_ts: exp.start_ts,
            stop_ts: exp.stop_ts,
            shuffle_version: exp.experiment.shuffle_version,
            variants: exp.experiment.variants.clone(),
            bucket_val: exp.experiment.bucket_val.clone(),
            holdout,
            mutex_group,
        }),
    };

    Feature {
        // FIXME: surely there must be a better way
        id: exp.id,
        name: exp.name.clone(),
        enabled: exp.enabled,
        version: exp.experiment.experiment_version,
        platform_bitmask: 0,
        value: exp.value.clone(),
        targeting: exp.experiment.targeting.clone(),
        overrides: exp.experiment.overrides.clone(),
        variant_set,
    }
}

fn experiment_to_feature_group(exp: &Experiment) -> FeatureGroup {
    FeatureGroup {
        // FIXME: surely there must be a better way
        id: exp.id,
        name: exp.name.clone(),
        enabled: exp.enabled,
        start_ts: exp.start_ts,
        stop_ts: exp.stop_ts,
        version: exp.experiment.experiment_version,
        shuffle_version: exp.experiment.shuffle_version,
        variants: exp.experiment.variants.clone(),
        targeting: exp.experiment.targeting.clone(),
        overrides: exp.experiment.overrides.clone(),
        platform_bitmask: 0,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use proptest::prelude::*;
    use serde_json::json;
    use serde_json::Error;

    enum Dc {
        Bool(Option<serde_json::Value>),
        Int(Option<serde_json::Value>),
        Float(Option<serde_json::Value>),
        String(Option<serde_json::Value>),
        Map(Option<String>),
    }

    fn make_feature() -> Feature {
        let v = Variant {
            name: "enabled".to_string(),
            lo: 0.0,
            hi: 0.1,
        };
        Feature {
            id: 1,
            name: "first_feature".to_string(),
            enabled: true,
            version: 1,
            platform_bitmask: 0,
            targeting: None,
            overrides: None,
            variant_set: Some(VariantSet {
                start_ts: 0,
                stop_ts: 2147483648, // 2 ** 31 - far future.
                shuffle_version: 0,
                bucket_val: BucketVal::UserId,
                variants: vec![v],
                holdout: None,
                mutex_group: None,
            }),
            value: Some(serde_json::Value::Null),
        }
    }

    fn make_dynamic_config(dc: Dc) -> Feature {
        let name_str: String;

        let value: serde_json::Value = match dc {
            Dc::Bool(val) => {
                name_str = "bool".to_string();
                match val {
                    None => serde_json::Value::Bool(true),
                    Some(b) => b,
                }
            }
            Dc::Int(val) => {
                name_str = "int".to_string();
                match val {
                    None => serde_json::Value::from(1),
                    Some(i) => i,
                }
            }
            Dc::Float(val) => {
                name_str = "float".to_string();
                match val {
                    None => serde_json::Value::from(2.0),
                    Some(f) => f,
                }
            }
            Dc::String(val) => {
                name_str = "string".to_string();
                match val {
                    None => serde_json::Value::from("some_string"),
                    Some(s) => s,
                }
            }
            Dc::Map(val) => {
                name_str = "map".to_string();
                match &val {
                    None => serde_json::from_str(r#"{"v":{"nested_map": {"w":false,"x": 1,"y":"some_string","z":3.0}},"w":false,"x": 1,"y":"some_string","z":3.0}"#).unwrap(),
                    Some(s) => serde_json::from_str(s).unwrap()
                }
            }
        };

        Feature {
            id: 2,
            name: name_str + "_dynamic_config",
            enabled: true,
            version: 1,
            value: Some(value),
            targeting: None,
            overrides: None,
            platform_bitmask: 0,
            variant_set: None,
        }
    }

    fn make_experiment(name: String, meg: Option<String>, hg: Option<String>) -> Experiment {
        let c = Variant {
            name: "control".to_string(),
            hi: 1.0,
            lo: 0.9,
        };
        let t = Variant {
            name: "treatment".to_string(),
            hi: 0.1,
            lo: 0.0,
        };
        Experiment {
            id: 1,
            name: name.clone(),
            experiment_type: ExperimentType::RangeVariant,
            enabled: true,
            start_ts: 0,
            stop_ts: 2147483648, // 2 ** 31 - far future.
            version: "1".to_string(),
            experiment: InnerExperiment {
                shuffle_version: 0,
                variants: vec![t, c],
                bucket_val: BucketVal::UserId,
                experiment_version: 1,
                targeting: None,
                overrides: None,
            },
            parent_hg_name: hg,
            parent_meg_name: meg,
            value: None,
        }
    }

    fn make_ctx(json: Option<String>) -> Result<Context, Error> {
        let c = Context {
            user_id: "795244".to_string(),
            locale: Some("US".to_string()),
            device_id: None,
            country_code: None,
            origin_service: None,
            user_is_employee: None,
            logged_in: None,
            app_name: None,
            build_number: None,
            authentication_token: None,
            request_url: None,
            cookie_created_timestamp: None,
        };
        return match json {
            None => Ok(c),
            Some(s) => {
                let cr = serde_json::from_str(&s);
                cr
            }
        };
    }

    fn make_tt(json: String) -> TargetingTree {
        let res: TargetingTree = serde_json::from_str(&json).unwrap();
        res
    }

    #[test]
    fn parse_targeting_tree() {
        let tt1 = make_tt(r#"{"EQ": {"field": "user_id", "values": ["795244"]}}"#.to_string());
        let tt2 = make_tt(r#"{"EQ": {"field": "user_id", "value": "795244"}}"#.to_string());
        let tt3 = make_tt(r#"{"NE": {"field": "user_id", "value": "795244"}}"#.to_string());
        let tt4 = make_tt(r#"{"GT": {"field": "user_id", "value": 7}}"#.to_string());
        let tt5 = make_tt(r#"{"LT": {"field": "user_id", "value": 8}}"#.to_string());
        let tt6 = make_tt(r#"{"GE": {"field": "user_id", "value": 8}}"#.to_string());
        let tt7 = make_tt(r#"{"LE": {"field": "user_id", "value": 8}}"#.to_string());

        let ctx1 = make_ctx(None).unwrap();
        let ctx2: Context = make_ctx(Some(r#"{"user_id": "7"}"#.to_string())).unwrap();

        assert!(tt1.eval(&ctx1)); // ctx1 has user_id 795244, so EQ passes
        assert!(!tt1.eval(&ctx2)); // ctx2 has user_id 7, so EQ fails
        assert!(tt2.eval(&ctx1)); // tt1 and tt2 are the same, just different representations
        assert!(!tt2.eval(&ctx2)); // so should have same results

        assert!(!tt3.eval(&ctx1)); // ctx has user_id 795244, so NE against 795244 fails
        assert!(tt3.eval(&ctx2)); // ctx2 has user_id 7, so NE against 7 passes

        assert!(tt4.eval(&ctx1)); // ctx has user_id 795244, so GT against 7 passes
        assert!(!tt4.eval(&ctx2)); // ctx2 has user_id 7, so GT against 7 fails

        assert!(!tt5.eval(&ctx1)); // ctx has user_id 795244, so LT against 8 passes
        assert!(tt5.eval(&ctx2)); // ctx2 has user_id 7, so LT against 8 fails

        assert!(tt6.eval(&ctx1)); // ctx has user_id 795244, so GE against 8 passes
        assert!(!tt6.eval(&ctx2)); // ctx2 has user_id 7, so GE against 8 fails

        assert!(!tt7.eval(&ctx1)); // ctx has user_id 795244, so LE against 8 fails
        assert!(tt7.eval(&ctx2)); // ctx2 has user_id 7, so LE against 8 passes
    }

    fn build_decider(
        cfgo: Option<String>,
        fvo: Option<Vec<Feature>>,
        dcvo: Option<Vec<Feature>>,
    ) -> Result<Decider, DeciderFailType> {
        let fv = match fvo {
            None => vec![make_feature()],
            Some(fv) => fv,
        };
        let dcv = match dcvo {
            None => vec![
                make_dynamic_config(Dc::Bool(None)),
                make_dynamic_config(Dc::Int(None)),
                make_dynamic_config(Dc::Float(None)),
                make_dynamic_config(Dc::String(None)),
                make_dynamic_config(Dc::Map(None)),
            ],
            Some(dc) => dc,
        };
        let cfg = match cfgo {
            Some(s) => s,
            None => "darkmode".to_string(), // set a reasonable default here?
        };
        return init(cfg, [fv, dcv].concat());
    }

    #[test]
    fn decider_initialization_works() -> Result<(), DeciderFailType> {
        let ctx = make_ctx(None)?;
        let d = build_decider(None, None, None)?;
        d.choose("first_feature".to_string(), &ctx)?;
        Ok(())
    }

    #[test]
    fn decider_errors_on_missing_name() -> Result<(), DeciderFailType> {
        let ctx = make_ctx(None)?;
        let d = build_decider(None, None, None)?;
        let r = d.choose("missing".to_string(), &ctx);
        match r {
            Ok(_) => panic!(),
            Err(e) => println!("got expected error: {:#?}", e),
        }
        Ok(())
    }

    #[test]
    fn test_name_to_decisionmaker() -> Result<(), String> {
        name_to_decisionmaker("darkmode")?;
        name_to_decisionmaker("fractional_availability")?;
        name_to_decisionmaker("locale")?;
        name_to_decisionmaker("value")?;
        let res = name_to_decisionmaker("bad-shouldbreak");
        match res {
            Ok(_) => Err("obviously bad variant: bad-shouldbreak passed".to_string()),
            Err(_) => Ok(()),
        }
    }

    proptest! {
        #[test]
        fn init_decider_doesnt_crash(s in "\\PC*") {
            let res = init_decider(s.to_string(), "../cfgsmall.json".to_string());
            match res {
                Ok(d) => println!("success: {:#?}", d),
                Err(e) => println!("error: {:#?}", e),
            }
        }
    }

    #[test]
    fn holdout_meg_parsing() -> Result<(), DeciderFailType> {
        let e1 = make_experiment(
            "first".to_string(),
            Some("meg".to_string()),
            Some("hg".to_string()),
        );
        let e2 = make_experiment(
            "second".to_string(),
            Some("meg_missing".to_string()),
            Some("hg".to_string()),
        );
        let meg = make_experiment("meg".to_string(), None, None);
        let hg = make_experiment("hg".to_string(), None, None);
        let ec: ExperimentConfig = HashMap::from([
            ("first".to_string(), e1),
            ("second".to_string(), e2),
            ("meg".to_string(), meg),
            ("hg".to_string(), hg),
        ]);

        let fv: Vec<Feature> = experiment_config_to_features(ec)?;
        let f1 = fv.iter().find(|&f| f.name == "first").unwrap();
        let f2 = fv.iter().find(|&f| f.name == "second").unwrap();
        let fmeg = fv.iter().find(|&f| f.name == "meg").unwrap();
        let fhg = fv.iter().find(|&f| f.name == "hg").unwrap();
        assert!(get_fp(&f1, FeatureParent::Holdout)?.name.clone() == fhg.name);
        assert!(get_fp(&f1, FeatureParent::Meg)?.name.clone() == fmeg.name);
        assert!(get_fp(&f2, FeatureParent::Meg).is_err());
        assert!(get_fp(&f2, FeatureParent::Holdout)?.name.clone() == fhg.name);
        assert!(get_fp(&fmeg, FeatureParent::Holdout).is_err());
        assert!(get_fp(&fmeg, FeatureParent::Meg).is_err());
        assert!(get_fp(&fhg, FeatureParent::Holdout).is_err());
        assert!(get_fp(&fhg, FeatureParent::Meg).is_err());
        Ok(())
    }

    enum FeatureParent {
        Meg,
        Holdout,
    }

    fn get_fp(f: &Feature, fp: FeatureParent) -> Result<FeatureGroup, DeciderFailType> {
        // grab the specified feature_parent(holdout or meg) from a feature, or err trying.
        if let Some(variant_set) = &f.variant_set {
            let fpo = match fp {
                FeatureParent::Meg => variant_set.mutex_group.clone(),
                FeatureParent::Holdout => variant_set.holdout.clone(),
            };
            return match fpo {
                None => Err(DeciderFailType::FeatureNotFound),
                Some(feature_parent) => Ok(feature_parent.clone()),
            };
        } else {
            return Err(DeciderFailType::FeatureNotFound);
        };
    }

    #[test]
    fn get_bool_works() -> Result<(), DeciderFailType> {
        let ctx = make_ctx(None)?;
        let d = build_decider(
            Some("darkmode fractional_availability value".to_string()),
            None,
            None,
        )?;
        let dc_res = d.get_bool("bool_dynamic_config".to_string(), &ctx);
        match dc_res {
            Ok(res) => {
                if res == true {
                    println!("got expected boolean: {:#?}", res)
                } else {
                    panic!()
                }
            }
            _ => panic!(),
        }

        Ok(())
    }

    #[test]
    fn get_bool_errors_on_missing_name() -> Result<(), DeciderFailType> {
        let ctx = make_ctx(None)?;
        let d = build_decider(
            Some("darkmode fractional_availability value".to_string()),
            None,
            None,
        )?;
        let r = d.get_bool("missing".to_string(), &ctx);
        match r {
            Ok(_) => panic!(),
            Err(e) => println!("got expected error: {:#?}", e),
        }
        Ok(())
    }

    #[test]
    fn get_int_works() -> Result<(), DeciderFailType> {
        let ctx = make_ctx(None)?;
        let d = build_decider(
            Some("darkmode fractional_availability value".to_string()),
            None,
            None,
        )?;
        let dc_res = d.get_int("int_dynamic_config".to_string(), &ctx);
        match dc_res {
            Ok(res) => {
                if res == 1 {
                    println!("got expected int: {:#?}", res)
                } else {
                    panic!()
                }
            }
            _ => panic!(),
        }

        Ok(())
    }

    #[test]
    fn get_int_errors_on_missing_name() -> Result<(), DeciderFailType> {
        let ctx = make_ctx(None)?;
        let d = build_decider(
            Some("darkmode fractional_availability value".to_string()),
            None,
            None,
        )?;
        let r = d.get_int("missing".to_string(), &ctx);
        match r {
            Ok(_) => panic!(),
            Err(e) => println!("got expected error: {:#?}", e),
        }
        Ok(())
    }

    #[test]
    fn get_float_works() -> Result<(), DeciderFailType> {
        let ctx = make_ctx(None)?;
        let d = build_decider(
            Some("darkmode fractional_availability value".to_string()),
            None,
            None,
        )?;
        let dc_res = d.get_float("float_dynamic_config".to_string(), &ctx);
        match dc_res {
            Ok(res) => {
                if res == 2.0 {
                    println!("got expected float: {:#?}", res)
                } else {
                    panic!()
                }
            }
            _ => panic!(),
        }

        Ok(())
    }

    #[test]
    fn get_float_errors_on_missing_name() -> Result<(), DeciderFailType> {
        let ctx = make_ctx(None)?;
        let d = build_decider(
            Some("darkmode fractional_availability value".to_string()),
            None,
            None,
        )?;
        let r = d.get_float("missing".to_string(), &ctx);
        match r {
            Ok(_) => panic!(),
            Err(e) => println!("got expected error: {:#?}", e),
        }
        Ok(())
    }

    #[test]
    fn get_string_works() -> Result<(), DeciderFailType> {
        let ctx = make_ctx(None)?;
        let d = build_decider(
            Some("darkmode fractional_availability value".to_string()),
            None,
            None,
        )?;
        let dc_res = d.get_string("string_dynamic_config".to_string(), &ctx);
        match dc_res {
            Ok(res) => {
                if res == "some_string" {
                    println!("got expected string: {:#?}", res)
                } else {
                    panic!()
                }
            }
            _ => panic!(),
        }

        Ok(())
    }

    #[test]
    fn get_string_errors_on_missing_name() -> Result<(), DeciderFailType> {
        let ctx = make_ctx(None)?;
        let d = build_decider(
            Some("darkmode fractional_availability value".to_string()),
            None,
            None,
        )?;
        let r = d.get_string("missing".to_string(), &ctx);
        match r {
            Ok(_) => panic!(),
            Err(e) => println!("got expected error: {:#?}", e),
        }
        Ok(())
    }

    #[test]
    fn get_map_works() -> Result<(), DeciderFailType> {
        let ctx = make_ctx(None)?;
        let map_dc_str = r#"{"v":{"nested_map": {"w":false,"x": 1,"y":"some_string","z":3.0}},"w":false,"x": 1,"y":"some_string","z":3.0}"#;
        let d = build_decider(
            Some("darkmode fractional_availability value".to_string()),
            None,
            Some(vec![make_dynamic_config(Dc::Map(Some(
                map_dc_str.to_string(),
            )))]),
        )?;
        let map = serde_json::from_str(map_dc_str).unwrap();
        let dc_res = d.get_map("map_dynamic_config".to_string(), &ctx);
        match dc_res {
            Ok(res) => {
                if res == map {
                    println!("got expected map: {:#?}", res)
                } else {
                    panic!()
                }
            }
            _ => panic!(),
        }

        Ok(())
    }

    #[test]
    fn get_map_errors_on_missing_name() -> Result<(), DeciderFailType> {
        let ctx = make_ctx(None)?;
        let d = build_decider(
            Some("darkmode fractional_availability value".to_string()),
            None,
            None,
        )?;
        let r = d.get_map("missing".to_string(), &ctx);
        match r {
            Ok(_) => panic!(),
            Err(e) => println!("got expected error: {:#?}", e),
        }
        Ok(())
    }

    #[test]
    fn test_value_eq() -> Result<(), String> {
        let v = json!({
            "s": "a string",
            "s2": "a string",
            "sn": "7",
            "n": 7i64,
            "bt1": true,
            "bt2": true,
            "bf": false,
            "bf2": false,
            "a": ["1", "2"],
            "o": {"a": 7i64}});

        // these comparisons are sensible enough, if sometimes false...
        assert!(true == value_eq(v["n"].clone(), v["n"].clone()).unwrap());
        assert!(true == value_eq(v["s"].clone(), v["s"].clone()).unwrap());
        assert!(true == value_eq(v["s"].clone(), v["s2"].clone()).unwrap());
        assert!(false == value_eq(v["sn"].clone(), v["s2"].clone()).unwrap());
        assert!(true == value_eq(v["bf"].clone(), v["bf2"].clone()).unwrap());
        assert!(true == value_eq(v["sn"].clone(), v["n"].clone()).unwrap());
        assert!(true == value_eq(v["n"].clone(), v["sn"].clone()).unwrap());
        assert!(true == value_eq(v["bt1"].clone(), v["bt2"].clone()).unwrap());
        assert!(false == value_eq(v["n"].clone(), v["s"].clone()).unwrap());
        assert!(false == value_eq(v["bt"].clone(), v["bf"].clone()).unwrap());

        // but here lies madness
        assert!(value_eq(v["n"].clone(), v["tb"].clone()).is_err());
        assert!(value_eq(v["n"].clone(), v["a"].clone()).is_err());
        assert!(value_eq(v["a"].clone(), v["o"].clone()).is_err());
        assert!(value_eq(v["a"].clone(), v["a"].clone()).is_err());
        Ok(())
    }
}
