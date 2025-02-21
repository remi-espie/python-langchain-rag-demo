#!/usr/bin/python3
import chess
import pgn

TRAINING_DATA_SIZE = 10000
TESTING_DATA_SIZE = 10

if __name__ == '__main__':
    fens_training = []
    last_moves_training = []
    fens_testing = []
    last_moves_testing = []
    n = 0

    for game in pgn.GameIterator("lichess_db_standard_rated_2014-07.pgn"):
        if game.termination == 'Normal' and game.opening != '?':
            board = chess.Board()
            moves = [move for move in game.moves[:-1] if not move.startswith('{')]

            if len(moves) % 2 == 0:
                continue

            if len(moves) == 1:
                continue

            san = ''

            for i, move in enumerate(moves[:-1]):
                if move.endswith('?!'):
                    move = move[:-2]
                if move.endswith('??'):
                    move = move[:-2]
                elif move.endswith('!'):
                    move = move[:-1]
                elif move.endswith('?'):
                    move = move[:-1]

                parsed_move = board.push_san(move)

                if i % 2 == 0:
                    if i > 0:
                        if n < TRAINING_DATA_SIZE:
                            fens_training.append(san.strip())
                            last_moves_training.append(parsed_move.uci())
                        else:
                            fens_testing.append(san.strip())
                            last_moves_testing.append(parsed_move.uci())

                san += f"{parsed_move.uci()} "

            n += 1

        if n == TRAINING_DATA_SIZE + TESTING_DATA_SIZE:
            break

    with open('training.txt', 'w') as f:
        # f.write('The following lines are training data for chess moves. The current board state is in the Forsyth-Edwards Notation (FEN) format. The move to be played is in Standard Algebraic Notation (SAN) format.\n')

        for i in range(len(fens_training)):
            fen = fens_training[i]
            last_move = last_moves_training[i]

            # f.write(f'If this is the current board state: `{fen}`, play the following move: `{last_move}`\n')
            f.write(f'{fen} -> {last_move}\n')

    with open('testing.txt', 'w') as f:
        for i in range(len(fens_testing)):
            fen = fens_testing[i]
            last_move = last_moves_testing[i]

            # f.write(f'If this is the current board state: `{fen}`, play the following move: `{last_move}`\n')
            f.write(f'{fen} -> {last_move}\n')
