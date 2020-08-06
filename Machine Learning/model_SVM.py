from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import pandas as pd
import cv2
import joblib


# importing file
data = pd.read_csv('Colours_Dataset_25.csv' , header = None)
data = data.sample(frac = 1).reset_index(drop = True)
X = data.iloc[: , :3].values
Y = data.iloc[: , -1].values


# splitting training and test data
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.04, random_state = 0)

# Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
joblib.dump(sc , 'Scalar1')


# Training the model
from sklearn.svm import SVC
classifier = SVC(kernel = 'linear', random_state = 0)
classifier.fit(X_train, Y_train)

joblib.dump(classifier , 'model_0.04')


# predictions
y_pred = classifier.predict(X_test)
print(confusion_matrix(Y_test , y_pred))
print(classifier.score(X_test , Y_test))

