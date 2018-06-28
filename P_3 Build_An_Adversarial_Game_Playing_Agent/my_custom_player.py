from sample_players import DataPlayer
from isolation import Isolation

class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only *required* method. You can modify
    the interface for get_action by adding named parameters with default
    values, but the function MUST remain compatible with the default
    interface.

    **********************************************************************
    NOTES:
    - You should **ONLY** call methods defined on your agent class during
      search; do **NOT** add or call functions outside the player class.
      The isolation library wraps each method of this class to interrupt
      search when the time limit expires, but the wrapper only affects
      methods defined on this class.

    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.
    **********************************************************************
    """
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller is responsible for
        cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE:
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # TODO: Replace the example implementation below with your own search
        #       method by combining techniques from lecture
        #
        # EXAMPLE: choose a random move without any search--this function MUST
        #          call self.queue.put(ACTION) at least once before time expires
        #          (the timer is automatically managed for you)          
        best_move = None
        self.count = 0
        try:
            depth = 0
            while True:
                move = self.queue.put(self.alpha_beta_search(state, depth))                
                if move == (-1,-1):
                    return best_move
                else:
                    best_move = move
                depth +=1
        except:
            return best_move, print(self.count)
        
    def min_value(self, state, alpha, beta, depth):
        if state.terminal_test():
            return state.utility(self.player_id)
        if depth <= 0 and state.ply_count <=2:
            return self.start_score(state)
        if depth <= 0 and state.ply_count >2:
            return self.score(state)
        v = float("inf")
        for a in state.actions():
            v = min(v, self.max_value(state.result(a), alpha, beta, depth-1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v


    def max_value(self, state, alpha, beta, depth):
        if state.terminal_test():
            return state.utility(self.player_id)
        if depth <= 0 and state.ply_count <=2:
            return self.start_score(state)
        if depth <= 0 and state.ply_count >2:
            return self.score(state)            
        v = float("-inf")
        for a in state.actions():
            v = max(v, self.min_value(state.result(a), alpha, beta, depth-1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def alpha_beta_search(self, state, depth):
        self.count += 1
        alpha=float("-inf")
        beta=float("inf")
        best_score = float("-inf") 
        best_move = None
        for a in state.actions():
            v = self.min_value(state.result(a), alpha, beta, depth-1)
            alpha = max(alpha, v)
            if v > best_score:
                best_score = v
                best_move = a
        return best_move

    def score (self, state):
        own_liberties = state.liberties(state.locs[self.player_id])
        opp_liberties = state.liberties(state.locs[1 - self.player_id])
        own_moves = len(own_liberties)
        opp_moves = len(opp_liberties)
        if own_moves < 5:
            return (1.5 * own_moves) - (opp_moves)
        elif own_moves == 0:
            return -10
        elif opp_moves == 0:
            return 10
        else:
            return (own_moves) - (1.5 * opp_moves)

    def start_score(self, state):
        own_liberties = state.liberties(state.locs[self.player_id])
        center_x, center_y = 5, 7
        center = (center_x, center_y)
        if center in own_liberties:
            return 10
        else:
            return -10

  
