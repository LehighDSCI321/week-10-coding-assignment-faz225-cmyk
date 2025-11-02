"""student_code.py
Directed Graph and DAG implementation for traversal, topological sorting, and testing.
This module follows PEP8 and Pylint clean style conventions.
"""

from collections import deque


class TraversableDigraph:
    """A basic directed graph supporting node addition and traversal."""

    def __init__(self):
        self.adj_list = {}
        self.node_weights = {}

    def add_node(self, node, node_weight=None):
        """Add a node with an optional weight."""
        if node not in self.adj_list:
            self.adj_list[node] = []
            self.node_weights[node] = node_weight

    def get_nodes(self):
        """Return all node labels."""
        return list(self.adj_list.keys())

    def get_node_value(self, node):
        """Return stored weight/value of a node."""
        return self.node_weights.get(node, None)

    def add_edge(self, src, dst, edge_weight=None):
        """Add a directed edge from src to dst with optional edge weight."""
        if src not in self.adj_list:
            self.add_node(src)
        if dst not in self.adj_list:
            self.add_node(dst)
        self.adj_list[src].append((dst, edge_weight))

    def get_edge_weight(self, src, dst):
        """Return the weight of an edge if it exists."""
        for neighbor, weight in self.adj_list.get(src, []):
            if neighbor == dst:
                return weight
        return None

    def bfs(self, start):
        """Perform BFS traversal starting from `start` (excluding the start node)."""
        visited = set()
        queue = deque([start])
        order = []
        visited.add(start)
        while queue:
            node = queue.popleft()
            for neighbor, _ in self.adj_list.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    order.append(neighbor)
                    queue.append(neighbor)
        return order

    def dfs(self, start):
        """Perform DFS traversal starting from `start` (excluding the start node)."""
        visited = set()
        order = []

        def dfs_visit(node):
            for neighbor, _ in self.adj_list.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    order.append(neighbor)
                    dfs_visit(neighbor)

        visited.add(start)
        dfs_visit(start)
        return order


class DAG(TraversableDigraph):
    """Directed Acyclic Graph with cycle detection and topological sorting."""

    def __init__(self):
        # pylint: disable=useless-parent-delegation
        super().__init__()

    def add_edge(self, src, dst, edge_weight=None):
        """Add an edge while ensuring no cycles are introduced."""
        super().add_edge(src, dst, edge_weight)
        if self._creates_cycle():
            # Remove the last added edge if it creates a cycle
            self.adj_list[src] = [
                (n, w) for n, w in self.adj_list[src] if n != dst or w != edge_weight
            ]
            raise ValueError("Adding this edge creates a cycle in the DAG.")

    def _creates_cycle(self):
        """Detect if the graph has a cycle using DFS-based detection."""
        visited = set()
        rec_stack = set()

        def dfs(node):
            visited.add(node)
            rec_stack.add(node)
            for neighbor, _ in self.adj_list.get(node, []):
                if neighbor not in visited and dfs(neighbor):
                    return True
                if neighbor in rec_stack:
                    return True
            rec_stack.remove(node)
            return False

        for node in self.adj_list:
            if node not in visited and dfs(node):
                return True
        return False

    def top_sort(self):
        """Perform topological sort (Kahn's Algorithm)."""
        in_degree = {node: 0 for node in self.adj_list}
        for src, edges in self.adj_list.items():  # ✅ fixed pylint C0206
            for dst, _ in edges:
                in_degree[dst] += 1

        queue = deque([n for n, deg in in_degree.items() if deg == 0])  # ✅ .items()
        result = []
        while queue:
            node = queue.popleft()
            result.append(node)
            for neighbor, _ in self.adj_list.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        return result

    def successors(self, node):
        """Return successors of a node."""
        return [n for n, _ in self.adj_list.get(node, [])]

    def predecessors(self, node):
        """Return predecessors of a node."""
        preds = []
        for src, edges in self.adj_list.items():  # ✅ fixed pylint C0206
            for dst, _ in edges:
                if dst == node:
                    preds.append(src)
        return preds
