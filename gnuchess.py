import select
import subprocess
import sys
from time import sleep
from threading import Thread

# Function to start GNU Chess process
process = subprocess.Popen(
    ['gnuchess', '--xboard'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

first_input = True

# Send a command to GNU Chess
def send_command(command):
    command = command.strip()
    print(f"<<< {command}")
    command = bytes(f"{command}\n", 'utf-8')
    process.stdin.write(command)
    process.stdin.flush()

# Read a response from GNU Chess
def read_response():
    while True:
        ready, _, _ = select.select([process.stdout], [], [])
        if ready:
            response = ''
            while response == '':
                response = process.stdout.readline().rstrip()
                print(f">>> {response}", flush=True)


thread = Thread(target = read_response)
thread.start()

# Make a move
while True:
    move = input("Enter a command to play a move: ")
    send_command(move)