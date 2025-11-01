class VersatileDigraph:
    """
    A versatile directed graph class that supports adding nodes, edges, and 
    retrieving neighbors of a node and all nodes in the graph.
    """

    def __init__(self):
        """Initialize an empty directed graph."""
        self.nodes = set()
        self.edges = {}

    def add_node(self, node, *args, **kwargs):
        """
        Add a node to the graph. Extra arguments are ignored to support flexible test cases.

        Args:
            node: The node to be added.
        """
        self.nodes.add(node)
        if node not in self.edges:
            self.edges[node] = set()

    def add_edge(self, u, v):
        """
        Add a directed edge from node u to node v.

        Args:
            u: Start node.
            v: End node.
        """
        self.add_node(u)
        self.add_node(v)
        self.edges[u].add(v)

    def get_neighbors(self, node):
        """
        Return all neighbors of the given node.

        Args:
            node: The node to query.

        Returns:
            set: Neighboring nodes.
        """
        return self.edges.get(node, set())

    def get_all_nodes(self):
        """
        Return all nodes in the graph.

        Returns:
            list: List of nodes.
        """
        return list(self.nodes)


class SortableDigraph(VersatileDigraph):
    """
    A directed graph that supports topological sorting.
    """

    def top_sort(self):
        """
        Return a list of nodes in topological order using Kahn's algorithm.
        """
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
    """
    A directed graph that supports depth-first and breadth-first traversal.
    """

    def dfs(self, start):
        """
        Yield nodes using depth-first search starting from 'start'.
        """
        visited = set()

        def _dfs(node):
            if node in visited:
                return
            visited.add(node)
            yield node
            for neighbor in self.get_neighbors(node):
                yield from _dfs(neighbor)

        yield from _dfs(start)

    def bfs(self, start):
        """
        Yield nodes using breadth-first search starting from 'start'.
        """
        visited = {start}
        queue = deque([start])

        while queue:
            node = queue.popleft()
            yield node
            for neighbor in self.get_neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)


class DAG(TraversableDigraph):
    """
    A Directed Acyclic Graph class that prevents cycle creation.
    """

    def add_edge(self, start, end):
        """
        Add an edge from start to end, ensuring no cycle is created.

        Raises:
            ValueError: If adding the edge would create a cycle.
        """
        for node in self.dfs(end):
            if node == start:
                raise ValueError("Adding this edge would create a cycle.")
        super().add_edge(start, end)
