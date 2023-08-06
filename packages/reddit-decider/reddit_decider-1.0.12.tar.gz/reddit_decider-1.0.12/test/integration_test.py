#!/usr/bin/env python
import json
import os
import random
import time

from unittest import TestCase

import rust_decider

from reddit_experiments import Experiments
from utils import make_experiment
from utils import make_request_context_map

# from utils import make_overrides
# from utils import targeting_tree
# from utils import make_variants

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def setup_baseplate_experiments(cfg_path):
    h = json.load(open(cfg_path))
    # we really only want to populate the raw string cache of _cfg_data,
    # so that when we go looking for keys, we find them.
    el = Experiments(
        cfg_data=h, config_watcher=None, server_span=None, context_name=None
    )
    return el


def setup_decider(cfg_path):
    return rust_decider.init(
        "darkmode targeting fractional_availability value", cfg_path
    )


def compare_implementations_against_cfg(cfg_path, user_ids, exp_names=None):
    if exp_names is None:
        h = json.load(open(cfg_path))
        exp_names = [
            k for k in h.keys() if k[0] in ["e", "g"]
        ]  # needed because the default cfg has some DCs.
    dc = setup_decider(cfg_path)
    bp = setup_baseplate_experiments(cfg_path)
    successes = []
    failures = []
    for exp_name in exp_names:
        for uid in user_ids:
            ctx_map = make_request_context_map({"user_id": str(uid)})
            ctx = rust_decider.make_ctx(ctx_map)
            res = dc.choose(exp_name, ctx)
            bpv = bp.variant(
                exp_name, user_id=str(uid), device_id=str(ctx_map.get("device_id"))
            )
            if res.err() or not (bpv == res.decision()):
                failures.append(
                    {
                        "uid": uid,
                        "exp_name": exp_name,
                        "dc": res.decision(),
                        "bpv": bpv,
                        "ctx": ctx_map,
                        "res": res,
                    }
                )
                print(
                    f"failure:{exp_name} {uid} bp:{bpv} != dc:{res.decision()} ctx={ctx_map}"
                )
            else:
                successes.append(uid)
    return successes, failures


class TestRustWithSdk(TestCase):
    def test_impls_against_cfg(self):
        cfg_path = f"{TEST_DIR}/../../cfg.json"
        h = json.load(open(cfg_path))
        exp_names = [k for k in h.keys() if k[0] in ["e", "g"]]
        uids = range(3000)
        good, bad = compare_implementations_against_cfg(cfg_path, uids, exp_names)
        if bad:
            print("mismatches found!\n\n", bad)
        else:
            print("all_good!")

        self.assertEqual(bad, [])
        self.assertEqual(len(good), len(uids) * len(exp_names))

    def test_impls_against_generated(self):
        # we want to be able to reproduce failures, so seed the RNG with the current timestamp,
        # and then log it on failures.  This will assist in debugging test fails.
        seed = int(time.time())
        random.seed(seed)
        msg = f"random seed={seed}"
        exp_cfg = {e["name"]: e for e in [make_experiment(n) for n in range(20)]}
        fn = "/tmp/genexp"  # TODO: generate the filename
        f = open(fn, "w")
        f.write(json.dumps(exp_cfg, indent=2))
        f.close()
        good, bad = compare_implementations_against_cfg(fn, range(3000))
        self.assertEqual(len(bad), 0, msg)
        self.assertEqual(len(good), 3000 * 20, msg)
