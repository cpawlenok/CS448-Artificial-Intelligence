# shopSmart.py
# ------------
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


"""
Here's the intended output of this script, once you fill it in:

Welcome to shop1 fruit shop
Welcome to shop2 fruit shop
For orders:  [('apples', 1.0), ('oranges', 3.0)] best shop is shop1
For orders:  [('apples', 3.0)] best shop is shop2
"""
from __future__ import print_function
import shop


def shopSmart(orderList, fruitShops):
    """
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    """

    "first I set the lowest total as the very first fruit shop"
    lowestTotal = 0.0
    for (type, weight) in orderList:
        lowestTotal = lowestTotal + (weight*fruitShops[0].getCostPerPound(type))
        lowestShop = fruitShops[0]

    """ 
        The reason I did this was because I couldn't think of a way to compare the total on the first iteration
        of looping through the shops...I'm sure there's a more efficient way to do this but I couldn't think of it 
    """

    for currShop in fruitShops[1:]:
        currentTotal = 0.0
        for (fruit, numPound) in orderList:
            currentTotal = currentTotal + (numPound*currShop.getCostPerPound(fruit))
        if currentTotal < lowestTotal:
            lowestShop = currShop
            total = sum

    "This nested loop iterates through the remaining shops to find the lowest total of grocery list"
    "I just realized that there's a getPriceOfOrder function that would have made my life a lot easier...oh well"

    return lowestShop


if __name__ == '__main__':
    "This code runs when you invoke the script from the command line"
    orders = [('apples', 1.0), ('oranges', 3.0)]
    dir1 = {'apples': 2.0, 'oranges': 1.0}
    shop1 = shop.FruitShop('shop1', dir1)
    dir2 = {'apples': 1.0, 'oranges': 5.0}
    shop2 = shop.FruitShop('shop2', dir2)
    shops = [shop1, shop2]
    print("For orders ", orders, ", the best shop is", shopSmart(orders, shops).getName())
    orders = [('apples', 3.0)]
    print("For orders: ", orders, ", the best shop is", shopSmart(orders, shops).getName())
