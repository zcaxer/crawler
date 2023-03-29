import random
from itertools import permutations


def generate_number():
    digits = list(range(10))
    random.shuffle(digits)
    return digits[:4]


def get_guess():
    guess = input("Enter your guess (4 digits): ")
    return [int(digit) for digit in guess]


def check_guess(number, guess):
    a = 0
    b = 0
    for i in range(4):
        if guess[i] == number[i]:
            a += 1
        elif guess[i] in number:
            b += 1
    return (a, b)


while True:
    number = generate_number()
    print("New game started!")
    while True:
        guess = get_guess()
        print(guess)
        a, b = check_guess(number, guess)
        print(f"{a}A{b}B")
        if (a, b) == (4, 0):
            print("Congratulations! You guessed the number.")
            break
    choice = input("Do you want to play again? (y/n): ")
    if choice.lower() != "y":
        break
