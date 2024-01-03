import random
from string import ascii_lowercase

# Initialize the stages of the game board
HANGMAN_ART = ['''
    +---+
        |
        |
        |
       ===''', '''
    +---+
    O   |
        |
        |
       ===''', '''
    +---+
    O   |
    |   |
        |
       ===''', '''
    +---+
    O   |
   /|   |
        |
       ===''', '''
    +---+
    O   |
   /|\  |
        |
       ===''', '''
    +---+
    O   |
   /|\  |
   /    |
       ===''', '''
    +---+
    O   |
   /|\  |
   / \  |
       ===''']

# # FOR TESTING
# words = ["annoy", "attention", "calm", "comfortable", "consequences",
#         "curious", "curve", "decide", "directions", "disappointed"]

def get_settings() -> tuple[str, int]:
    """
    Get user choice of desired word pool and max word length
    """
    # word_options values used verbatim to open the word file
    word_options = {1: 'animals', 2: 'vocab_words'}

    print("Word pool options:")
    for key, value in word_options.items():
        print(f"\tOption {key} - {value}")
    print()

    # Collect and validate user's choice
    while True:
        try:
            word_choice = int(input("Please enter the desired option number: "))
            if word_choice in word_options.keys():
                break
            else:
                raise ValueError
        except ValueError:
            print("Please enter a valid option.")

    # Display max word length options to user
    length_options = {1: 5, 2: 10, 3: 20}
    print("\nMax word length options:")
    for key, value in length_options.items():
        print(f"\tOption {key} - {value} letters")

    # Collect and validate user's choice
    while True:
        try:
            length_choice = int(input("Please enter the desired option number: "))
            if length_choice in length_options.keys():
                break
            else:
                raise ValueError
        except ValueError:
            print("Please enter a valid option.")

    return word_options[word_choice], length_options[length_choice]


def get_random_word(word_option: str, max_length: int) -> str:
    """
    Opens file according to the selected word pool and returns
    a randomly selected word no longer than the selected max length
    """
    
    filename = word_option + ".txt"
    # file must be in same dir as hangman.py
    with open(filename) as f:
        contents = f.readlines()
        wordlist = [word.strip().lower() for word in contents if len(word) <= max_length]

    index = random.randint(0, len(wordlist) - 1) # inclusive range
    
    return wordlist[index]

# # FOR TESTING
# def get_random_word(word_list: list) -> str:
#     index = random.randint(0, len(word_list) - 1) # range is inclusive
#     return word_list[index]


def display_board(incorrect: str, correct: str, secret_word: str):
    # Update the game board's hangman art
    print(HANGMAN_ART[len(incorrect)], '\n')

    print(f"INCORRECT: {' '.join(incorrect)}\n")
    
    blanks = '_' * len(secret_word)
    # Replace blanks with correctly guessed letters
    for i in range(len(secret_word)):
        if secret_word[i] in correct:
            blanks = blanks[:i] + secret_word[i] + blanks[i+1:]

    # Show the current status of the secret word
    # add spaces between each letter for extra clarity
    print(f"WORD: {' '.join(blanks)}\n")


def get_guess(already_guessed) -> str:
    # Ensure player guesses a single, valid letter
    while True:
        guess = input("Guess a letter: ").lower()

        if len(guess) != 1:
            print("Please guess a single letter.")
        elif guess in already_guessed:
            print("You've already guessed that letter! Please guess another one.")
        elif guess not in ascii_lowercase:
            print("Please enter a valid letter.")
        else:
            return guess


def play_again() -> bool:
    answer = ""
    while answer not in ['y', 'yes', 'n', 'no']:
        answer = input("\nPlay again? (yes/no): ").lower()

    return answer.startswith('y')

# ---------------
# Set up the game
# ---------------
print("""===============
 H A N G M A N
===============\n""")

incorrect_letters  = ""
correct_letters = ""
word_pool, max_length = get_settings()
secret_word = get_random_word(word_pool, max_length)
# # FOR TESTING
# secret_word = get_random_word(words)
game_done = False

# --------------
# Main game loop
# --------------
while True:
    display_board(incorrect_letters, correct_letters, secret_word)

    guess = get_guess(incorrect_letters + correct_letters)

    if guess in secret_word:
        correct_letters += guess

        # Check if player won
        won = True
        for i in range(len(secret_word)):
            if secret_word[i] not in correct_letters:
                won = False
                break

        if won:
            print(f"You win!\nThe secret word is: {secret_word.upper()}!")
            game_done = True
    else:
        incorrect_letters += guess

        # Check if player lost
        if len(incorrect_letters) == len(HANGMAN_ART) - 1: # player has run out of turns
            display_board(incorrect_letters, correct_letters, secret_word)
            print("You lost!")
            # Display game statistics
            print(f"- Incorrect guesses: {len(incorrect_letters)}")
            print(f"- Correct guesses:   {len(correct_letters)}")
            print(f"The secret word was: {secret_word.upper()}")

            game_done = True # Use this line for 'Part 4: Testing your program'

    # Play again?
    if game_done:
        if play_again():
            incorrect_letters = ""
            correct_letters   = ""
            game_done = False
            word_pool, max_length = get_settings()
            secret_word = get_random_word(word_pool, max_length)
            # secret_word = get_random_word(words)
        else:
            break

print("\nGoodbye!\n")