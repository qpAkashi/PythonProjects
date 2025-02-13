import random

options = ("rock", "paper", "scissors")
computerOption = random.choice(options)


player = input("Choose between rock, paper, or scissors: ").lower()


if player not in options:
    print("Invalid choice. Please choose rock, paper, or scissors.")
else:
    print(f"You chose: {player}")
    print(f"Computer chose: {computerOption}")


    if player == computerOption:
        print("It's a tie!")
    elif (player == "rock" and computerOption == "scissors") or \
         (player == "paper" and computerOption == "rock") or \
         (player == "scissors" and computerOption == "paper"):
        print("You won!")
    else:
        print("You lost!")