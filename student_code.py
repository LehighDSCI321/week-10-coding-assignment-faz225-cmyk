"""
This module implements a sortable directed graph class SortableDigraph, which 
inherits from the versatile directed graph class VersatileDigraph. It provides 
functionality for managing nodes, edges, and performing topological sorting.
"""

from collections import deque


class VersatileDigraph:
    """
    A versatile directed graph class that supports adding nodes, edges, and 
    retrieving neighbors of a node and all nodes in the graph.
    
    Attributes:
        nodes (set): A set containing all nodes in the graph.
        edges (dict): An adjacency list where keys are nodes and values are 
            sets of neighboring nodes pointed to by the key node.
    """

    def __init__(self):
        """Initialize an empty directed graph."""
        self.nodes = set()
        self.edges = {}  # Key: node, Value: set of neighboring nodes

    def add_node(self, node):
        """
        Add a node to the graph (no duplicate addition if the node already exists).
        
        Args:
            node: The node to be added (must be a hashable type).
        """
        self.nodes.add(node)
        if node not in self.edges:
            self.edges[node] = set()

    def add_edge(self, u, v):
        """
        Add a directed edge from node u to node v (automatically adds nodes 
        that do not exist).
        
        Args:
            u: The start node of the edge.
            v: The end node of the edge.
        """
        self.add_node(u)  # Ensure the start node exists
        self.add_node(v)  # Ensure the end node exists
        self.edges[u].add(v)  # Add the edge u->v

    def get_neighbors(self, node):
        """
        Retrieve all neighbors of a specified node (i.e., nodes pointed to by 
        the given node).
        
        Args:
            node: The node to query for neighbors.
            
        Returns:
            set: A set of the node's neighbors (returns an empty set if the 
                node does not exist).
        """
        return self.edges.get(node, set())

    def get_all_nodes(self):
        """
        Retrieve a list of all nodes in the graph.
        
        Returns:
            list: A list containing all nodes in the graph.
        """
        return list(self.nodes)


class SortableDigraph(VersatileDigraph):
    """
    A sortable directed graph class that inherits from VersatileDigraph. It 
    adds a top_sort method to perform topological sorting on directed acyclic 
    graphs (DAGs).
    """

    def top_sort(self):
        """
        Perform topological sorting on the graph using Kahn's algorithm (only 
        applicable to DAGs).
        
        Algorithm steps:
            1. Calculate the in-degree (number of incoming edges) for each node.
            2. Initialize a queue with all nodes having an in-degree of 0.
            3. Process the queue in a loop:
               - Dequeue a node and add it to the topological order result.
               - Decrement the in-degree of its neighbors; if a neighbor's 
                 in-degree becomes 0, enqueue it.
               
        Returns:
            list: A list of nodes in topological order (if the graph contains 
                a cycle, the result length will be less than the total number 
                of nodes).
        """
        # Calculate in-degree for each node (using dictionary literal instead of dict())
        in_degree = {n: 0 for n in self.nodes}
        for current_node in self.nodes:  # Rename to current_node to avoid conflict
            for neighbor in self.get_neighbors(current_node):
                in_degree[neighbor] += 1

        # Initialize queue with nodes having in-degree 0
        queue = deque()
        for n in self.nodes:  # Rename to n to avoid conflict
            if in_degree[n] == 0:
                queue.append(n)

        top_order = []
        while queue:
            current = queue.popleft()
            top_order.append(current)
            # Process all neighbors of the current node, decrement their in-degree
            for neighbor in self.get_neighbors(current):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return top_order

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
