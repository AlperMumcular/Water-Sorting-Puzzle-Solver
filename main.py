# Alper Mumcular
# Water Sorting Puzzle - A* Search

import time, heapq, copy  # Required libraries

start = time.time()  # Timer Start


# Modified Data Structure for A* fringe
# O(1) access to the lowest priority item
class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority, actualCost, answer):
        entry = (priority, self.count, item, actualCost, answer)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item, actualCost, answer) = heapq.heappop(self.heap)
        return item, actualCost, answer

    def isEmpty(self):
        return len(self.heap) == 0


# Read txt file
file1 = open('tubelist.txt', 'r')
Lines = file1.readlines()

# Convert txt file structure into python list (treated as a Stack)
game = tuple()

# Read each word line by line then add them to the list
for line in Lines:
    tmp = list()
    for word in line.split():  # reading each word
        if word != "_":
            tmp.append(word)
    game += (tmp,)

lenGame = len(game)  # Number of tubes

uniq = dict()  # Number of different colors
tubeHeight = 0  # height of the tubes
for x in range(0, lenGame):
    tubeHeight = max(tubeHeight, len(game[x]))
    for y in range(0, len(game[x])):
        uniq[game[x][y]] = 0


# This function finds the removable color and its count from specified tube
def remove(puzzle, tubeNo):
    tubeLen = len(puzzle[tubeNo])
    if tubeLen == 0:  # Tube is empty
        return None, False
    else:  # Tube is not empty
        count = 1
        p = tubeLen - 1
        color = puzzle[tubeNo][p]
        for i in range(p - 1, -1, -1):
            if puzzle[tubeNo][i] == color:
                count = count + 1
            else:
                break

        return color, count


# This function takes from the source tube and adds it to the destination tube
def insert(puzzle, tubeNo, color, firstTube, count):
    if count is None:  # Source tube is empty
        return False
    tubeLen = len(puzzle[tubeNo])
    if tubeLen == 0:  # Destination tube is empty
        for i in range(0, count):
            puzzle[firstTube].pop()
            puzzle[tubeNo].append(color)

        return True
    elif tubeLen == tubeHeight or puzzle[tubeNo][tubeLen - 1] != color:  # Destination tube is full or color mismatching
        return False
    else:  # Other cases
        cnt = count
        for i in range(0, tubeHeight - tubeLen):  # Fill destination tube as much as it can
            if cnt > 0:
                puzzle[firstTube].pop()
                puzzle[tubeNo].append(color)
                cnt = cnt - 1
        return True


# A function that checks whether the puzzle is solved or not
def isSolved(puzzle):
    for i in range(0, lenGame):
        tubeLen = len(puzzle[i])
        if tubeLen != tubeHeight and tubeLen != 0:  # If a tube is not empty and not full, then the game is not finished
            return False
        else:
            colorCount = len(set(puzzle[i]))
            if colorCount != 1 and tubeLen == tubeHeight:  # If the tube is full and there are more than 1 color
                return False
    return True


# This function checks a single tube is completed or not
def isFull(arr):
    if len(set(arr)) == 1 and len(arr) == tubeHeight:  # If there is exactly one color and tube is full
        return True
    return False


# This function lists all possible moves in given state
def possibleMoves(puzzle):
    possible = list()
    for i in range(0, lenGame):
        if isFull(puzzle[i]) is False:  # If the tube is full then no move needed therefore it is not possible
            for j in range(0, lenGame):
                if isFull(puzzle[j]) is False:  # If the tube is full then no move needed therefore it is not possible
                    if i != j and (len(set(puzzle[i])) == 1 and len(puzzle[j]) == 0) is False:  #unnecessary pour
                        color = remove(list(map(list, puzzle)), i)
                        if color[0] is not None:  # if it is not none then it is possible
                            if insert(list(map(list, puzzle)), j, color[0], i, color[1]) is True:
                                possible.append([i, j])
    return possible


# A function that estimates how we are close to goal state(s)
# It counts how many are there different colors according to its bottom color in each tube
# It is admissible because these colors have to be replaced.
def heuristic(puzzle):
    total = 0
    for i in range(0, lenGame):
        tubeLen = len(puzzle[i])
        if tubeLen != 0:
            color = puzzle[i][0]
            for n in range(1, tubeLen):
                if color != puzzle[i][n]:
                    color = puzzle[i][n]
                    total += 1

    return total


# Second heuristic function that checks bottom colors in each tube
# It looks the bottom colors of all tubes and counts how many similar colors are in the bottom
# It is also admissible because at least one of them has to be replaced.
def heuristic2(puzzle):
    temp = uniq.copy()
    for i in range(0, lenGame):
        if len(puzzle[i]) > 0:
            temp[puzzle[i][0]] += 1
    total = 0
    for val in temp.values():
        if val > 1:
            total += val - 1
    return total


queue = PriorityQueue()  # A* fringe data structure

heu = heuristic(game)  # Initial heuristic calls
heu2 = heuristic2(game)

queue.push(game, heu + heu2, 0, list())  # Initial game state

visited = set()  # Closed set that keeps all seen game states up to some point

# This function tries possible moves, adds all possible states into queue according to their priorities
# Priority = Heuristic1 + Heuristic2 + Cost (number of movement count made up to that state)
def Solver(puzzle, cost, answer):
    puzzle_tuple = tuple(map(tuple, puzzle))  # Convert puzzle to a tuple of tuples

    if puzzle_tuple in visited:  # If the state is visited, then skip
        return None

    visited.add(puzzle_tuple)  # If the state is not visited, make it visited

    global queue

    if isSolved(puzzle):  # Stop condition --> Winning the game
        queue = PriorityQueue()
        print(puzzle)
        return answer
    else:
        print("moveCount = " + str(len(answer)) + " puzz" + str(puzzle) + " move " + str(answer))
        for move in possibleMoves(puzzle):  # Add all possible moves
            temp = copy.deepcopy(puzzle)
            ansCopy = copy.deepcopy(answer)
            ansCopy.append("tube " + str(move[0] + 1) + " moves to tube " + str(move[1] + 1))

            color = remove(temp, move[0])
            insert(temp, move[1], color[0], move[0], color[1])

            heur = heuristic(temp)
            heur2 = heuristic2(temp)
            updatedCost = cost + 1

            queue.push(temp, heur + heur2 + updatedCost, updatedCost, ansCopy)
        return None


result = None

# If we assume there is at least one solution, then the optimal solution is guaranteed.
while queue.isEmpty() is not True:  # If queue is empty --> We won the game or There is no solution
    currPuzzle, currCost, currAnswer = queue.pop()
    result = Solver(currPuzzle, currCost, currAnswer)

if result is not None:  # Print results
    print(result)
    print("Optimal Cost: " + str(len(result)))
else:
    print("No solution")

end = time.time()
print("Run time: " + str(end - start) + " seconds")  # Show the time it takes
