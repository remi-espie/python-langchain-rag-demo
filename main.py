import subprocess
import threading
import logging


def start_process(command):
    return subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        text=True,
    )

def pipe_gnuchess(source, destination, logger):
    logger.info("Starting pipe_gnuchess")
    response = ''
    while True:
        line = source.stdout.readline()
        response += line
        if line.startswith('My move is :'):
            logger.info(response)
            destination.stdin.write(response)
            destination.stdin.flush()
            response = ''


def pipe_ai(source, destination, logger):
    logger.info("Starting pipe_ai")
    while True:
        line = source.stdout.readline()
        logger.info(line)
        if line == "----------":
            break
    while True:
        line = source.stdout.readline()
        logger.info(line)
        destination.stdin.write(line)
        destination.stdin.flush()

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("Starting processes")

    # Start the processes
    # ai_process = start_process(['python3', 'ai.py'])
    gnuchess_process = start_process(['python3', 'gnuchess.py'])

    # logger.info("Starting threads")
    #
    # # Create threads to pipe the streams
    # thread_gnuchess = threading.Thread(target=pipe_gnuchess, args=(gnuchess_process, ai_process, logger))
    # thread_ai = threading.Thread(target=pipe_ai, args=(ai_process, gnuchess_process, logger))
    #
    # # Start the threads
    # thread_gnuchess.start()
    # thread_ai.start()
    #
    # # Wait for the threads to finish
    # thread_gnuchess.join()
    # thread_ai.join()
    #
    # # Close the processes
    # ai_process.terminate()
    # gnuchess_process.terminate()

    print(gnuchess_process.stdout.readline())