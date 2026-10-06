"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def _ev(metric, labels):
    return {"metric": metric, "labels": labels, "value": 1}


def run(name):
    if name == "permetric":
        events = [
            _ev("http", {"code": "200"}),
            _ev("http", {"code": "500"}),
            _ev("rpc", {"code": "0"}),
            _ev("rpc", {"code": "1"}),
        ]
        res = core.ingest(events, 2, core.Counter())
        _line({"actions": [r["action"] for r in res]})
        return 0
    if name == "overflow":
        events = [
            _ev("http", {"m": "GET"}),
            _ev("http", {"m": "POST"}),
            _ev("http", {"m": "PUT"}),
        ]
        res = core.ingest(events, 2, core.Counter())
        _line({"actions": [r["action"] for r in res], "keys": [r["key"] for r in res]})
        return 0
    if name == "dup":
        events = [
            _ev("http", {"code": "200"}),
            _ev("http", {"code": "200"}),
        ]
        res = core.ingest(events, 10, core.Counter())
        _line({"cardinality": [r["cardinality"] for r in res]})
        return 0
    if name == "order":
        events = [
            _ev("http", {"a": "1", "b": "2"}),
            _ev("http", {"b": "2", "a": "1"}),
        ]
        res = core.ingest(events, 10, core.Counter())
        _line({"cardinality": [r["cardinality"] for r in res], "keys": [r["key"] for r in res]})
        return 0
    if name == "work":
        events = [_ev("http", {"code": "c%04d" % i}) for i in range(2000)]
        counter = core.Counter()
        core.ingest(events, 100000, counter)
        _line({"events": 2000, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
