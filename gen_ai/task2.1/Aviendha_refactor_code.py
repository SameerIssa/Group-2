# 0 for Kecimen and 1 for Besni
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, f1_score, confusion_matrix, log_loss
np.loadtxt
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

# gather training data and sort features and outputs 
data = np.loadtxt("Raisin_Dataset_01.csv", delimiter=",", skiprows=1)
X = data[:, 0:7]
Y = data[:, 7]

# split dataset
training_X, test_X, training_Y, test_Y = train_test_split(X, Y, test_size=0.2)

# train model
model = make_pipeline(StandardScaler(), SGDClassifier(loss='log_loss'))
model.fit(training_X, training_Y)

# models predictions
test_results = model.predict(test_X)
training_results = model.predict(training_X)

# combine bias and weight into parameter vector w
weights = model.named_steps['sgdclassifier'].coef_[0]
intercept = model.named_steps['sgdclassifier'].intercept_
w = np.concatenate([intercept, weights])

# printing results 
print(f"intercept: {intercept}\n")
print(f"weights: {weights}\n")
print(f"parameter vector w: {w}")
print(f'\nPredicted Values:\n{test_results}')

# calculating evaluation metrics
# confusion matrix 
test_mat = confusion_matrix(test_Y, test_results)
test_tn = test_mat[0, 0]
test_tp = test_mat[1, 1]
test_fn = test_mat[1, 0]
test_fp = test_mat[0, 1]

train_mat = confusion_matrix(training_Y, training_results)
train_tn = train_mat[0, 0]
train_tp = train_mat[1, 1]
train_fn = train_mat[1, 0]
train_fp = train_mat[0, 1]

# accuracy
test_accuracy = accuracy_score(test_Y, test_results)
training_accuracy = accuracy_score(training_Y, training_results)

# sensitivity (recall)
test_sensitivity = recall_score(test_Y, test_results)
training_sensitivity = recall_score(training_Y, training_results)

# specificity
test_specificity = test_tn / (test_tn + test_fp)
training_specificity = train_tn / (train_tn + train_fp)

# f1 score 
test_f1score = f1_score(test_Y, test_results)
training_f1score = f1_score(training_Y, training_results)

# log-loss
test_logloss = log_loss(test_Y, test_results)
training_logloss = log_loss(training_Y, training_results)

# printing evaluation metrics 
print(f'\ntest accuracy: {test_accuracy}')
print(f'training accuracy: {training_accuracy}')

print(f'\ntest sensitivity: {test_sensitivity}')
print(f'training sensitivity: {training_sensitivity}')

print(f'\ntest specificity: {test_specificity}')
print(f'training specificity: {training_specificity}')

print(f'\ntest f1score: {test_f1score}')
print(f'training f1score: {training_f1score}')

print(f'\ntest log loss: {test_logloss}')
print(f'training log loss: {training_logloss}\n')
