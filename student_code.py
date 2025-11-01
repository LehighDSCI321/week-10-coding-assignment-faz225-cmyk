"""Graph implementation for DAG, TraversableDigraph, and SortableDigraph."""

from collections import deque


class VersatileDigraph:
    """A versatile directed graph class with support for node/edge management."""

    def __init__(self):
        self.nodes = set()
        self.edges = {}

    def add_node(self, node, *_args, **_kwargs):
        self.nodes.add(node)
        if node not in self.edges:
            self.edges[node] = set()

    def add_edge(self, u, v):
        self.add_node(u)
        self.add_node(v)
        self.edges[u].add(v)

    def get_neighbors(self, node):
        return self.edges.get(node, set())

    def get_all_nodes(self):
        return list(self.nodes)

    def get_nodes(self):
        return self.get_all_nodes()

    def successors(self, node):
        return list(self.get_neighbors(node))

    def predecessors(self, node):
        return [n for n in self.nodes if node in self.get_neighbors(n)]


class SortableDigraph(VersatileDigraph):
    """A directed graph that supports topological sorting."""

    def top_sort(self):
        in_degree = {n: 0 for n in self.nodes}
        for current_node in self.nodes:
            for neighbor in self.get_neighbors(current_node):
                in_degree[neighbor] += 1

        queue = deque(n for n in self.nodes if in_degree[n] == 0)
        top_order = []

        while queue:
            current = queue.popleft()
            top_order.append(current)
            for neighbor in self.get_neighbors(current):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return top_order


class TraversableDigraph(SortableDigraph):
    """A directed graph supporting DFS and BFS traversals."""

    def dfs(self, start):
        visited = set()

        def _dfs(node):
            if node in visited:
                return
            visited.add(node)
            if node != start:
                yield node
            for neighbor in self.get_neighbors(node):
                yield from _dfs(neighbor)

        yield from _dfs(start)

    def bfs(self, start):
        visited = {start}
        queue = deque([start])

        while queue:
            node = queue.popleft()
            for neighbor in self.get_neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    yield neighbor


class DAG(TraversableDigraph):
    """A Directed Acyclic Graph class that blocks cycle-forming edges."""

    def add_edge(self, start, end, **_kwargs):
        for node in self.dfs(end):
            if node == start:
                raise ValueError("Adding this edge would create a cycle.")
        super().add_edge(start, end)
