# Bot for a game "Thousand" utilizing the (MCTS) algorithm
## Description 
The "Thousand bot" was my final project for the AI course. 
The goal was to develop a bot to play the game 'Thousand' using the Monte Carlo Tree Search (MCTS) algorithm.
I decided to divide the problem into two main parts: bidding and playing phases. The first phase, bidding, is based on probabilities.
The approach I used involved calculating all possible hands, counting winning tricks, and points for melds.
Then, I parsed the sum of these values into a dictionary and calculated the probabilities of having a hand that would surely give us a certain number of points.
Based on the generated probabilities, the cards in meld colors, and bias points (a global variable), the bot decides whether to play or pass.
The implementation of the second phase, playing, was based on the MCTS algorithm, which runs only when no card is a guaranteed winner.
The FullGame.py script simulates a game with random players and prints data describing the game to the standard output.
## Dependencies

This project requires the following external libraries:

- `typeguard`: For runtime type checking.
- `random`: For generating random numbers and making random choices.
- `copy`: For creating deep copies of objects.
- `logging`: For logging messages and debugging information.
- `pygame`: For creating graphical interfaces and handling game mechanics. *(currently in progress)*
- `math`: For mathematical functions and calculations.
- `concurrent.futures`: For concurrent execution of code using threads or processes.

### Installation

You can install these dependencies using the following command:

    pip install typeguard pygame

Note: The `random`, `copy`, `logging`, `math`, and `concurrent.futures` libraries are part of the Python standard library and do not require separate installation.
## Usage

To run the Thousand bot, follow these steps:

1. Ensure you have Python 3.9 installed on your system.
2. Install the required dependencies
3. Run the FullGame.py script to simulate a game:

    ```bash
    python FullGame.py
    ```
