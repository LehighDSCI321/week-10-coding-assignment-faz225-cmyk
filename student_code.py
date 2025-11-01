
from collections import deque

class TraversableDigraph(SortableDigraph):
    def dfs(self, start):
        # Depth-first traversal generator: yields each node as it is visited.
        visited = set()
        def _dfs(node):
            if node in visited:
                return  # Already visited this node, skip to avoid cycles
            visited.add(node)
            yield node  # Visit the node
            # Traverse neighbors (outgoing edges) in depth-first manner
            for neighbor in self._edges.get(node, []):
                yield from _dfs(neighbor)
        # Start DFS from the given start node
        yield from _dfs(start)

    def bfs(self, start):
        # Breadth-first traversal generator: yields each node as it is visited.
        visited = set([start])
        queue = deque([start])
        while queue:
            node = queue.popleft()
            yield node  # Visit the node
            # Traverse neighbors (outgoing edges) in breadth-first manner
            for neighbor in self._edges.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

class DAG(TraversableDigraph):
    def add_edge(self, start, end):
        # Before adding a new edge, check if a path exists from `end` to `start`.
        # If `start` is reachable from `end`, adding an edge from `start` to `end` would create a cycle.
        for node in self.dfs(end):
            if node == start:
                raise Exception("Adding this edge would create a cycle.")
        # If no cycle is found, it's safe to add the edge.
        super().add_edge(start, end)
