from copy import deepcopy
from colorama import Fore, Back, Style

# desenha quebra-cabeça no terminal
leftDownAngle = '\u2514'
rightDownAngle = '\u2518'
rightUpAngle = '\u2510'
leftUpAngle = '\u250C'
middleJunction = '\u253C'
topJunction = '\u252C'
bottomJunction = '\u2534'
rightJunction = '\u2524'
leftJunction = '\u251C'
bar = Style.BRIGHT + Fore.YELLOW + '\u2502' + Fore.RESET + Style.RESET_ALL
dash = '\u2500'
firstLine = Style.BRIGHT + Fore.YELLOW + leftUpAngle + dash + dash + dash + topJunction + dash + dash + dash + topJunction + dash + dash + dash + rightUpAngle + Fore.RESET + Style.RESET_ALL
middleLine = Style.BRIGHT + Fore.YELLOW + leftJunction + dash + dash + dash + middleJunction + dash + dash + dash + middleJunction + dash + dash + dash + rightJunction + Fore.RESET + Style.RESET_ALL
lastLine = Style.BRIGHT + Fore.YELLOW + leftDownAngle + dash + dash + dash + bottomJunction + dash + dash + dash + bottomJunction + dash + dash + dash + rightDownAngle + Fore.RESET + Style.RESET_ALL

# matriz de direção
DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}

# matriz final
END_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# exibe o puzzle
def printPuzzle(array):
    print(firstLine)
    for a in range(len(array)):
        for i in array[a]:
            if i == 0:
                print(bar, Back.RED + ' ' + Back.RESET, end=' ')
            else:
                print(bar, i, end=' ')
        print(bar)
        if a == 2:
            print(lastLine)
        else:
            print(middleLine)

# Node que armazena cada estado do quebra-cabeça
class Node:
    def __init__(self, currentNode, previousNode, g, h, dir):
        self.currentNode = currentNode
        self.previousNode = previousNode
        self.g = g
        self.h = h
        self.dir = dir

    def f(self):
        return self.g + self.h

def getPos(currentState, element):
    for row in range(len(currentState)):
        if element in currentState[row]:
            return (row, currentState[row].index(element))

# cálcula a distância
def euclidianCost(currentState):
    cost = 0
    for row in range(len(currentState)):
        for col in range(len(currentState[0])):
            pos = getPos(END_STATE, currentState[row][col])
            cost += abs(row - pos[0]) + abs(col - pos[1])
    return cost

# retorna os nodes adjacentes
def getAdjNode(node):
    listNode = []
    emptyPos = getPos(node.currentNode, 0)

    for dir in DIRECTIONS.keys():
        newPos = (emptyPos[0] + DIRECTIONS[dir][0], emptyPos[1] + DIRECTIONS[dir][1])
        if 0 <= newPos[0] < len(node.currentNode) and 0 <= newPos[1] < len(node.currentNode[0]):
            newState = deepcopy(node.currentNode)
            newState[emptyPos[0]][emptyPos[1]] = node.currentNode[newPos[0]][newPos[1]]
            newState[newPos[0]][newPos[1]] = 0
            listNode.append(Node(newState, node.currentNode, node.g + 1, euclidianCost(newState), dir))

    return listNode

# obtêm o melhor node disponível entre os nodes
def getBestNode(openSet):
    firstIter = True

    for node in openSet.values():
        if firstIter or node.f() < bestF:
            firstIter = False
            bestNode = node
            bestF = bestNode.f()
    return bestNode

# cria o array para a função printPuzzle
def buildPath(closedSet):
    node = closedSet[str(END_STATE)]
    branch = list()

    while node.dir:
        branch.append({ 'dir': node.dir, 'node': node.currentNode })
        node = closedSet[str(node.previousNode)]
    
    branch.append({ 'dir': '', 'node': node.currentNode })
    branch.reverse()

    return branch

def main(puzzle):
    openSet = { str(puzzle): Node(puzzle, puzzle, 0, euclidianCost(puzzle), "") }
    closedSet = {}

    while True:
        testNode = getBestNode(openSet)
        closedSet[str(testNode.currentNode)] = testNode

        if testNode.currentNode == END_STATE:
            return buildPath(closedSet)

        adjNode = getAdjNode(testNode)
        for node in adjNode:
            if str(node.currentNode) in closedSet.keys() or str(node.currentNode) in openSet.keys() and openSet[str(node.currentNode)].f() < node.f():
                continue
            openSet[str(node.currentNode)] = node

        del openSet[str(testNode.currentNode)]

if __name__ == '__main__':
    print('digite o estado inicial da matriz exemplo: 8 0 6 5 4 7 2 3 1')
    initialState = list(map(lambda x: int(x), input().split(' ')))

    puzzle = main([
        [initialState[0], initialState[1], initialState[2]],
        [initialState[3], initialState[4], initialState[5]],
        [initialState[6], initialState[7], initialState[8]]
    ])

    print()
    print(dash + dash + rightJunction, "Estado inicial", leftJunction + dash + dash)
    for puzz in puzzle:
        printPuzzle(puzz['node'])
        print()
    print('\n\n', dash + dash + rightJunction, 'total de passos: ', len(puzzle) - 1, leftJunction + dash + dash, '\n\n\n')
    