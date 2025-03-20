import sys

import numpy
from matplotlib import pyplot
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.naive_bayes import MultinomialNB

from common import TRANSFORMATION_ALLOWED, transform_dataset, read_dataset, CLASS_TO_STRING
from main import TRANSFORMATION_TO_STRING, TEST_DATA_TRIM

if __name__ == '__main__':
    # Get CLI arguments
    if len(sys.argv) != 3:
        print('Usage: python main.py <training_data_size> <transformation>')
        print('<training_data_size>: between 1 and 120000')

        print('<transformation>: one of ')
        for transformation in TRANSFORMATION_ALLOWED:
            print(f'  - {transformation}')

        sys.exit(1)

    # Get the arguments
    training_data_size = int(sys.argv[1])
    transformation = sys.argv[2]

    # Check if the arguments are valid
    if training_data_size < 1 or training_data_size > 120000:
        print('Training data size must be between 1 and 120000')
        sys.exit(1)

    if transformation not in TRANSFORMATION_ALLOWED:
        print('Transformation must be one of ', TRANSFORMATION_ALLOWED)
        sys.exit(1)

    # Read the training and test data
    print('Reading dataset...')
    training_data = transform_dataset(read_dataset('train.csv'), transformation)
    test_data = transform_dataset(read_dataset('test.csv'), transformation)
    entire_dataset = training_data + test_data

    print(f'* Got {len(training_data)} training data and {len(test_data)} test data')
    print(f'* Using transformation: {TRANSFORMATION_TO_STRING[transformation]}')
    print(f'* Will trim training data to {training_data_size}')
    print(f'* Will trim test data to {len(entire_dataset) - training_data_size}')
    print(f'* Example training data: {training_data[0]}')
    print()

    # Extract features
    print('Extracting features...')

    bow_vectorizer = CountVectorizer(max_df=0.90, min_df=2, max_features=10000, stop_words='english')
    bow = bow_vectorizer.fit_transform(list([data[0] for data in entire_dataset]))

    print(f'* Extracted {len(bow_vectorizer.get_feature_names_out())} features')
    print(f'* Example features: {bow_vectorizer.get_feature_names_out()[:10]}')
    print(f'* Feature matrix shape: {bow.shape}')
    print()

    # Train the model
    print('Training the model...')

    y = numpy.array([data[1] for data in entire_dataset])
    X_train, X_test, y_train, y_test = train_test_split(
        bow, y, train_size=training_data_size / len(entire_dataset), random_state=42
    )

    model = MultinomialNB()
    model.fit(X_train, y_train)
    print()

    # Evaluate the model
    print('Evaluating the model...')
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_pred, y_test)
    f1 = f1_score(y_pred, y_test, average="weighted")

    print(f'* Accuracy: {accuracy:.2f}')
    print(f'* F1: {f1:.2f}')
    print()

    # Show example predictions
    print('Example predictions:')
    for i in range(5):
        print(f'* Prediction {i}')
        print(f'  - Predicted: {CLASS_TO_STRING[int(y_pred[i])]}')
        print(f'  - Actual: {CLASS_TO_STRING[int(y_test[i])]}')

    print()

    # Display confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=CLASS_TO_STRING)
    disp.plot()
    pyplot.show()
