import chess as ch
import random as rd

class Engine:
    def __init__(self, board, maxDepth, color):
        self.board = board
        self.color = color
        self.maxDepth = maxDepth
        self.current_depth = 0
        self.searching = False

    def handle_command(self, command):
        if command == "uci":
            print("uciok")
        elif command == "isready":
            print("readyok")
        elif command.startswith("position"):
            parts = command.split(" ")
            if parts[1] == "startpos":
                self.board = ch.Board()
            elif parts[1] == "fen":
                fen = " ".join(parts[2:])
                self.board.set_fen(fen)
            if "moves" in command:
                moves_start_index = command.index("moves") + len("moves") + 1
                moves_str = command[moves_start_index:].strip()
                moves_list = moves_str.split()
                for move_str in moves_list:
                    move = ch.Move.from_uci(move_str)
                    self.board.push(move)
        elif command.startswith("go"):
            if "infinite" in command:
                # Handle time management if needed
                pass
            else:
                self.searching = True
                self.current_depth = self.maxDepth
                self.get_best_move()
        elif command == "ucinewgame":
            self.searching = False
            self.current_depth = 0
        elif command == "quit":
            print("Bye!")
            exit()



    def get_best_move(self):
        best_move = self.engine(None, 1)
        uci_best_move = self.convert_to_uci(best_move)
        print(f"bestmove {uci_best_move}")

    def eval_function(self):
        compt = 0
        for i in range(64):
            compt += self.squareResPoints(ch.SQUARES[i])
        compt += self.mateOpportunity() + self.opening() + 0.001 * rd.random()
        return compt

    def mateOpportunity(self):
        if self.board.is_game_over():
            if self.board.result() == "1-0":
                return 999
            elif self.board.result() == "0-1":
                return -999
        return 0

    def opening(self):
        if self.board.fullmove_number < 10:
            if self.board.turn == self.color:
                return 1 / 30 * len(list(self.board.legal_moves))
            else:
                return -1 / 30 * len(list(self.board.legal_moves))
        else:
            return 0

    def squareResPoints(self, square):
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

        if self.board.color_at(square) != self.color:
            return -pieceValue
        else:
            return pieceValue

    def engine(self, candidate, depth):
        if depth == self.maxDepth or self.board.is_game_over():
            return self.eval_function()

        moveList = list(self.board.legal_moves)
        newCandidate = float("-inf") if depth % 2 != 0 else float("inf")
        
        for move in moveList:
            self.board.push(move)
            value = self.engine(newCandidate, depth + 1)

            if value > newCandidate and depth % 2 != 0:
                if depth == 1:
                    self.best_move = move
                newCandidate = value
            elif value < newCandidate and depth % 2 == 0:
                newCandidate = value

            if candidate is not None and value < candidate and depth % 2 == 0:
                self.board.pop()
                break
            elif candidate is not None and value > candidate and depth % 2 != 0:
                self.board.pop()
                break

            self.board.pop()

        if depth > 1:
            return newCandidate
        else:
            return self.best_move

    def convert_to_uci(self, move):
        return ch.Move.uci(move)

# Main loop for UCI communication
if __name__ == "__main__":
    engine = Engine(ch.Board(), maxDepth=4, color=ch.WHITE)  # Initialize the engine
    while True:
        command = input()
        engine.handle_command(command)
