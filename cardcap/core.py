"""按标签组合做基数限制。"""

OVERFLOW = "__overflow__"


class Counter:
    """记录本批处理里做过的组合比较次数。"""

    def __init__(self):
        self.scanned = 0


def label_key(labels):
    """把标签集合写成一个组合串。"""
    return ",".join("%s=%s" % (k, labels[k]) for k in labels)


def ingest(events, cap, counter):
    """逐条收采样，返回每条采样的判定结果。"""
    seen = {}
    out = []
    for ev in events:
        metric = ev["metric"]
        key = label_key(ev.get("labels", {}))
        bucket = seen.setdefault(metric, [])
        for existing in bucket:
            counter.scanned += 1
            if existing == key:
                break
        bucket.append(key)
        total = sum(len(v) for v in seen.values())
        if total > cap:
            action = "drop"
        else:
            action = "keep"
        out.append({
            "metric": metric,
            "key": key,
            "action": action,
            "cardinality": total,
        })
    return out
