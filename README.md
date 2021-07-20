# RL-TicTacToeAgent
An assignment to demonstrate Reinforced Learning of an Numerical TicTacToe agent. Instead of X’s and O’s, the numbers 1 to 9 are used. In the 3x3 grid, numbers 1 to 9 are filled, with one number in each cell. The first player plays with the odd numbers, the second player plays with the even numbers, i.e. player 1 can enter only an odd number in the cell while player 2 can enter an even number in one of the remaining cells. Each number can be used exactly once in the entire grid. The player who puts down 15 points in a line - (column, row or a diagonal) wins the game. 

In this assignment the agent is the first player i.e. he plays with odd numbers.
We design a naive environment i.e the other player and also the agent to learn using RL.

## Files:
1. TCGame_Env.py: The source code for the naive environment i.e. the other player.
2. TicTacToe_Agent.ipynb: The source code for the agent that learns from the environment.

