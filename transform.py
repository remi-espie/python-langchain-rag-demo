#!/usr/bin/python3
import pgn

if __name__ == '__main__':
    moves = []
    n = 0

    for game in pgn.GameIterator("lichess_db_standard_rated_2014-07.pgn"):
        if game.termination == 'Normal' and game.opening != '?':
            moves.append(game.moves)
            n += 1

        if n == 10000:
            break

    for i, party_move in enumerate(moves):
        moves[i] = [move for move in party_move if not move.startswith('{')]

    with open('training.txt', 'w') as f:
        for party_moves in moves:
            current_move = 1
            f.write('If the following moves were played: `')

            for i in range(0, len(party_moves) - 3, 2):
                if i < len(party_moves) - 5:
                    f.write(f'{current_move}.{' '.join(party_moves[i:i+2])} ')
                else:
                    f.write(f'{current_move}.{party_moves[i]}')

                current_move += 1

            f.write(f'`, play the following move: `{party_moves[-2]}`\n')