import random
random.seed()

def mc_dice_odds(expectedSum, numberOfDices, rangeMax=1000000):
    probabilityIn = 0
    probabilityOut = 0
    for i in range(rangeMax):
        sum = 0
        for j in range(numberOfDices):
            sum += random.randint(1,6)
        if (sum) == expectedSum:
            probabilityIn += 1
        else:
            probabilityOut += 1
    return probabilityIn/(probabilityIn+probabilityOut)


# Montecarlo is such unreliable, is more usefull using dice_odds.py -> what_are_the_odds function;

# if __name__ == "__main__":
#     # from dice_odds_2 import what_are_the_odds
#     # # print(mc_dice_odds(7, 2))
#     # # print(dice_odds.what_are_the_odds(7, 2))
#     # # print(mc_dice_odds(8, 3))
#     # print(what_are_the_odds(8, 3))
