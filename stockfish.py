import subprocess
from time import sleep

# Start Stockfish
process = subprocess.Popen(
    'stockfish',
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

# Send a command to Stockfish
def send_command(command):
    print(f"<<< {command}")
    process.stdin.write(f"{command}\n")
    process.stdin.flush()

# Read a response from Stockfish
def read_response():
    line = process.stdout.readline()
    print(f">>> {line}", end='')
    return line

# Wait for a specific response
def wait_response(response):
    while True:
        line = read_response()
        if response in line:
            break

# Wait for a best move
def wait_best_move():
    while True:
        line = read_response()
        if 'bestmove' in line:
            return line.split()[1]

# Dump Stockfish board
def dump_board():
    send_command('d')

    while True:
        line = read_response()
        if 'Checkers' in line:
            break

# Send positions
def send_position(moves):
    send_command(f"position startpos moves {moves.strip()}")

# Make a move
if __name__ == '__main__':
    # Start the game
    send_command('uci')
    wait_response('uciok')

    send_command('ucinewgame')
    send_command('isready')
    wait_response('readyok')

    # Play moves
    moves = ''
    send_command('position startpos')

    while True:
        # TODO: LLM turn
        print(f"/!\\ Current board state: {moves.strip()}")
        move = input('Enter your move: ')
        moves += f" {move}"
        send_position(moves)
        dump_board()

        # Stockfish turn
        send_command('go depth 2')
        move = wait_best_move()
        moves += f" {move}"

        send_position(moves)
        dump_board()
