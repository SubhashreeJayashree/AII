from collections import deque

def bfs_shortest_path(graph, start, goal):
    visited = set()
    queue = deque([(start, [start])])

    while queue:
        node, path = queue.popleft()

        if node == goal:
            return path

        if node not in visited:
            visited.add(node)

            for neighbor in graph[node]:
                queue.append((neighbor, path + [neighbor]))

    return None

# City map (Graph)
city_map = {
    'Home': ['Park', 'Mall'],
    'Park': ['School'],
    'Mall': ['Office'],
    'School': ['Hospital'],
    'Office': [],
    'Hospital': []
}

path = bfs_shortest_path(city_map, 'Home', 'Hospital')
print("Shortest Path:", path)
