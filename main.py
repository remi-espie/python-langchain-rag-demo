import sys
import time

from textblob.classifiers import NaiveBayesClassifier, DecisionTreeClassifier, MaxEntClassifier, \
    PositiveNaiveBayesClassifier

from common import TRANSFORMATION_ALLOWED, ALGORITHM_ALLOWED, transform_dataset, read_dataset

TRANSFORMATION_TO_STRING = {
    'title': 'Title only',
    'description': 'Description only',
    'both': 'Title and Description'
}

ALGORITHM_TO_STRING = {
    'naive_bayes': 'Naive Bayes',
    'decision_tree': 'Decision Tree',
    'max_ent': 'Max Entropy',
    'positive_naive_bayes': 'Positive Naive Bayes'
}

TEST_DATA_TRIM = 100


def get_classifier(algorithm):
    if algorithm == 'naive_bayes':
        return NaiveBayesClassifier
    elif algorithm == 'decision_tree':
        return DecisionTreeClassifier
    elif algorithm == 'max_ent':
        return MaxEntClassifier
    elif algorithm == 'positive_naive_bayes':
        return PositiveNaiveBayesClassifier


if __name__ == '__main__':
    # Get CLI arguments
    if len(sys.argv) != 4:
        print('Usage: python main.py <training_data_size> <transformation> <algorithm>')
        print('<training_data_size>: between 1 and 120000')

        print('<transformation>: one of ')
        for transformation in TRANSFORMATION_ALLOWED:
            print(f'  - {transformation}')

        print('<algorithm>: one of ')
        for algorithm in ALGORITHM_ALLOWED:
            print(f'  - {algorithm}')

        sys.exit(1)

    # Get the arguments
    training_data_size = int(sys.argv[1])
    transformation = sys.argv[2]
    algorithm = sys.argv[3]

    # Check if the arguments are valid
    if training_data_size < 1 or training_data_size > 120000:
        print('Training data size must be between 1 and 120000')
        sys.exit(1)

    if transformation not in TRANSFORMATION_ALLOWED:
        print('Transformation must be one of ', TRANSFORMATION_ALLOWED)
        sys.exit(1)

    if algorithm not in ALGORITHM_ALLOWED:
        print('Algorithm must be one of ', ALGORITHM_ALLOWED)
        sys.exit(1)

    # Read the training and test data
    print('Reading dataset...')
    training_data = transform_dataset(read_dataset('train.csv'), transformation)
    test_data = transform_dataset(read_dataset('test.csv'), transformation)

    print(f'* Got {len(training_data)} training data and {len(test_data)} test data')
    print(f'* Using transformation: {TRANSFORMATION_TO_STRING[transformation]}')
    print(f'* Will trim training data to {training_data_size}')
    print(f'* Will trim test data to {TEST_DATA_TRIM}')
    print(f'* Example training data: {training_data[0]}')
    print()

    training_data = training_data[:training_data_size]
    test_data = test_data[:TEST_DATA_TRIM]

    # Start classifying
    print('Training classifier...')
    print(f'* Using algorithm: {ALGORITHM_TO_STRING[algorithm]}')
    start_classification = time.perf_counter()
    classifier = get_classifier(algorithm)(training_data)
    end_classification = time.perf_counter()
    classification_time = end_classification - start_classification
    print(f'* Training took {classification_time:.2f}s')
    print()

    # Check accuracy
    print('Checking accuracy...')
    start_accuracy = time.perf_counter()
    accuracy = classifier.accuracy(test_data)
    end_accuracy = time.perf_counter()
    accuracy_time = end_accuracy - start_accuracy
    print(f'* Accuracy: {accuracy:.2f}')
    print(f'* Accuracy check took {accuracy_time:.2f}s')

    # Write the results to the CSV file
    with open('results.csv', 'a') as file:
        file.write(
            f'{training_data_size},{transformation},{algorithm},{accuracy},{classification_time},{accuracy_time}\n')
