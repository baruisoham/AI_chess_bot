import chess as ch  # Importing the python-chess library
import random as rd  # Importing the random module for adding a small random factor to the evaluation function

class Engine:
    def __init__(self, board, maxDepth, color):
        # Constructor for the Engine class
        # board: an instance of the chess.Board class representing the initial position
        # maxDepth: the maximum depth for the search algorithm
        # color: the color of the engine (ch.WHITE or ch.BLACK)
        self.board = board
        self.color = color
        self.maxDepth = maxDepth
        self.current_depth = 0  # Current depth of the search
        self.searching = False  # Flag to indicate if the engine is currently searching for a move
        self.best_move = None  # The best move found by the search algorithm

    def handle_command(self, command):
        # Method to handle UCI commands
        if command == "uci":
            # Respond with "uciok" when the UCI command is received
            print("uciok")
        elif command == "isready":
            # Respond with "readyok" when the "isready" command is received
            print("readyok")
        elif command.startswith("position"):        #if command starts with position, it checks for the subcommand given

            parts = command.split(" ")
            if parts[1] == "startpos":           # If "startpos" is subcommand, reset the board to the initial position
                self.board = ch.Board()
            elif parts[1] == "fen":             # If "fen" is provided, set the board position using the provided FEN string
                fen = " ".join(parts[2:])
                self.board.set_fen(fen)
                
            if "moves" in command:
                # If the "moves" part is present, update the board position with the provided moves
                
                
                moves_start_index = command.index("moves") + len("moves") + 1           ##find index of 'moves' in command, then add length of 'moves' + 1 to reach the starting of the move
                moves_str = command[moves_start_index:].strip()                     ## take command, and only keep the part after moves_start_index    ## strip() -- remove whitespaces
                moves_list = moves_str.split()
                
                for move_str in moves_list:                             #add all moves into move list and process them individually
                    move = ch.Move.from_uci(move_str)
                    self.board.push(move)                               #make the given move into your chessboard
                    
                    
        elif command.startswith("go"):      # "go" command to start searching for the best move
            if "infinite" in command:
                pass
            else:
                self.searching = True  # Set the searching flag to True
                self.current_depth = self.maxDepth  # Reset the current depth to the maximum depth
                self.get_best_move()  # Call the get_best_move method to find the best move
                
        elif command == "ucinewgame":
            # Handle the "ucinewgame" command to reset the engine for a new game
            self.searching = False  # Reset the searching flag
            self.current_depth = 0  # Reset the current depth
            
        elif command == "quit":
            # Handle the "quit" command to exit the engine
            print("Bye!")
            exit()

    def get_best_move(self):
        # Method to find the best move using engine and print it in UCI format
        best_move = self.engine(None, 1)  # Call the engine method with an initial depth of 1
        uci_best_move = self.convert_to_uci(best_move)  # Convert the best move to UCI format
        print(f"bestmove {uci_best_move}")  # Print the best move in UCI format

    def eval_function(self):
        # Evaluation function for the engine
        compt = 0
        for i in range(64):                 #we go to each square on the board and add eval points of each square in compt
            compt += self.squareResPoints(ch.SQUARES[i])
        # Add additional factors to the evaluation score
        compt += self.mateOpportunity() + self.opening() + 0.001 * rd.random()      # we add extra points for mate opportunity, opening phase points
        return compt

    def mateOpportunity(self):
        # Method to evaluate mate opportunities
        if self.board.is_game_over():
            # If the game is over, return a large positive or negative score based on the result
            if self.board.result() == "1-0":
                return 999
            elif self.board.result() == "0-1":
                return -999
        return 0

    def opening(self):
        # Method to evaluate the opening phase of the game
        if self.board.fullmove_number < 10:
            # If the game is in the opening phase (less than 10 full moves)
            
            if self.board.turn == self.color:           #if it is my color's turn, then encourage more legal moves
               
                return 1 / 30 * len(list(self.board.legal_moves))   # 1/30*no. of legal moves
            
            else:                                       # if it is my opponent's turn, then discourage legal moves
                
                return -1 / 30 * len(list(self.board.legal_moves))  
        else:
            return 0

    def squareResPoints(self, square):
        # Method to evaluate the value of a piece on a given square
        pieceValue = 0
        if self.board.piece_type_at(square) == ch.PAWN:
            pieceValue = 1
        elif self.board.piece_type_at(square) == ch.ROOK:
            pieceValue = 5.1
        elif self.board.piece_type_at(square) == ch.BISHOP:
            pieceValue = 3.33
        elif self.board.piece_type_at(square) == ch.KNIGHT:
            pieceValue = 3.2
        elif self.board.piece_type_at(square) == ch.QUEEN:
            pieceValue = 8.8

        # if my color, then +pieceValue, if opponent, then -ve piece value
        if self.board.color_at(square) != self.color:
            return -pieceValue
        else:
            return pieceValue


    #minimax alpha beta pruning


                                            #candidate -> best score in previous branch
    def engine(self, candidate, depth):
        
        if depth == self.maxDepth or self.board.is_game_over():
            # If the maximum depth is reached or the game is over, return the evaluation score found until now
            return self.eval_function()

        moveList = list(self.board.legal_moves)  # Get a list of legal moves
        newCandidate = float("-inf") if depth % 2 != 0 else float("inf")  # Initialize the new candidate value, if our turn, then initialize to -infitinty

        for move in moveList:
            self.board.push(move)  # Make the move on the board
            value = self.engine(newCandidate, depth + 1)  # Recursively call the engine with the next depth

            if value > newCandidate and depth % 2 != 0:
                # If the value is better and it's the engine's turn (maximizing player)
                if depth == 1:
                    self.best_move = move  # Store the best move if at the root level as initial move (initialization)
                newCandidate = value
                
            elif value < newCandidate and depth % 2 == 0:  #if it is opponent and we want to minimize its points, we find values lesser than its candidate value and update it.
                newCandidate = value

            #alpha beta pruning doen now

            if candidate is not None and value < candidate and depth % 2 == 0:          #if opponent's move, and the final value we found is less than candidate(previous depth value) then prune the remaining moves, won't let me go there only
                # Alpha-beta pruning for the minimizing player
                self.board.pop()
                break
            elif candidate is not None and value > candidate and depth % 2 != 0:        #if it engine's turn and it finds a better value, then prune remaining moves
                # Alpha-beta pruning for the maximizing player
                self.board.pop()
                break

            self.board.pop()  # Undo the move

        if depth > 1:
            # Return the new candidate value for non-root levels
            return newCandidate
        else:
            # Return the best move at the root level because we did not find new candidate at root level
            return self.best_move

    def convert_to_uci(self, move):
        # Method to convert a chess.Move object to UCI format
        return ch.Move.uci(move)

# Main loop for UCI communication
if __name__ == "__main__":
    engine = Engine(ch.Board(), maxDepth=4, color=ch.WHITE)  # Initialize the engine
    while True:
        command = input()  # Wait for a UCI command
        engine.handle_command(command)