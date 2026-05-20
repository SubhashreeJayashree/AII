from collections import deque

def simple_graph_search(graph, start, goal):
    visited = set()
    frontier = deque([start])

    while frontier:
        node = frontier.popleft()

        if node == goal:
            print("Goal found:", node)
            return

        if node not in visited:
            print("Visiting:", node)
            visited.add(node)

            for neighbor in graph[node]:
                if neighbor not in visited:
                    frontier.append(neighbor)

    print("Goal not found")

# Example graph
graph = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['E'],
    'D': ['G'],
    'E': [],
    'G': []
}

simple_graph_search(graph, 'A', 'G')
