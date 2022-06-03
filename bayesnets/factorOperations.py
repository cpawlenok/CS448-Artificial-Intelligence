# factorOperations.py
# -------------------
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


from bayesNet import Factor
import operator as op
import util
import functools

def joinFactorsByVariableWithCallTracking(callTrackingList=None):


    def joinFactorsByVariable(factors, joinVariable):
        """
        Input factors is a list of factors.
        Input joinVariable is the variable to join on.

        This function performs a check that the variable that is being joined on 
        appears as an unconditioned variable in only one of the input factors.

        Then, it calls your joinFactors on all of the factors in factors that 
        contain that variable.

        Returns a tuple of 
        (factors not joined, resulting factor from joinFactors)
        """

        if not (callTrackingList is None):
            callTrackingList.append(('join', joinVariable))

        currentFactorsToJoin =    [factor for factor in factors if joinVariable in factor.variablesSet()]
        currentFactorsNotToJoin = [factor for factor in factors if joinVariable not in factor.variablesSet()]

        # typecheck portion
        numVariableOnLeft = len([factor for factor in currentFactorsToJoin if joinVariable in factor.unconditionedVariables()])
        if numVariableOnLeft > 1:
            print("Factor failed joinFactorsByVariable typecheck: ", factor)
            raise ValueError("The joinBy variable can only appear in one factor as an \nunconditioned variable. \n" +  
                               "joinVariable: " + str(joinVariable) + "\n" +
                               ", ".join(map(str, [factor.unconditionedVariables() for factor in currentFactorsToJoin])))
        
        joinedFactor = joinFactors(currentFactorsToJoin)
        return currentFactorsNotToJoin, joinedFactor

    return joinFactorsByVariable

joinFactorsByVariable = joinFactorsByVariableWithCallTracking()


def joinFactors(factors):
    """
    Question 3: Your join implementation 

    Input factors is a list of factors.  
    
    You should calculate the set of unconditioned variables and conditioned 
    variables for the join of those factors.

    Return a new factor that has those variables and whose probability entries 
    are product of the corresponding rows of the input factors.

    You may assume that the variableDomainsDict for all the input 
    factors are the same, since they come from the same BayesNet.

    joinFactors will only allow unconditionedVariables to appear in 
    one input factor (so their join is well defined).

    Hint: Factor methods that take an assignmentDict as input 
    (such as getProbability and setProbability) can handle 
    assignmentDicts that assign more variables than are in that factor.

    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """

    # typecheck portion
    setsOfUnconditioned = [set(factor.unconditionedVariables()) for factor in factors]
    if len(factors) > 1:
        intersect = functools.reduce(lambda x, y: x & y, setsOfUnconditioned)
        if len(intersect) > 0:
            print("Factor failed joinFactors typecheck: ", factor)
            raise ValueError("unconditionedVariables can only appear in one factor. \n"
                    + "unconditionedVariables: " + str(intersect) + 
                    "\nappear in more than one input factor.\n" + 
                    "Input factors: \n" +
                    "\n".join(map(str, factors)))


    "*** YOUR CODE HERE ***"
    uncondition = set()
    condition = set()

    #iterate through factors to get conditioned and unconditioned variables
    for currentFactor in factors:
        uncondition = uncondition.union(currentFactor.unconditionedVariables()) #unconditioned variables in current factor
        condition = condition.union(currentFactor.conditionedVariables())   #conditioned varaibles in current factor
    dictEntries = currentFactor.variableDomainsDict()           # assume this is the same for all factors so we can
                                                                # use the very last factor of the iteration
    #   list all unconditioned variables
    #   realized that union is a thing so I
    #   didn't have to check for duplicates
    #   but this is already here so it's staying
    #   I redact the previous comment, I needed to use sets for this because I was getting an unhashable type error

    for var in uncondition:         # got the error message informing that there were copies in condition
        if var in condition:
            condition.remove(var)   # so remove all copies from condition

    #   generate factor, this took forever to figure out that I need to generate the factor before I can get all
    #   possible assignments and use them to calculate probabilities of the new table

    newTable = Factor(uncondition, condition, dictEntries)              # create new table
    newTableAssignments = newTable.getAllPossibleAssignmentDicts()      # get all possible assignments for new table

    for entry in newTableAssignments:
        entryProbability = 1.0             # need this to reset entry probability for each individual possible dict entry
        for factor in factors:             # iterate through all factors
            entryProbability = entryProbability*factor.getProbability(entry)    # use factors probabilities to get
        newTable.setProbability(entry, entryProbability)                        # newTable's probabilities

    return newTable
    #   get probability for the new factor
    #   probabilty will be the sum of all probabilites

    "*** END YOUR CODE HERE ***"


def eliminateWithCallTracking(callTrackingList=None):

    def eliminate(factor, eliminationVariable):
        """
        Question 4: Your eliminate implementation 

        Input factor is a single factor.
        Input eliminationVariable is the variable to eliminate from factor.
        eliminationVariable must be an unconditioned variable in factor.
        
        You should calculate the set of unconditioned variables and conditioned 
        variables for the factor obtained by eliminating the variable
        eliminationVariable.

        Return a new factor where all of the rows mentioning
        eliminationVariable are summed with rows that match
        assignments on the other variables.

        Useful functions:
        Factor.getAllPossibleAssignmentDicts
        Factor.getProbability
        Factor.setProbability
        Factor.unconditionedVariables
        Factor.conditionedVariables
        Factor.variableDomainsDict
        """
        # autograder tracking -- don't remove
        if not (callTrackingList is None):
            callTrackingList.append(('eliminate', eliminationVariable))

        # typecheck portion
        if eliminationVariable not in factor.unconditionedVariables():
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Elimination variable is not an unconditioned variable " \
                            + "in this factor\n" + 
                            "eliminationVariable: " + str(eliminationVariable) + \
                            "\nunconditionedVariables:" + str(factor.unconditionedVariables()))
        
        if len(factor.unconditionedVariables()) == 1:
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Factor has only one unconditioned variable, so you " \
                    + "can't eliminate \nthat variable.\n" + \
                    "eliminationVariable:" + str(eliminationVariable) + "\n" +\
                    "unconditionedVariables: " + str(factor.unconditionedVariables()))

        "*** YOUR CODE HERE ***"
        condition = factor.conditionedVariables()
        uncondition = factor.unconditionedVariables()
        uncondition.remove(eliminationVariable)     # I originally thought I had to remove the eliminationVariable from
                                                    # the conditioned variables
        domainDict = factor.variableDomainsDict()   # Included this because frustration is a thing
        newTable = Factor(uncondition, condition, domainDict)
        dictEntries = newTable.getAllPossibleAssignmentDicts()

        for entry in dictEntries:
            #print(entry)
            sumProbability = 0.0
            for value in domainDict[eliminationVariable]:   # I was trying to index all possible assignments instead of
                temp = entry                                # the domain of the eliminationVariable
                temp[eliminationVariable] = value
                sumProbability = sumProbability + factor.getProbability(temp)
            newTable.setProbability(entry, sumProbability)
        return newTable
        "*** END YOUR CODE HERE ***"

    return eliminate

eliminate = eliminateWithCallTracking()


def normalize(factor):
    """
    Question 5: Your normalize implementation 

    Input factor is a single factor.

    The set of conditioned variables for the normalized factor consists 
    of the input factor's conditioned variables as well as any of the 
    input factor's unconditioned variables with exactly one entry in their 
    domain.  Since there is only one entry in that variable's domain, we 
    can either assume it was assigned as evidence to have only one variable 
    in its domain, or it only had one entry in its domain to begin with.
    This blurs the distinction between evidence assignments and variables 
    with single value domains, but that is alright since we have to assign 
    variables that only have one value in their domain to that single value.

    Return a new factor where the sum of the all the probabilities in the table is 1.
    This should be a new factor, not a modification of this factor in place.

    If the sum of probabilities in the input factor is 0,
    you should return None.

    This is intended to be used at the end of a probabilistic inference query.
    Because of this, all variables that have more than one element in their 
    domain are assumed to be unconditioned.
    There are more general implementations of normalize, but we will only 
    implement this version.

    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """

    # typecheck portion
    variableDomainsDict = factor.variableDomainsDict()
    for conditionedVariable in factor.conditionedVariables():
        if len(variableDomainsDict[conditionedVariable]) > 1:
            print("Factor failed normalize typecheck: ", factor)
            raise ValueError("The factor to be normalized must have only one " + \
                            "assignment of the \n" + "conditional variables, " + \
                            "so that total probability will sum to 1\n" + 
                            str(factor))

    "*** YOUR CODE HERE ***"
    sum = 0.0
    dictEntries = factor.getAllPossibleAssignmentDicts()    # we need all the possible assignment dictionaries to sum the probabilities
    uncondition = factor.unconditionedVariables()
    unconditionCopy = []                                    # this holds the unconditioned variables to be factored
    condition = factor.conditionedVariables()

    for item in uncondition:
        unconditionCopy.append(item)

    for u in uncondition:
        currentVariable = factor.variableDomainsDict()[u]   # took forever to realize that I'm indexing a dictionary
        if len(currentVariable) == 1:                       # if there's one unconditioned variable
            condition.add(u)                                # put the variable in conditioned variables
            unconditionCopy.remove(u)                       # remove the variable from unconditioned variables

    for entry in dictEntries:                               #
        sum += factor.getProbability(entry)

    normal = Factor(unconditionCopy, condition, variableDomainsDict)

    for entry in dictEntries:
        newProbability = factor.getProbability(entry)/sum
        normal.setProbability(entry, newProbability)

    return normal
    "*** END YOUR CODE HERE ***"

