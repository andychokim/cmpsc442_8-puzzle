import math

input = open("input.txt", "r").read().split(",")
moves = ["D","U","R","L"]
goalState = ["_","1","2","3","4","5","6","7","8"]

def move_left(state, emptyIndex, movingNumber):
    tempState = state.copy()
    tempState[emptyIndex] = movingNumber
    tempState[emptyIndex - 1] = "_"
    return tempState

def move_right(state, emptyIndex, movingNumber):
    tempState = state.copy()
    tempState[emptyIndex] = movingNumber
    tempState[emptyIndex + 1] = "_"
    return tempState

def move_up(state, emptyIndex, movingNumber):
    tempState = state.copy()
    tempState[emptyIndex] = movingNumber
    tempState[emptyIndex - 3] = "_"
    return tempState

def move_down(state, emptyIndex, movingNumber):
    tempState = state.copy()
    tempState[emptyIndex] = movingNumber
    tempState[emptyIndex + 3] = "_"
    return tempState

def manhattan_heuristic(state):
    distance = 0
    for i in state:
        if i == "_":
            continue
        currentCoordinate = (state.index(i) // 3, state.index(i) % 3)
        goalCoordinate = (int(i) // 3, int(i) % 3)
        distance = distance + (abs(goalCoordinate[0] - currentCoordinate[0])) + (abs(goalCoordinate[1] - currentCoordinate[1]))
    return distance

def euclidian_heuristic(state):
    distance = 0
    for i in state:
        if i == "_":
            continue
        currentCoordinate = (state.index(i) // 3, state.index(i) % 3)
        goalCoordinate = (int(i) // 3, int(i) % 3)
        a = abs(goalCoordinate[0] - currentCoordinate[0])
        b = abs(goalCoordinate[1] - currentCoordinate[1])
        distance = distance + math.sqrt(a**2 + b**2)
    return distance


def q1_DFS(initialState):
    stack = [(initialState, [])]
    visited = set()
    nodeCount = 0
    
    #start of the algorithm
    while stack:
        # print("stack")
        # for i in stack:
        #     print(i)
        state, path = stack.pop(0)
        # print("state", state)
        # print("nodeCount", nodeCount)
        if (state) == goalState:
            return path
        
        childrenStack = []
        emptySpotIndex = state.index("_")
        visited.add(tuple(state))
        nodeCount = nodeCount + 1

        for move in moves:
            if ((move == "D") and (emptySpotIndex not in (6, 7, 8))):
                movingNumber = state[emptySpotIndex + 3]
                nextState = move_down(state, emptySpotIndex, movingNumber)
                if (tuple(nextState) not in visited):
                    childrenStack.append((nextState, "".join(path) + (movingNumber + "U")))
                continue

            if ((move == "U") and (emptySpotIndex not in (0, 1, 2))):
                movingNumber = state[emptySpotIndex - 3]
                nextState = move_up(state, emptySpotIndex, movingNumber)
                if (tuple(nextState) not in visited):
                    childrenStack.append((nextState, "".join(path) + (movingNumber + "D")))
                continue

            if ((move == "R") and (emptySpotIndex not in (2, 5, 8))):                
                movingNumber = state[emptySpotIndex + 1]
                nextState = move_right(state, emptySpotIndex, movingNumber)
                if (tuple(nextState) not in visited):
                    childrenStack.append((nextState, "".join(path) + (movingNumber + "L")))
                continue

            if ((move == "L") and (emptySpotIndex not in (0, 3, 6))):
                movingNumber = state[emptySpotIndex - 1]
                nextState = move_left(state, emptySpotIndex, movingNumber)
                if (tuple(nextState) not in visited):
                    childrenStack.append((nextState, "".join(path) + (movingNumber + "R")))
                continue
        stack = childrenStack + stack

    return None

def q1_BFS(initialState):
    queue = [(initialState, [])]
    visited = set()
    nodeCount = 0

    #start of the algorithm
    while queue:

        state, path = queue.pop(0)
        # print("state", state)
        # print("nodeCount", nodeCount)
        if state == goalState:
            return path

        emptySpotIndex = state.index("_")
        visited.add(tuple(state))
        nodeCount = nodeCount + 1

        for move in moves:
            if ((move == "D") & (emptySpotIndex not in (6, 7, 8))):
                movingNumber = state[emptySpotIndex + 3]
                nextState = move_down(state, emptySpotIndex, movingNumber)

                if (tuple(nextState) not in visited):
                    queue.append((nextState, "".join(path) + (movingNumber + "U")))

            if ((move == "U") & (emptySpotIndex not in (0, 1, 2))):
                movingNumber = state[emptySpotIndex - 3]
                nextState = move_up(state, emptySpotIndex, movingNumber)

                if (tuple(nextState) not in visited):
                    queue.append((nextState, "".join(path) + (movingNumber + "D")))

            if ((move == "R") & (emptySpotIndex not in (2, 5, 8))):                
                movingNumber = state[emptySpotIndex + 1]
                nextState = move_right(state, emptySpotIndex, movingNumber)

                if (tuple(nextState) not in visited):
                    queue.append((nextState, "".join(path) + (movingNumber + "L")))

            if ((move == "L") & (emptySpotIndex not in (0, 3, 6))):
                movingNumber = state[emptySpotIndex - 1]
                nextState = move_left(state, emptySpotIndex, movingNumber)

                if (tuple(nextState) not in visited):
                    queue.append((nextState, "".join(path) + (movingNumber + "R")))
                    
    return None

def q1_UCS(initialState):
    prioQueue = [(initialState, [], 0)]
    lowestCostQueue = 0
    visited = set()
    nodeCount = 0

    #start of the algorithm
    while prioQueue:

        tempLowestCost = prioQueue[0][2]
        for queue in prioQueue:
            if queue[2] < tempLowestCost:
                tempLowestCost = queue[2]
                lowestCostQueue = prioQueue.index(queue)

        state, path, cost = prioQueue.pop(lowestCostQueue)
        # print("state", state, "cost", cost)
        # print("nodeCount", nodeCount)
        if state == goalState:
            return path
        nodeCount = nodeCount + 1

        emptySpotIndex = state.index("_")
        visited.add(tuple(state))

        for move in moves:
            if ((move == "D") & (emptySpotIndex not in (6, 7, 8))):
                movingNumber = state[emptySpotIndex + 3]
                tempState = move_down(state, emptySpotIndex, movingNumber)

                if (tuple(tempState) not in visited):
                    prioQueue.append((tempState, ("".join(path) + (movingNumber + "U")), (cost + 1)))

            if ((move == "U") & (emptySpotIndex not in (0, 1, 2))):
                movingNumber = state[emptySpotIndex - 3]
                tempState = move_up(state, emptySpotIndex, movingNumber)

                if (tuple(tempState) not in visited):
                    prioQueue.append((tempState, ("".join(path) + (movingNumber + "D")), (cost + 1)))

            if ((move == "R") & (emptySpotIndex not in (2, 5, 8))):                
                movingNumber = state[emptySpotIndex + 1]
                tempState = move_right(state, emptySpotIndex, movingNumber)

                if (tuple(tempState) not in visited):
                    prioQueue.append((tempState, ("".join(path) + (movingNumber + "L")), (cost + 1)))

            if ((move == "L") & (emptySpotIndex not in (0, 3, 6))):
                movingNumber = state[emptySpotIndex - 1]
                tempState = move_left(state, emptySpotIndex, movingNumber)

                if (tuple(tempState) not in visited):
                    prioQueue.append((tempState, ("".join(path) + (movingNumber + "R")), (cost + 1)))

    return None

def q1_Astar_Manhattan(initialState):
    queue = [(initialState, [], manhattan_heuristic(initialState))]
    shortestQueue = 0
    visited = set()
    nodeCount = 0

    #start of the algorithm
    while queue:

        shortestDistance = queue[0][2]
        for i in queue:
            if i[2] < shortestDistance:
                shortestDistance = i[2]
                shortestQueue = queue.index(i)

        state, path, distance = queue.pop(shortestQueue)
        # print("state", state, "distance", distance)
        # print("nodeCount", nodeCount)
        if state == goalState:
            return path
        nodeCount = nodeCount + 1
        
        emptySpotIndex = state.index("_")
        visited.add(tuple(state))

        for move in moves:
            if ((move == "D") & (emptySpotIndex not in (6, 7, 8))):
                movingNumber = state[emptySpotIndex + 3]
                tempState = move_down(state, emptySpotIndex, movingNumber)

                if (tuple(tempState) not in visited):
                    queue.append((tempState, ("".join(path) + (movingNumber + "U")), manhattan_heuristic(tempState)))

            if ((move == "U") & (emptySpotIndex not in (0, 1, 2))):
                movingNumber = state[emptySpotIndex - 3]
                tempState = move_up(state, emptySpotIndex, movingNumber)

                if (tuple(tempState) not in visited):
                    queue.append((tempState, ("".join(path) + (movingNumber + "D")), manhattan_heuristic(tempState)))

            if ((move == "R") & (emptySpotIndex not in (2, 5, 8))):                
                movingNumber = state[emptySpotIndex + 1]
                tempState = move_right(state, emptySpotIndex, movingNumber)

                if (tuple(tempState) not in visited):
                    queue.append((tempState, ("".join(path) + (movingNumber + "L")), manhattan_heuristic(tempState)))

            if ((move == "L") & (emptySpotIndex not in (0, 3, 6))):
                movingNumber = state[emptySpotIndex - 1]
                tempState = move_left(state, emptySpotIndex, movingNumber)

                if (tuple(tempState) not in visited):
                    queue.append((tempState, ("".join(path) + (movingNumber + "R")), manhattan_heuristic(tempState)))

    return None

def q1_Astar_Euclidian(initialState):
    queue = [(initialState, [], euclidian_heuristic(initialState))]
    shortestQueue = 0
    visited = set()
    nodeCount = 0

    #start of the algorithm
    while queue:

        shortestDistance = queue[0][2]
        for i in queue:
            if i[2] < shortestDistance:
                shortestDistance = i[2]
                shortestQueue = queue.index(i)

        state, path, distance = queue.pop(shortestQueue)
        # print("state", state, "distance", distance)
        # print("nodeCount", nodeCount)
        if state == goalState:
            return path
        
        emptySpotIndex = state.index("_")
        visited.add(tuple(state))
        nodeCount = nodeCount + 1

        for move in moves:
            if ((move == "D") & (emptySpotIndex not in (6, 7, 8))):
                movingNumber = state[emptySpotIndex + 3]
                tempState = move_down(state, emptySpotIndex, movingNumber)

                if (tuple(tempState) not in visited):
                    queue.append((tempState, ("".join(path) + (movingNumber + "U")), euclidian_heuristic(tempState)))

            if ((move == "U") & (emptySpotIndex not in (0, 1, 2))):
                movingNumber = state[emptySpotIndex - 3]
                tempState = move_up(state, emptySpotIndex, movingNumber)

                if (tuple(tempState) not in visited):
                    queue.append((tempState, ("".join(path) + (movingNumber + "D")), euclidian_heuristic(tempState)))

            if ((move == "R") & (emptySpotIndex not in (2, 5, 8))):                
                movingNumber = state[emptySpotIndex + 1]
                tempState = move_right(state, emptySpotIndex, movingNumber)

                if (tuple(tempState) not in visited):
                    queue.append((tempState, ("".join(path) + (movingNumber + "L")), euclidian_heuristic(tempState)))

            if ((move == "L") & (emptySpotIndex not in (0, 3, 6))):
                movingNumber = state[emptySpotIndex - 1]
                tempState = move_left(state, emptySpotIndex, movingNumber)

                if (tuple(tempState) not in visited):
                    queue.append((tempState, ("".join(path) + (movingNumber + "R")), euclidian_heuristic(tempState)))

    return None

resultPathA = q1_DFS(input)
print("The solution of Q1.1a is:\n" + ",".join(resultPathA[i:i+2] for i in range(0, len(resultPathA), 2)), "\n")

resultPathB = q1_BFS(input)
print("The solution of Q1.1b is:\n" + ",".join(resultPathB[i:i+2] for i in range(0, len(resultPathB), 2)), "\n")

resultPathC = q1_UCS(input)
print("The solution of Q1.1c is:\n" + ",".join(resultPathC[i:i+2] for i in range(0, len(resultPathC), 2)), "\n")

resultPathD = q1_Astar_Manhattan(input)
print("The solution of Q1.1d is:\n" + ",".join(resultPathD[i:i+2] for i in range(0, len(resultPathD), 2)), "\n")

resultPathE = q1_Astar_Euclidian(input)
print("The solution of Q1.1e is:\n" + ",".join(resultPathE[i:i+2] for i in range(0, len(resultPathE), 2)), "\n")