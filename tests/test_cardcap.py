import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cardcap import core


def ev(metric, labels):
    return {"metric": metric, "labels": labels, "value": 1}


class CardcapTest(unittest.TestCase):
    def test_empty_input(self):
        self.assertEqual(core.ingest([], 4, core.Counter()), [])

    def test_single_sample_is_kept(self):
        res = core.ingest([ev("http", {"code": "200"})], 4, core.Counter())
        self.assertEqual(res[0]["action"], "keep")
        self.assertEqual(res[0]["cardinality"], 1)

    def test_result_fields(self):
        res = core.ingest([ev("http", {"code": "200"})], 4, core.Counter())
        for field in ("metric", "key", "action", "cardinality"):
            self.assertIn(field, res[0])

    def test_two_series_under_cap(self):
        events = [ev("http", {"code": "200"}), ev("http", {"code": "500"})]
        res = core.ingest(events, 5, core.Counter())
        self.assertEqual([r["action"] for r in res], ["keep", "keep"])

    def test_counting_happens(self):
        counter = core.Counter()
        core.ingest([ev("http", {"code": "200"}), ev("http", {"code": "500"})], 5, counter)
        self.assertGreater(counter.scanned, 0)


if __name__ == "__main__":
    unittest.main()
