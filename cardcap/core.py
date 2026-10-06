"""按标签组合做基数限制。"""

OVERFLOW = "__overflow__"


class Counter:
    """记录本批处理里做过的组合比较次数。"""

    def __init__(self):
        self.scanned = 0


def label_key(labels):
    """把标签集合写成一个组合串。"""
    return ",".join("%s=%s" % (k, labels[k]) for k in sorted(labels))


def ingest(events, cap, counter):
    """逐条收采样，返回每条采样的判定结果。"""
    ledgers = {}
    out = []
    for ev in events:
        metric = ev["metric"]
        key = label_key(ev.get("labels", {}))
        state = ledgers.setdefault(metric, {"keys": set(), "overflow": False})
        counter.scanned += 1
        if key in state["keys"]:
            action = "keep"
        elif len(state["keys"]) < cap:
            state["keys"].add(key)
            action = "keep"
        else:
            state["overflow"] = True
            action = "merge"
            key = OVERFLOW
        cardinality = len(state["keys"]) + (1 if state["overflow"] else 0)
        out.append({
            "metric": metric,
            "key": key,
            "action": action,
            "cardinality": cardinality,
        })
    return out
