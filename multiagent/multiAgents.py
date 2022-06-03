# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

# All of the work in this class was written by me, Christopher Pawlenok and Anthony DeAngelo
# sources:
#   https://www.w3schools.com/python/python_reference.asp (This is the python section, I looked up multiple things here)
#   https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/    (miniMax pseudocode)
#   https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/    (alpha-beta pseudocode)
#   https://stackoverflow.com/questions/35721636/understanding-the-minmax-pseudocode            (miniMax pseudocode)
#

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """

        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # I would also like to cite spotify.com for keeping my sanity
        foodPos = newFood.asList()  # originally I tried to convert the grid to coordinates on my own but that didn't work out so well
        foodRef = []
        ghostRef = []
        if len(foodPos) != 0:  # had to add this when the game would give me an error right before ending
            for food in foodPos:
                foodRef.append(manhattanDistance(newPos, food))
            foodDis = 10 / min(foodRef)  # we want smaller numbers for food proximity so inverse works better
        else:
            foodDis = 0                     # this is so the game actually ends
        for ghost in newGhostStates:
            ghostRef.append(manhattanDistance(newPos, ghost.getPosition()))
        if min(ghostRef) < 4:               # Only worry about the ghosts when theyre close
            ghostDis = 10 * min(ghostRef)   # when they're close, prioritize their influence on pacman
        else:
            ghostDis = min(ghostRef) * 0.2  # when they're far, minimize their influence on pacman

        print("Food:", foodDis)
        print("Ghost:", ghostDis)
        print("________________________________________________")
        return successorGameState.getScore() + (foodDis + ghostDis)
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        returnThis = self.miniMax(gameState, 0, self.index)[1]  # call miniMax for the first time
        return returnThis           # I originally had returnThis[1] and was wondering why I was getting strange actions

    # miniMax function accepts state, depth and agentNum and returns a tuple with (best eval number, associated action)
    # this is calculated at every possible move so if we use greater depth, it takes a while for pacman to make a decision
    def miniMax(self, gameState, depth, agentNum):
        if gameState.isWin() or gameState.isLose():             # first make sure the game isn't over
            return (self.evaluationFunction(gameState), "")     # I kept creating tuples inside of tuples
                                                                # so this was my fix for that
        if depth == self.depth:                                 # make sure we haven't reach max depth
            return (self.evaluationFunction(gameState), "")     # if we have, return the dreaded tuple

        if agentNum == self.index:                              # are we max?
            max = True
        else:                                                   # or are we min?
            max = False

        if agentNum == (gameState.getNumAgents() - 1):          # is it the last ghost?
            depth = depth + 1                                   # if it is, the depth increase right after
            newAgent = self.index                               # I had to make this as a temp agent because
        else:                                                   # generateSuccessor() requires the current agentNum
            newAgent = agentNum + 1

        legalActions = gameState.getLegalActions(agentNum)
        if max:
            bestNum = -99999999                 # wow, that's a really small number
            for action in legalActions:
                value = self.miniMax(gameState.generateSuccessor(agentNum, action), depth, newAgent)    # receive tuple
                if value[0] > bestNum:          # check the evaluation number in the tuple
                    best = (value[0], action)   # current max of all the evaluationFunctions
                    bestNum = value[0]          # you never know when you're going to need max eval number so store it
        if not max:
            bestNum = 99999999                  # hopefully the eval function doesn't generate a larger number
            for action in legalActions:
                value = self.miniMax(gameState.generateSuccessor(agentNum, action), depth, newAgent)
                if value[0] < bestNum:
                    best = (value[0], action)   # this tuple was the bane of my existence
                    bestNum = value[0]          # store current smallest number
        return best                             # return agent's move that is either max or min

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        returnThis = self.abMiniMax(gameState, 0, self.index, -999999999, 999999999)[1]     # pass alpha = really small
        print("Return:", returnThis)                                                        # pass beta = really big
        return returnThis

    # Same as miniMax function but we send alhpa and beta now to check if we can break the loop iterating thru actions
    def abMiniMax(self, gameState, depth, agentNum, alpha, beta):
        if gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState), "")

        if depth == self.depth:
            return (self.evaluationFunction(gameState), "")

        if agentNum == self.index:
            maxi = True
        else:
            maxi = False

        if agentNum == (gameState.getNumAgents() - 1):
            depth = depth + 1
            newAgent = self.index
        else:
            newAgent = agentNum + 1

        legalActions = gameState.getLegalActions(agentNum)
        if maxi:            # Max agent
            bestNum = -99999999
            for action in legalActions:
                value = self.abMiniMax(gameState.generateSuccessor(agentNum, action), depth, newAgent, alpha, beta)
                if value[0] > bestNum:
                    best = (value[0], action)
                    bestNum = value[0]
                if value[0] > beta:                     # If current value is better than best min
                    return best                         # return current value and action
                alpha = max([value[0], alpha])          # else change alpha if current value > alpha


        if not maxi:        # Min agent
            bestNum = 99999999
            for action in legalActions:
                value = self.abMiniMax(gameState.generateSuccessor(agentNum, action), depth, newAgent, alpha, beta)
                if value[0] < bestNum:
                    best = (value[0], action)
                    bestNum = value[0]
                if value[0] < alpha:                    # same as max but if current value is better than best max
                    return best                         # return current value
                beta = min([value[0], beta])            # else check if current value is better than beta
        return best


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        returnThis = self.expectiMax(gameState, 0, self.index)[1]
        return returnThis
    # same function as in miniMax with a small tweak to the min Agents that finds the average of the minAgent's actions
    # still returns a tuple of (eval number, associated move)
    def expectiMax(self, gameState, depth, agentNum):
        if gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState), "")

        if depth == self.depth:
            return (self.evaluationFunction(gameState), "")

        if agentNum == self.index:
            max = True
        else:
            max = False

        if agentNum == (gameState.getNumAgents() - 1):
            depth = depth + 1
            newAgent = self.index
        else:
            newAgent = agentNum + 1

        legalActions = gameState.getLegalActions(agentNum)
        if max:
            bestNum = -99999999
            for action in legalActions:
                value = self.expectiMax(gameState.generateSuccessor(agentNum, action), depth, newAgent)
                if value[0] > bestNum:
                    best = (value[0], action)
                    bestNum = value[0]
        if not max:
            avgNum = 0
            for action in legalActions:
                value = self.expectiMax(gameState.generateSuccessor(agentNum, action), depth, newAgent)
                avgNum += (value[0] / len(legalActions))        # find the average of the random agents
                best = (avgNum, action)                         # I just left this as best so we return the right value
        return best

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: Accepts a game state and evaluates the state based on food, ghost and capsule location
    """
    pacPos = currentGameState.getPacmanPosition()   # I can't remember if I actually used all these
    foodList = currentGameState.getFood().asList()  # just some helpful info about the game state
    ghostPos = currentGameState.getGhostStates()    # changing some of the values in this function yields funny results
    posCapsules = currentGameState.getCapsules()    # Yes, I'm aware this function is a mess but it's a beautiful mess
    numFood = len(foodList)

    foodDis = []        # list to store food distances
    ghostDis = []       # list to store ghost distances
    capsuleDis = []     # list to store capsule distances
    scaredDis = []      # list to store scaredGhost distances

    if numFood != 0:                                # kept running out out of food and throwing errors
        for food in foodList:                       # iterate through food
            dis = manhattanDistance(pacPos, food)   # find distance from pacman to food
            foodDis.append(dis)
        if min(foodDis) < 4:                        # I had to gradient food like I did with my ghosts in reflexAgent
            foodWeight = float(1/min(foodDis))      # when food is really close, get or suffer the consequences
        elif min(foodDis) < 8:                  # when it's kind of close, other things might be more important in life
            foodWeight = float(0.5/min(foodDis))
        else:
            foodWeight = float(0.1/min(foodDis))    # when it's far away, know it's there but eating ghosts fares better
        foodWeightAlt = 10/(sum(foodDis) / len(foodDis))    # so we don't leave any food on the board
    else:
        foodWeight = 0          # when there's no food left on the board, dontCrash.exe
        foodWeightAlt = 0       # pleaseDontCrash.png

    if len(ghostPos) != 0:                                      # ghosts have 2 states, feared and not feared
        for ghost in ghostPos:                                  # iterate through ghosts
            dis = manhattanDistance(pacPos, ghost.getPosition())    # distance to ghost
            if ghost.scaredTimer:                                   # if ghost is scared
                scaredDis.append(dis)                               # sick em
                ghostWeight = float(100/min(scaredDis))
            else:                                                   # if ghost isn't scared
                ghostDis.append(dis)                                # run away
                if min(ghostDis) < 5:                               # gradient again because pacman kept getting stuck
                    ghostWeight = float(min(ghostDis))
                else:
                    ghostWeight = 0                                 # if ghost is far, don't worry about him

    if len(posCapsules) != 0:                                       # dontCrash.jpg
        for capsule in posCapsules:                                 # we can only iterate when there's multiple capsules
            dis = manhattanDistance(pacPos, capsule)
            capsuleDis.append(dis)
            capWeight = float(1/min(capsuleDis))
    elif len(posCapsules) == 1:                                     # alsoDontCrash.txt
        capWeight = float(1/manhattanDistance(pacPos, posCapsules))
    else:
        capWeight = 0

    totalEval = 0.8*foodWeight + foodWeightAlt + 0.3*ghostWeight + 7.0*capWeight + currentGameState.getScore()
    # the weights are decent, I'm sure if I dedicated my life to optimizing pacman I could have came up with some better
    # weights for these but they score fairly well and run in decent time even though he gets a stuck sometimes

    return totalEval    # return the mess I just created

# Abbreviation
better = betterEvaluationFunction
