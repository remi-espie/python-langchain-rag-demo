import csv

TRANSFORMATION_ALLOWED = ['title', 'description', 'both']
# ALGORITHM_ALLOWED = ['naive_bayes', 'decision_tree', 'max_ent', 'positive_naive_bayes']
ALGORITHM_ALLOWED = ['naive_bayes', 'max_ent']

CLASS_KEY = 'Class Index'
TITLE_KEY = 'Title'
DESCRIPTION_KEY = 'Description'

CLASS_TO_STRING = {
    1: 'World',
    2: 'Sports',
    3: 'Business',
    4: 'Sci/Tech'
}


def read_dataset(path):
    with open(path, 'r') as file:
        data = csv.DictReader(file)
        return list(data)


def transform_dataset(data, transformation):
    if transformation == 'title':
        return list((row[TITLE_KEY], row[CLASS_KEY]) for row in data)
    elif transformation == 'description':
        return list((row[DESCRIPTION_KEY], row[CLASS_KEY]) for row in data)
    elif transformation == 'both':
        return list((f'{row[TITLE_KEY]} {row[DESCRIPTION_KEY]}', row[CLASS_KEY]) for row in data)
