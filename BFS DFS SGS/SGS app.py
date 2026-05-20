from collections import deque

def simple_graph_search(graph, start, goal):
    frontier = deque([start])
    explored = set()

    while frontier:
        state = frontier.popleft()

        if state == goal:
            print("Target reached:", state)
            return

        explored.add(state)

        for action in graph[state]:
            if action not in explored and action not in frontier:
                frontier.append(action)

    print("Target not found")

# Robot environment
rooms = {
    'Room1': ['Room2', 'Room3'],
    'Room2': ['Room4'],
    'Room3': [],
    'Room4': ['Target'],
    'Target': []
}

simple_graph_search(rooms, 'Room1', 'Target')
