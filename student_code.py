from collections import deque

class SortableDigraph:
    """基础有向图类：假设已提供节点与边结构"""
    def __init__(self):
        self.graph = {}  # 字典结构：{节点: [相邻节点列表]}

    def add_vertex(self, v):
        if v not in self.graph:
            self.graph[v] = []

    def add_edge(self, src, dst):
        """添加一条有向边"""
        self.add_vertex(src)
        self.add_vertex(dst)
        self.graph[src].append(dst)

    def neighbors(self, v):
        """返回节点的所有邻居"""
        return self.graph.get(v, [])

    def __contains__(self, v):
        return v in self.graph

    def __repr__(self):
        return f"{self.graph}"


# ============================================================
# TraversableDigraph：支持 DFS / BFS 遍历
# ============================================================
class TraversableDigraph(SortableDigraph):
    """继承自 SortableDigraph，增加 DFS 与 BFS 功能"""

    def dfs(self, start, visited=None):
        """深度优先遍历（递归生成器实现）"""
        if visited is None:
            visited = set()
        visited.add(start)
        yield start  # 访问当前节点
        for neighbor in self.neighbors(start):
            if neighbor not in visited:
                yield from self.dfs(neighbor, visited)

    def bfs(self, start):
        """广度优先遍历（使用 deque 队列）"""
        visited = set()
        queue = deque([start])
        visited.add(start)

        while queue:
            node = queue.popleft()
            yield node  # 生成下一个节点
            for neighbor in self.neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)


# ============================================================
# DAG：继承自 TraversableDigraph，重写 add_edge 防止环路
# ============================================================
class DAG(TraversableDigraph):
    """有向无环图（Directed Acyclic Graph）"""

    def add_edge(self, src, dst):
        """添加边时防止形成环"""
        # 若添加的边 src -> dst 会形成 dst -> src 路径，则拒绝
        if self._has_path(dst, src):
            raise ValueError(f"Adding edge {src} -> {dst} would create a cycle.")
        super().add_edge(src, dst)

    def _has_path(self, start, target, visited=None):
        """判断是否存在从 start 到 target 的路径"""
        if visited is None:
            visited = set()
        if start == target:
            return True
        visited.add(start)
        for neighbor in self.neighbors(start):
            if neighbor not in visited and self._has_path(neighbor, target, visited):
                return True
        return False


# ============================================================
# 示例测试
# ============================================================
if __name__ == "__main__":
    # 构建示例图（衣服穿着顺序）
    g = DAG()
    g.add_edge("shirt", "vest")
    g.add_edge("shirt", "pants")
    g.add_edge("shirt", "socks")
    g.add_edge("vest", "jacket")
    g.add_edge("pants", "tie")
    g.add_edge("pants", "belt")
    g.add_edge("belt", "jacket")
    g.add_edge("socks", "shoes")
    g.add_edge("shoes", "jacket")

    print("图结构：", g.graph)

    print("\nDFS 从 shirt 开始：")
    print(list(g.dfs("shirt")))

    print("\nBFS 从 shirt 开始：")
    print(list(g.bfs("shirt")))

    # 尝试添加会造成环的边
    try:
        g.add_edge("jacket", "shirt")
    except ValueError as e:
        print("\n⚠️ 检测到环路：", e)
