## Matthew Conroy 2017
## Hangliang Ren 2022
##
##
## A simulation of the game No Thanks!
## see https://en.wikipedia.org/wiki/No_Thanks!_(game)
##
##
## This program simulates the all pairs of strategies in strategy 2.
##
##
import itertools,random

class Player:

	def __init__(self, tokens, cards):
		self.tokens = tokens
		self.cards = cards

class GameState: # I don't actually use this class!!!

	def __init__(self, tokens, card): ## the current state of the game is the number of tokens on the
		self.tokens = tokens          ## current card, and which card is current
		self.card = card


numberOfPlayers = 4 ## the number of players
numberOfGames = 1000


def pairs(alphas=[10, 15, 20], betas=[1, 2, 3, 4]):
    """
    parameters:
        alphas: All alpha values we will try.
        betas: All beta values we will try.
    Return all pairs [alpha, beta] we will try.
    """
    # get all combinations of alphas and betas
    combinations = []
    for alpha in alphas:
        for beta in betas:
            combinations.append([alpha, beta])

    # get all pairs [alpha, beta] we will try
    pairs_try = itertools.product(combinations, repeat=2)
    return list(pairs_try)


wins=[] # array to keep track of how many times each player wins
for i in range(numberOfPlayers):
	wins.append(0)

# prepare all [alpha, beta] pairs we will try
pairs_try = pairs()

results = dict()
for player_0, player_others in pairs_try:
    for game in range(numberOfGames): ## main game loop

        ### prepare the deck for a game

        # generate the deck
        deck = list(range(3,36))
        # shuffle the cards
        random.shuffle(deck)
        #remove 9 cards
        deck = deck[:-9]

        ### initialize players array
        # Each player needs two things: an integer indicating how many
        # tokens they have, and a list of the cards they have

        players=[]
        for i in range(numberOfPlayers):
            players.append(1)

        # initialize each player with 11 tokens and an empty list of cards

        for i in range(numberOfPlayers):
            players[i] = Player(11,[])


        #### start playing

        currentPlayer = game % numberOfPlayers ## start with a different player each time
        cardIndex = 0 # start at one end of the deck of cards
        currentTokens = 0 # initially there are no tokens on the current card
        while(cardIndex<24):
            currentCard = deck[cardIndex]
            ## currentPlayer either adds a token, or takes the card
            if (currentPlayer in [0]):
                cardThresh=player_0[0]
                # this next conditional statement is the strategy for this/these players:
                beta_0 = player_0[1]
                if players[currentPlayer].tokens < beta_0:  # when number of tokens less than beta
                    # pick up the card if (1) it is adjacent to a card the player already has, or
                    # (2) currentCard-1.5*currentTokens<cardThresh, or
                    # (3) the player has no tokens
                    if (  (currentCard+1 in players[currentPlayer].cards) or (currentCard-1 in players[currentPlayer].cards)
                    or (currentCard - 1.5 * currentTokens < cardThresh) or (players[currentPlayer].tokens==0)):
                    ## currentPlayer takes the card and the tokens, if any
                        players[currentPlayer].tokens = players[currentPlayer].tokens+currentTokens
                        players[currentPlayer].cards.append(currentCard)
                        cardIndex=cardIndex+1 ## get ready to turn over the next card
                        currentTokens=0
                    else:## currentPlayer adds a token to the card
                        currentTokens = currentTokens + 1
                        players[currentPlayer].tokens=players[currentPlayer].tokens-1
                else:  # when number of tokens greater than or equal to beta
                    # pick up the card if (1) it is adjacent to a card the player already has, or
                    # (2) currentCard-currentTokens<cardThresh, so the number of tokens offsets the points of the cards sufficiently, or
                    # (3) the player has no tokens
                    if (  (currentCard+1 in players[currentPlayer].cards) or (currentCard-1 in players[currentPlayer].cards)
                    or (currentCard-currentTokens<cardThresh) or (players[currentPlayer].tokens==0)):
                    ## currentPlayer takes the card and the tokens, if any
                        players[currentPlayer].tokens = players[currentPlayer].tokens+currentTokens
                        players[currentPlayer].cards.append(currentCard)
                        cardIndex=cardIndex+1 ## get ready to turn over the next card
                        currentTokens=0
                    else:## currentPlayer adds a token to the card
                        currentTokens = currentTokens + 1
                        players[currentPlayer].tokens=players[currentPlayer].tokens-1

            if (currentPlayer in [1,2,3]):
                cardThresh=player_others[0]
                # this next conditional statement is the strategy for this/these players:
                beta_other = player_others[1]
                if players[currentPlayer].tokens < beta_0:  # when number of tokens less than beta
                    # pick up the card if (1) is a adjacent to a card the player already has, or
                    # (2) currentCard-1.5*currentTokens<cardThresh, or
                    # (3) the player has no tokens
                    if ( (currentCard+1 in players[currentPlayer].cards) or (currentCard-1 in players[currentPlayer].cards) or
                    (currentCard - 1.5 * currentTokens < cardThresh) or (players[currentPlayer].tokens==0)):
                    ## currentPlayer takes the card and the tokens, if any
                        players[currentPlayer].tokens = players[currentPlayer].tokens+currentTokens
                        players[currentPlayer].cards.append(currentCard)
                        cardIndex=cardIndex+1 ## get ready to turn over the next card
                        currentTokens=0
                    else:## currentPlayer adds a token to the card
                        currentTokens = currentTokens + 1
                        players[currentPlayer].tokens=players[currentPlayer].tokens-1
                else:  # when number of tokens greater than or equal to beta
                    # pick up the card if (1) is a adjacent to a card the player already has, or
                    # (2) currentCard-currentTokens<cardThresh, so the number of tokens offsets the points of the cards sufficiently, or
                    # (3) the player has no tokens
                    if ( (currentCard+1 in players[currentPlayer].cards) or (currentCard-1 in players[currentPlayer].cards) or
                    (currentCard-currentTokens<cardThresh) or (players[currentPlayer].tokens==0)):
                    ## currentPlayer takes the card and the tokens, if any
                        players[currentPlayer].tokens = players[currentPlayer].tokens+currentTokens
                        players[currentPlayer].cards.append(currentCard)
                        cardIndex=cardIndex+1 ## get ready to turn over the next card
                        currentTokens=0
                    else:## currentPlayer adds a token to the card
                        currentTokens = currentTokens + 1
                        players[currentPlayer].tokens=players[currentPlayer].tokens-1

            # next players turn
            currentPlayer = (currentPlayer+1) % numberOfPlayers

        ## game is over!

        ## calculate the players' scores

        # initialize score array
        scores=[]
        for i in range(numberOfPlayers):
            scores.append(1)

        minScore = 0 # clear minScore
        for i in range(numberOfPlayers):
            # calculate player i's score, find minimum score
            scores[i] = -players[i].tokens # start by subtracting the tokens
            players[i].cards.sort() # put the cards list in increasing order
            for j in range(len(players[i].cards)):
                # the lowest cards count, and all other cards count only if they are not one more
                # than the previous cards in the list
                if( (j==0)  or (players[i].cards[j-1]!=players[i].cards[j]-1)):
                    scores[i] = scores[i]+players[i].cards[j]
            if ((scores[i]<minScore) or (i==0)):
                minScore = scores[i]
        numWithMinScore=0
        for i in range(numberOfPlayers):
            # count number of players with minimum score
            if (scores[i]==minScore):
                numWithMinScore += 1
        # if a tie, each tying player gets an equal fraction of the win (i.e., if two tie, they each get 0.5, etc.)
        for i in range(numberOfPlayers):
            if (scores[i]==minScore):
                wins[i] += 1./numWithMinScore
    
    # calculate current estimated win probability for player zero
    result = (tuple(player_0), tuple(player_others))
    results[result] = wins[0] * 1. / numberOfGames
    
    # reset all values in wins list to 0, prepare for next pairs
    wins = [0 for k in range(len(wins))]

# find the pair (player_0, player_other) that yield the hugest winning probability of player_0
to_find = max(results.values())
for result in results:
    if results[result] == to_find:
        print("The pair of strategy yields the hugest winning probability:", result, to_find)

# the dictionary "results" stores winning probability of player_0, by trying all pairs of strategies
print("\nAll results:")
for strategy in results:
    # strategy here stores a pair of strategy, in this pair,
    # the first tuple stores strategy player_0 follow, the second tuple stores strategy player_other follow
    print("Strategy:", strategy, "Win Probability:", results[strategy])