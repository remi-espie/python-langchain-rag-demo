import subprocess

from common import ALGORITHM_ALLOWED, TRANSFORMATION_ALLOWED


def run_tests_with_size(training_data_size):
    for algorithm_idx in range(len(ALGORITHM_ALLOWED)):
        algorithm = ALGORITHM_ALLOWED[algorithm_idx]

        for transformation_idx in range(len(TRANSFORMATION_ALLOWED)):
            transformation = TRANSFORMATION_ALLOWED[transformation_idx]

            print(
                f'Starting test with (training_data_size={training_data_size}, algorithm={algorithm}, transformation={transformation})...')

            res = subprocess.run(['python', 'main.py', str(training_data_size), transformation, algorithm], check=False,
                                 capture_output=True)

            if res.returncode != 0:
                print(f'* Test failed with return code {res.returncode}')
                return False

            print(f'* Test completed successfully')
            print()

    return True


if __name__ == '__main__':
    # Prepare the results CSV file
    with open('results.csv', 'w') as file:
        file.write(f'training_data_size,transformation,algorithm,accuracy,classification_time,accuracy_time\n')

    # Start the tests
    for training_data_size in range(10, 10000, 10):
        res = run_tests_with_size(training_data_size)

        if not res:
            break
