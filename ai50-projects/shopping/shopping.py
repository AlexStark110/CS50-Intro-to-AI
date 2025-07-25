"""
Shopping - Machine Learning Classification

Predict whether a user will make a purchase based on browsing behavior
"""

import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative (int)
        - Administrative_Duration (float)
        - Informational (int)
        - Informational_Duration (float)
        - ProductRelated (int)
        - ProductRelated_Duration (float)
        - BounceRates (float)
        - ExitRates (float)
        - PageValues (float)
        - SpecialDay (float)
        - Month (int: 0=Jan, 1=Feb, 2=Mar, ..., 11=Dec)
        - OperatingSystems (int)
        - Browser (int)
        - Region (int)
        - TrafficType (int)
        - VisitorType (int: 0=Not Returning, 1=Returning)
        - Weekend (int: 0=False, 1=True)

    labels should be a list of 0s and 1s, where 1 represents a user who did
    make a purchase, and 0 represents a user who did not make a purchase.
    """
    evidence = []
    labels = []
    
    # Month mapping
    months = {
        'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5,
        'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11
    }
    
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Process evidence
            evidence_row = []
            
            # Administrative (int)
            evidence_row.append(int(row['Administrative']))
            
            # Administrative_Duration (float)
            evidence_row.append(float(row['Administrative_Duration']))
            
            # Informational (int)
            evidence_row.append(int(row['Informational']))
            
            # Informational_Duration (float)
            evidence_row.append(float(row['Informational_Duration']))
            
            # ProductRelated (int)
            evidence_row.append(int(row['ProductRelated']))
            
            # ProductRelated_Duration (float)
            evidence_row.append(float(row['ProductRelated_Duration']))
            
            # BounceRates (float)
            evidence_row.append(float(row['BounceRates']))
            
            # ExitRates (float)
            evidence_row.append(float(row['ExitRates']))
            
            # PageValues (float)
            evidence_row.append(float(row['PageValues']))
            
            # SpecialDay (float)
            evidence_row.append(float(row['SpecialDay']))
            
            # Month (int)
            evidence_row.append(months[row['Month']])
            
            # OperatingSystems (int)
            evidence_row.append(int(row['OperatingSystems']))
            
            # Browser (int)
            evidence_row.append(int(row['Browser']))
            
            # Region (int)
            evidence_row.append(int(row['Region']))
            
            # TrafficType (int)
            evidence_row.append(int(row['TrafficType']))
            
            # VisitorType (int: 0=Not Returning, 1=Returning)
            visitor_type = 1 if row['VisitorType'] == 'Returning_Visitor' else 0
            evidence_row.append(visitor_type)
            
            # Weekend (int: 0=False, 1=True)
            weekend = 1 if row['Weekend'] == 'TRUE' else 0
            evidence_row.append(weekend)
            
            evidence.append(evidence_row)
            
            # Process label
            label = 1 if row['Revenue'] == 'TRUE' else 0
            labels.append(label)
    
    return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted scikit-learn model (e.g., KNeighborsClassifier) trained on the data.
    """
    # Use k-nearest neighbors classifier
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    true_positives = 0
    true_negatives = 0
    false_positives = 0
    false_negatives = 0
    
    for actual, predicted in zip(labels, predictions):
        if actual == 1 and predicted == 1:
            true_positives += 1
        elif actual == 0 and predicted == 0:
            true_negatives += 1
        elif actual == 0 and predicted == 1:
            false_positives += 1
        elif actual == 1 and predicted == 0:
            false_negatives += 1
    
    # Calculate sensitivity (true positive rate)
    sensitivity = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    
    # Calculate specificity (true negative rate)
    specificity = true_negatives / (true_negatives + false_positives) if (true_negatives + false_positives) > 0 else 0
    
    return sensitivity, specificity


if __name__ == "__main__":
    main()