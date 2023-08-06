# xUnionFind
一个简单使用的并查集

```python
uf = UnionFind()
uf.union(1, 2)
uf.union(3, 4)
uf.union(5, 6)
uf.union(1, 3)
uf.union(6, 4)

assert uf.connected(1, 6)
```
