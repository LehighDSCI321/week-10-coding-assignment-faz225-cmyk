from collections import deque

class SortableDigraph:
    """
    Base class representing a simple directed graph.
    Stores nodes and directed edges in a dictionary.
    """

    def __init__(self):
        # Each key is a node; each value is a list of neighbors (successors)
        self.graph = {}
        # Optional: store node values if tests require
        self.node_values = {}

    def add_node(self, node, value=None):
        """
        Add a node to the graph.
        If 'value' is provided, store it in the node_values dictionary.
        """
        if node not in self.graph:
            self.graph[node] = []
        if value is not None:
            self.node_values[node] = value

    def add_edge(self, src, dst):
        """
        Add a directed edge from src to dst.
        Automatically adds missing nodes.
        """
        if src not in self.graph:
            self.add_node(src)
        if dst not in self.graph:
            self.add_node(dst)
        self.graph[src].append(dst)

    def neighbors(self, node):
        """Return a list of all nodes directly reachable from 'node'."""
        return self.graph.get(node, [])

    def get_successors(self, node):
        """Alias for neighbors(node)"""
        return self.neighbors(node)

    def get_predecessors(self, node):
        """Return all nodes that have an edge pointing to this node."""
        return [n for n, neighbors in self.graph.items() if node in neighbors]

    def __contains__(self, node):
        return node in self.graph

    def __repr__(self):
        return f"{self.graph}"


# ============================================================
# TraversableDigraph
# ============================================================
class TraversableDigraph(SortableDigraph):
    """Directed graph that supports DFS and BFS traversal."""

    def dfs(self, start, visited=None):
        """Depth-First Search traversal implemented as a generator."""
        if visited is None:
            visited = set()
        visited.add(start)
        yield start
        for neighbor in self.neighbors(start):
            if neighbor not in visited:
                yield from self.dfs(neighbor, visited)

    def bfs(self, start):
        """Breadth-First Search traversal using a queue."""
        visited = set([start])
        queue = deque([start])
        while queue:
            node = queue.popleft()
            yield node
            for neighbor in self.neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)


# ============================================================
# DAG
# ============================================================
class DAG(TraversableDigraph):
    """Directed Acyclic Graph (no cycles allowed)."""

    def add_edge(self, src, dst):
        """Add an edge only if it doesn't create a directed cycle."""
        if self._has_path(dst, src):
            raise ValueError(f"Adding edge {src} -> {dst} would create a cycle.")
        super().add_edge(src, dst)

    def _has_path(self, start, target, visited=None):
        """Check if there is a path from start to target (to detect cycles)."""
        if visited is None:
            visited = set()
        if start == target:
            return True
        visited.add(start)
        for neighbor in self.neighbors(start):
            if neighbor not in visited and self._has_path(neighbor, target, visited):
                return True
        return False
