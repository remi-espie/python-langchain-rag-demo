import subprocess

# Function to start GNU Chess process
process = subprocess.Popen(
    ['gnuchess'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=True,
    text=True,
)

# Send a command to GNU Chess
def send_command(command):
    process.stdin.write(command + '\n')
    process.stdin.flush()

# Read a response from GNU Chess
def read_response(command):
    while True:
        line = process.stdout.readline()
        if line == 'Invalid move: \n':
            continue
        print(line, end='')
        if line.startswith('My move is :') or line.startswith('Invalid move: '+ command):
            break
    return

# Make a move
while True:
    move = input("Enter a command to play a move: ")
    send_command(move)
    read_response(move)

