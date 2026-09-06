############### Our Blackjack House Rules #####################

# The deck is unlimited in size.
# There are no jokers.
# The Jack/Queen/King all count as 10.
# The the Ace can count as 11 or 1.
# Use the following list as the deck of cards:
cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
# The cards in the list have equal probability of being drawn.
# Cards are not removed from the deck as they are drawn.


import random


def deal_card():
    """Returns a random card from the deck."""
    return random.choice(cards)

# Hint 6: Create a function called calculate_score() that takes a List of cards as input
# and returns the score.
# Look up the sum() function to help you do this.


def calculate_score(cardsn):
    """Take a list of cards and return the score calculated from the cards"""
    total = sum(cardsn)
    if len(cardsn)==2 and total==21:
        total = 0
    elif total > 21:
        for i in range(len(cardsn)):
            if cardsn[i] == 11:
                cardsn[i] = 1
        total = sum(cardsn)
    return total
    # Hint 7: Inside calculate_score() check for a blackjack (a hand with only 2 cards: ace + 10) and return 0 instead of the actual score. 0 will represent a blackjack in our game.
    # Hint 8: Inside calculate_score() check for an 11 (ace). If the score is already over 21, remove the 11 and replace it with a 1. You might need to look up append() and remove().
    # Hint 13: Create a function called compare() and pass in the user_score and computer_score. If the computer and user both have the same score, then it's a draw.
    # If the computer has a blackjack (0), then the user loses. If the user has a blackjack (0), then the user wins. If the user_score is over 21, then the user loses.
    # If the computer_score is over 21, then the computer loses. If none of the above, then the player with the highest score wins.

def compare(user_score, computer_score):
    print("Your score is " + str(user_score))
    print("Computer score is " + str(computer_score))
    if computer_score == 0:
        print("You lose, opponent has Blackjack!") 
    
    elif user_score == 0:
        print( "You win with a Blackjack!")

    elif user_score == computer_score:
            print( "Draw!")

    elif user_score > 21:
        print("You went over. You lose!")
        return False
    
    elif computer_score > 21:
        print("Opponent went over. You win!")
        return False

    elif user_score > computer_score:
        print( "You win!")
    
    else:
        print("You lose!") 
    
    return True

cardu = []
cardc = []
for i in range(2):
    cardu.append(deal_card())
    cardc.append(deal_card())
print("Your cards:", cardu)
print("Computer cards:", cardc)
scoreu = calculate_score(cardu)
scorec = calculate_score(cardc)
result = compare(scoreu, scorec)
#print ("first result:", result)

def play_game():
    global result
    cardu.append(deal_card())
    scoreu = calculate_score(cardu)
    cardc.append(deal_card())
    scorec = calculate_score(cardc)
    print("Your cards:", cardu)
    print("Computer cards:", cardc)
    result = compare(scoreu, scorec)

    # Hint 5: Deal the user and computer 2 cards each using deal_card()
    # Hint 9: Call calculate_score(). If the computer or the user has a blackjack (0) or if the user's score is over 21, then the game ends.
    # Hint 10: If the game has not ended, ask the user if they want to draw another card. If yes, then use the deal_card() function to add another card to the user_cards List.
    # If no, then the game has ended.
    # Hint 11: The score will need to be rechecked with every new card drawn and the checks in Hint 9 need to be repeated until the game ends.
    # Hint 12: Once the user is done, it's time to let the computer play. The computer should keep drawing cards as long as it has a score less than 17.


# Hint 14: Ask the user if they want to restart the game. If they answer yes, clear the console and start a new game of blackjack and show the logo from art.
while result == True and input("Do you want to play a game of Blackjack? Type 'y' or 'n': ") == "y":
    play_game()
print("End of the game!")
