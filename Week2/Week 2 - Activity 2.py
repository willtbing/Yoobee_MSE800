import random
import string

class Play_Game:
    def __init__(self, max_lives=6):
        self.max_lives = max_lives
        self.secret_word = self.get_random_word()
        self.blanks = self.make_blanks(self.secret_word)
        self.lives = max_lives
        self.used_letters = set()

    # get a random word from a predefined list
    def get_random_word(self):
        
        words = [
            "python", "variable", "function", "iterator", "notebook",
            "pipeline", "dataset", "computer", "research", "analytics"
        ]
        return random.choice(words)

    # create a list of blanks for the word
    def make_blanks(self, word):
        
        return ["_" for _ in word]

    # prompt the user for a letter, ensuring it's valid and not already used
    def prompt_for_letter(self):

        while True:
            guess = input("Guess a letter: ").strip().lower()
            if len(guess) != 1 or guess not in string.ascii_lowercase:
                print(" → Please enter a single A-Z letter.")
                continue
            if guess in self.used_letters:
                print(" → You already tried that letter.")
                continue
            return guess

    # reveal the guessed letter in the blanks if it exists in the word
    def reveal_letters(self, letter):

        found_any = False
        for i, ch in enumerate(self.secret_word):
            if ch == letter and self.blanks[i] == "_":
                self.blanks[i] = letter
                found_any = True
        return found_any

    # check if all blanks are filled
    def all_blanks_filled(self):
       
        return "_" not in self.blanks

def main():
    game = Play_Game()
    print("\nWelcome to Word Guessing!")
    print(f"The word has {len(game.secret_word)} letters.")
    print(" ".join(game.blanks))

    while True:
        guess = game.prompt_for_letter()
        game.used_letters.add(guess)

        if game.reveal_letters(guess):
            print("\n Well done, Nice job! You found a letter.")
            print(" ".join(game.blanks))
            if game.all_blanks_filled():
                print("\n Congratulation! You guessed the word!")
                print(f"Word: {game.secret_word}")
                print("GAME OVER")
                break
        else:
            game.lives -= 1
            print(f"\nNope. You lose a life. Lives left: {game.lives}")
            print(" ".join(game.blanks))
            if game.lives <= 0:
                print("\n Out of lives & Sad story!")
                print(f"The word was: {game.secret_word}")
                print("GAME OVER")
                break

if __name__ == "__main__":
    main()
