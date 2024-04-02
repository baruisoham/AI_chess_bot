# AI Chess Engine

This is a chess engine implemented in Python using the `python-chess` library. The engine uses a depth-limited negamax algorithm with alpha-beta pruning for move selection, and a simple evaluation function that considers material, mate opportunities, and opening position.

## Features

- Supports the Universal Chess Interface (UCI) protocol for communication with chess GUIs
- Handles basic UCI commands like `uci`, `isready`, `position`, `go`, `ucinewgame`, and `quit`
- Implements a negamax search algorithm with alpha-beta pruning
- Simple evaluation function based on material, mate opportunities, and opening position
- Configurable search depth (default is 4 ply)

## Usage

1. Install the required dependencies:
   `pip install python-chess`
   `pip install pyinstaller`
3. Create an executable file
   `pyinstaller --onefile chessbot.py`
4. Or, you could directly download the executable file from Soham's repository 
5. Add the executable as an engine in PyChess. 
6. The engine will now start listening for UCI commands. You can interact with it using a compatible chess GUI (like PyChess)

## UCI Commands

- `uci`: Tells the engine to use the UCI protocol.
- `isready`: Checks if the engine is ready to receive commands.
- `position [fen <fen-string> | startpos] [moves <move1> <move2> ...]`: Sets the position on the board.
- `go [infinite | depth <depth>]`: Starts calculating the best move.
- `ucinewgame`: Resets the game and clears the move history.
- `quit`: Quits the engine.


## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
