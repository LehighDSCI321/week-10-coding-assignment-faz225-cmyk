from collections import deque

class SortableDigraph:
    """
    Base class for a simple directed graph.
    It maintains a dictionary where each vertex maps to a list of its neighbors.
    """
    def __init__(self):
        self.graph = {}  # {vertex: [list of neighbors]}

    def add_vertex(self, v):
        """Add a vertex to the graph if it doesn't exist."""
        if v not in self.graph:
            self.graph[v] = []

    def add_edge(self, src, dst):
        """
        Add a directed edge from src to dst.
        Automatically adds the vertices if they don't already exist.
        """
        self.add_vertex(src)
        self.add_vertex(dst)
        self.graph[src].append(dst)

    def neighbors(self, v):
        """Return the list of neighbors for a given vertex."""
        return self.graph.get(v, [])

    def __contains__(self, v):
        return v in self.graph

    def __repr__(self):
        return f"{self.graph}"


# ============================================================
# TraversableDigraph: adds DFS and BFS traversal capabilities
# ============================================================
class TraversableDigraph(SortableDigraph):
    """
    A directed graph that supports traversal methods:
    - Depth-First Search (DFS)
    - Breadth-First Search (BFS)
    """

    def dfs(self, start, visited=None):
        """
        Depth-First Search traversal implemented as a recursive generator.
        Yields each node as it is visited.
        """
        if visited is None:
            visited = set()
        visited.add(start)
        yield start  # Visit the current node
        for neighbor in self.neighbors(start):
            if neighbor not in visited:
                yield from self.dfs(neighbor, visited)

    def bfs(self, start):
        """
        Breadth-First Search traversal using a queue (deque).
        Yields nodes level by level.
        """
        visited = set()
        queue = deque([start])
        visited.add(start)

        while queue:
            node = queue.popleft()
            yield node  # Yield the next node
            for neighbor in self.neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)


# ============================================================
# DAG: Directed Acyclic Graph (inherits from TraversableDigraph)
# Prevents creation of cycles when adding edges
# ============================================================
class DAG(TraversableDigraph):
    """
    A Directed Acyclic Graph (DAG).
    Overrides add_edge() to ensure that no directed cycles are created.
    """

    def add_edge(self, src, dst):
        """
        Add a directed edge only if it does not create a cycle.
        Raises ValueError if adding the edge would form a cycle.
        """
        if self._has_path(dst, src):
            raise ValueError(f"Adding edge {src} -> {dst} would create a cycle.")
        super().add_edge(src, dst)

    def _has_path(self, start, target, visited=None):
        """
        Helper method to check if there is a path from start to target.
        Used internally to detect potential cycles.
        """
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
# Example usage and testing
# ============================================================
if __name__ == "__main__":
    # Build a sample DAG (clothing order example)
    g = DAG()
    g.add_edge("shirt", "vest")
    g.add_edge("shirt", "pants")
    g.add_edge("shirt", "tie")
    g.add_edge("vest", "jacket")
    g.add_edge("pants", "shoe")
    g.add_edge("pants", "belt")
    g.add_edge("belt", "jacket")
    g.add_edge("socks", "shoes")
    g.add_edge("vest", "jacket")
    g.add_edge("tie", "jacket")
    print("Graph structure:", g.graph)

    print("\nDFS traversal starting from 'shirt':")
    print(list(g.dfs("shirt")))

    print("\nBFS traversal starting from 'shirt':")
    print(list(g.bfs("shirt")))

    # Attempt to add an edge that would create a cycle
    try:
        g.add_edge("jacket", "shirt")
    except ValueError as e:
        print("\n⚠️ Cycle detected:", e)
