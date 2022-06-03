# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here

        "*** YOUR CODE HERE ***"
        # Citations:
        # This website was useful in figuring out what I was actually calculating for V, Q, and general layout:
        # https://medium.com/@curiousily/solving-an-mdp-with-q-learning-from-scratch-deep-reinforcement-learning-for-hackers-part-1-45d1d360c120
        #
        # w3 Schools was used for python syntax and functions:
        # https://www.w3schools.com/python
        #
        # To figure out a nifty way of getting the max of a list of tuples I used this link:
        #https://www.geeksforgeeks.org/python-get-first-element-with-maximum-value-in-list-of-tuples/#:~:text=In%20Python%2C%20we%20can%20bind,value%20of%20other%20tuple%20indexes.
        # Honestly didn't expect this to work but it did

        # So the learningAgents class says to return the Q value from this function, to go about doing this we have to
        # find the max(Q(s', a))

        mdp = self.mdp
        iterations = self.iterations
        discount = self.discount
        states = mdp.getStates()
        # print(type(values))    I'm not sure what a counter is but I'm about to find out

        # The loop structure goes as follows: iterations(states(actions))) but I'm not quite sure how to iterate through
        # all of the iterations yet since the iterations is zero in the autograder

        for iteration in range(iterations):
            newValues = self.values.copy()
            for state in states:
                actions = mdp.getPossibleActions(state)
                Q = []
                if len(actions) == 0:   # This is sloppy practice but I kept taking the max of Q while it was empty
                    Q = []
                else:                   # made sure this only computes when there are possible actions
                    for action in actions:
                        Q.append(self.computeQValueFromValues(state, action))   # add new Q value
                    newValues[state] = max(Q)
            self.values = newValues




    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # For this function we only have to calculate the sum(Q(s,a) = T(s, a, s') * [R(s, a, s') + discount * V(s')]
        mdp = self.mdp
        Q = 0.0
        transition = mdp.getTransitionStatesAndProbs(state, action)         # next state and probability of next state

        for newState in transition:
            reward = mdp.getReward(state, action, newState)                         # R(s, a, s')
            Q += newState[1]*(reward + self.discount*self.getValue(newState[0]))
            # sum(Q(s,a) = T(s, a, s') * [R(s, a, s') + discount * V(s')]
        return Q

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        from operator import itemgetter
        mdp = self.mdp
        actions = []
        if len(mdp.getPossibleActions(state)) == 0:
            return None         # in case there are no legal actions, return None data type
        for action in mdp.getPossibleActions(state):
            actions.append((action, self.computeQValueFromValues(state, action)))
        return max(actions, key=itemgetter(1))[0]       # I thought I'd try something new for getting the max, I cited
                                                        # in problem one
    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):

        "*** YOUR CODE HERE ***"
        # this problem was a test of my patience
        mdp = self.mdp
        iterations = self.iterations
        states = mdp.getStates()

        for iteration in range(iterations):
            state = states[iteration % len(states)]     # index states starting with 0 % len(states) = 0
            actions = mdp.getPossibleActions(state)     # end by indexing iterations % len(states) = ?
            Q = []                                      # setup Q list to get max Q value
            if len(actions) == 0:                       # this is just to prevent max(empty list)
                Q = []  # meaningless but I have to put something here
            elif mdp.isTerminal(state):                 # this is to prevent expanding a terminal state
                Q = []  # meaningless but I have to put something here
            else:
                for action in actions:
                    Q.append(self.computeQValueFromValues(state, action))
                self.values[state] = max(Q)             # only update the state from this iteration'


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        from operator import itemgetter
        mdp = self.mdp
        values = self.values
        discount = self.discount
        iterations = self.iterations
        theta = self.theta
        states = mdp.getStates()

        # step one: compute predecessors
        predecessors = {}
        for state in states:
            predecessors = self.computePredecessors(state, predecessors) # really regret using such a large variable name
        # originally planned on creating more functions to clean this up but got carried away with the logic
        # step two: initialize priority queue
        prioQueue = util.PriorityQueue()

        # step three: fill priority queue with Q values in a very specific way
        # first we can use some of what we learned in problem one to fill a values list
        for state in states:
            qValues = []
            highQ = 0.0     # so this resets for every state
            diff = 0.0      # this also
            for action in mdp.getPossibleActions(state):
                qValues.append((action, self.computeQValueFromValues(state, action)))
                # once this is full with actions from a state and the Q values
                # we can compare to figure out what goes in the priority queue

            if not mdp.isTerminal(state):
                highQ = max(qValues, key=itemgetter(1))[1]
                diff = abs(values[state] - highQ)
                prioQueue.update(state, -diff)

        # now that priority queue is filled made we can start iterations
        # I just followed to given tasks on the Project document and added some print statements to see what was
        # going on for the rest of this problem
        # not sure why or how all this works but I do know it's similar to Astar search and it uses that to only update
        # values that are likely to change the policy
        # this also reminds me of alpha beta pruning as well

        for iteration in range(self.iterations):
            if prioQueue.isEmpty():
                return
            current = prioQueue.pop()

            if not mdp.isTerminal(current):
                newQ = []
                for action in mdp.getPossibleActions(current):
                    newQ.append(self.computeQValueFromValues(current, action))
                values[current] = max(newQ)

            for p in predecessors:
                newHighQ =[]
                for action in mdp.getPossibleActions(p):
                    newHighQ.append(self.computeQValueFromValues(p, action))

                diff = abs(values[p] - max(newHighQ))       # this gave me some trouble, I was accidentally adding lists
                if diff > theta:                            # to values instead of floats, took me forever to find
                    prioQueue.update(p, -diff)



    def computePredecessors(self, state, predecessors):
        mdp = self.mdp

        # compute predecessors of a given state, return predecessors
        # wanted to use some weird inheritance but I couldn't figure out how to do it

        if not mdp.isTerminal(state):
            for action in mdp.getPossibleActions(state):
                transitions = mdp.getTransitionStatesAndProbs(state, action)
                for transition in transitions:
                    if transition[1] != 1:
                        predecessors[transition[0]] = state

        return predecessors


