from gym import spaces
import numpy as np
import random
from itertools import groupby
from itertools import product



class TicTacToe():

    def __init__(self):
        """initialise the board"""
        
        # initialise state as a 2D array of 3,3 with all nans
        self.state = np.empty((3,3))  
        self.state[:] = np.nan
        
        # all possible numbers from 1 to 9
        self.all_possible_numbers = np.arange(1, 10)

        self.reset()


    def is_winning(self, curr_state):
        """Takes state as an input and returns whether any row, column or diagonal has winning sum
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan]
        Output = False"""
        
        # Check sum of any column is 15
        is_column_win = (curr_state.sum(axis=0) == 15).sum() > 0
        
        # Check sum of any row is 15
        is_row_win = (curr_state.sum(axis=1) == 15).sum() > 0
        
        # Check sum of any diagonal is 15
        is_diagonal_win = curr_state.trace() == 15 or np.flip(curr_state,1).trace()
        
        return is_column_win or is_row_win or is_diagonal_win
 

    def is_terminal(self, curr_state):
        # Terminal state could be winning state or when the board is filled up

        if self.is_winning(curr_state) == True:
            return True, 'Win'

        elif len(self.allowed_positions(curr_state)) ==0:
            return True, 'Tie'

        else:
            return False, 'Resume'


    def allowed_positions(self, curr_state):
        """Takes state as an input and returns all indexes that are blank"""
        return np.argwhere(np.isnan(curr_state))


    def allowed_values(self, curr_state):
        """Takes the current state as input and returns all possible (unused) values that can be placed on the board"""
        
        # Find used values
        used_values = curr_state[~np.isnan(curr_state)]
        
        # Find allowed values for agent
        agent_values = np.array([val for val in self.all_possible_numbers if val not in used_values and val % 2 != 0])
        
        # Find allowed values for environment
        env_values = np.array([val for val in self.all_possible_numbers if val not in used_values and val % 2 == 0])

        return (agent_values, env_values)


    def action_space(self, curr_state):
        """Takes the current state as input and returns all possible actions, i.e, all combinations of allowed positions and allowed values"""
    
        # Here action is a pair of location and value.
    
        # Find all possible actions for the agent from current state
        agent_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[0])
        
        # Find all possible actions for the environment from current state
        env_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[1])
        
        return (list(agent_actions), list(env_actions))



    def state_transition(self, curr_state, curr_action):
        """Takes current state and action and returns the board position just after agent's move.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = [1, 2, 3, 4, nan, nan, nan, 9, nan]
        """
        # Get location from action
        loc = curr_action[0]
        
        # Get value from action
        value = curr_action[1]
        
        # Update value at the location
        curr_state[loc[0]][loc[1]] = value
        
        return curr_state


    def step(self, curr_state, curr_action):
        """Takes current state and action and returns the next state, reward and whether the state is terminal. Hint: First, check the board position after
        agent's move, whether the game is won/loss/tied. Then incorporate environment's move and again check the board status.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = ([1, 2, 3, 4, nan, nan, nan, 9, nan], -1, False)"""
        
        # Perform user action from current state and transition to next state
        self.state_transition(curr_state, curr_action)
        
        # Check the state
        is_terminal, agent_win_tie_resume = self.is_terminal(curr_state)
        
        
        if is_terminal:
            # The agent action resulted in termination. Thus the game either was won by the agent or it was tied.
            # If agent won reward is 10.
            # If game was a tie reward is 0
            
            if agent_win_tie_resume == 'Win':
                reward = 10  
            elif agent_win_tie_resume == 'Tie':
                reward = 0
                
            return curr_state, reward, True
        else:
            # Let environment take a random action from its action space from current state.
            state_action_space = self.action_space(curr_state)[1]
            state_action_space_n = len(state_action_space)
            env_action_index = np.random.choice(np.arange(state_action_space_n))
            env_action = state_action_space[env_action_index]
            self.state_transition(curr_state, env_action)
            
            is_terminal, env_win_tie_resume = self.is_terminal(curr_state)
            
            # If environment won reward is -10.
            # If game was a tie reward is 0
            # If the game is resumed reward is -1
            if is_terminal:
                if env_win_tie_resume == 'Win':
                    reward = -10
                elif agent_win_tie_resume == 'Tie':
                    reward = 0
            else:
                reward = -1
                
            return curr_state, reward, is_terminal
                
            
    def reset(self):
        return self.state
