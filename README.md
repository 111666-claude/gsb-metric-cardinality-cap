# metric-cardinality-cap

把一行一条的指标采样（JSONL）按标签组合收进基数上限里。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m cardcap --sample=permetric
python3 -m cardcap --sample=overflow
python3 -m cardcap --sample=dup
python3 -m cardcap --sample=order
python3 -m cardcap --sample=work
```

## 口径

- **组合**：一条采样的组合由指标名与标签集合共同决定，标签书写顺序不影响组合身份。
- **基数**：每个指标名各有一份组合台账；上限是"每个指标"的组合条数，不是全局条数。
- **合并**：某指标的组合条数达到上限后，再出现的新组合归入该指标的一个合并桶，合并桶只占一个位置。
- **幂等**：同一组合重复进来只算一条，台账里的条数不增长。

## 不变量

- 每个指标的组合台账条数不超过上限，另有至多一个合并桶。
- 同一组合无论出现多少次、标签次序如何，都只对应台账里的一条。
- `scanned` 不随采样条数平方级放大：两千条采样的 `scanned` 不超过 6000。

## 输出契约

每条采样对应一条 JSON 结果，字段 `metric` / `key` / `action` / `cardinality`；
`action` 取 `keep` 或 `merge`，`key` 是归一化后的组合串，`cardinality` 是该指标当前台账条数。
合并桶的组合串固定为 `__overflow__`。
`--sample=work` 只打印 `{"events": N, "scanned": N}`。
