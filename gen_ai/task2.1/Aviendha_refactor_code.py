import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, f1_score, confusion_matrix, log_loss
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

def evaluate_model(y_true, y_pred):
    """Compute evaluation metrics given true and predicted labels."""
    conf_mat = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = conf_mat.ravel()
    
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "sensitivity (recall)": recall_score(y_true, y_pred),
        "specificity": tn / (tn + fp),
        "f1_score": f1_score(y_true, y_pred),
        "log_loss": log_loss(y_true, y_pred)
    }
    return metrics

# Load dataset
data = np.loadtxt("Raisin_Dataset_01.csv", delimiter=",", skiprows=1)
X, Y = data[:, :-1], data[:, -1]

# Split dataset
training_X, test_X, training_Y, test_Y = train_test_split(X, Y, test_size=0.2)

# Train model
model = make_pipeline(StandardScaler(), SGDClassifier(loss='log_loss'))
model.fit(training_X, training_Y)

# Predictions
test_results = model.predict(test_X)
training_results = model.predict(training_X)

# Extract model parameters
weights = model.named_steps['sgdclassifier'].coef_[0]
intercept = model.named_steps['sgdclassifier'].intercept_
w = np.concatenate([intercept, weights])

# Print model parameters
print(f"intercept: {intercept}\n")
print(f"weights: {weights}\n")
print(f"parameter vector w: {w}")
print(f'\nPredicted Values:\n{test_results}')

# Evaluate model
train_metrics = evaluate_model(training_Y, training_results)
test_metrics = evaluate_model(test_Y, test_results)

# Print evaluation metrics
for key, value in test_metrics.items():
    print(f'\ntest {key}: {value}')
for key, value in train_metrics.items():
    print(f'training {key}: {value}')
