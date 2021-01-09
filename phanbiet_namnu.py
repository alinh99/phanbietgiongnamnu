import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import os
for dirname, _, filenames in os.walk('input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

data = pd.read_csv("input/voice.csv")
print(data)

data.label = [1 if each == 'male' else 0 for each in data.label]
print(data)

male = data[data.label == 1]
female = data[data.label == 0]

plt.figure(figsize=(9, 9))
plt.scatter(male.meanfreq, male.meanfun, color="blue", label = "male", alpha=0.2)
plt.scatter(female.meanfreq, female.meanfun, color="green", label="female", alpha=0.2)
plt.legend()
plt.xlabel("MeanFreq")
plt.ylabel("Meanfun")
plt.show()

y = data.label.values
x = data.drop(["label"], axis=1)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=5)

log = LogisticRegression(max_iter=500)

log.fit(x_train, y_train)

predicted_label = pd.DataFrame(log.predict(x_test))
score = log.score(x_test, y_test)
print(score)
print(predicted_label)
print(x_test)