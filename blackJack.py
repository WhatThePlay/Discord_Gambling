from CardDeck import Deck
from random import Random

random = Random()

# takes a Deck as a list and shuffles it
DeckList = list(Deck.items())
RandomDeckList = random.sample(DeckList, len(DeckList))


# deals a card to the mentioned hand
def deal_card(deck, hand):
    hand.append(deck[0])
    deck.pop(0)


# returns the the total value of every card in mentioned hand
def count_value(hand):
    value = 0
    for i in range(len(hand)):
        value += hand[i][1]
    return value


# resets the game by clearing both hands and creating a new deck
def reset_game(hand1, hand2, deck, new_deck):
    hand1.clear()
    hand2.clear()
    deck.clear()
    deck += new_deck


# returns the mentioned hand as a clean String
def tostring(hand):
    s = ""
    for i in range(len(hand)):
        s += hand[i][0]
        s += " "
    return s
