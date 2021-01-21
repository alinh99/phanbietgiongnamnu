import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import sklearn as sk
import seaborn as sns
from subprocess import check_output
import os

# for dirname, _, filenames in os.walk('input'):
#     for filename in filenames:
#         print(os.path.join(dirname, filename))

data = pd.read_csv("input/voice.csv")
# print(data)

data.label = [1 if each == 'male' else 0 for each in data.label]
# print(data)

male = data[data.label == 1]
female = data[data.label == 0]

# plt.figure(figsize=(9, 9))
# plt.scatter(male.meanfreq, male.meanfun, color="blue", label="male", alpha=0.2)
# plt.scatter(female.meanfreq, female.meanfun, color="green", label="female", alpha=0.2)
# plt.legend()
# plt.xlabel("MeanFreq")
# plt.ylabel("Meanfun")
# plt.show()

y = data.label.values
x = data.drop(["label"], axis=1)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=5)
log = LogisticRegression(max_iter=500)

log.fit(x_train, y_train)

predicted_label = pd.DataFrame(log.predict(x_test))
score = log.score(x_test, y_test)

print("Accuracy of Logistic Regression: ", score)
# print(predicted_label)
# print(x_test)
# print(check_output(["ls", "input"]).decode("utf8"))
# print(data.head(10))
# print(data.describe())
# print(data.info())


correlation = data.corr()  # tìm sự tương quan của các cột với nhau
# print(correlation)
#
# plt.figure(figsize=(15, 15))
#
# print(sns.heatmap(correlation, square=True))
# plt.show()
# Importing sklearn libraries
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn import metrics

x = data.iloc[:, :-1].values
y = data.iloc[:, -1].values
# print(y)

# Encoding label (male=1 and female=0)
encoder = LabelEncoder()
y = encoder.fit_transform(y)
# print(y)

# Standarizing features
scaler = StandardScaler()
scaler.fit(x)
x = scaler.transform(x)
# Creating Training and Test sets
# # 70-30% of train and test
# Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.30)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.30)
x_train, x_test, y_train, y_test = np.array(x_train, dtype='float32'), np.array(x_test,dtype='float32'), np.array(y_train, dtype='float32'), np.array(y_test, dtype='float32')

# Random Forest
random_forest = RandomForestClassifier()
random_forest.fit(x_train, y_train)
y_predicted = random_forest.predict(x_test)

# Test Accuracy (RF)
random_accuracy = metrics.accuracy_score(y_test, y_predicted)
print("Accuracy of Random Forest: ", random_accuracy)

# # This script shows you how to make a submission using a few
# # useful Python libraries.
# # It gets a public leaderboard score of 0.76077.
# # Maybe you can tweak it and do better...?
#

import xgboost as xgb

# # xgboost model
gbm = xgb.XGBClassifier(max_depth=3, n_estimators=300, learning_rate=0.05).fit(x_train, y_train)
y_pred = gbm.predict(x_test)

# # Test Accuracy (xgboost)
xgb_accuracy = metrics.accuracy_score(y_test, y_pred)
print("Accuracy of XGBoost: ", xgb_accuracy)



def convertToOneHot(vector, num_classes=None):
    assert isinstance(vector, np.ndarray)
    assert len(vector) > 0

    if num_classes is None:
        num_classes = np.max(vector) + 1
    else:
        assert num_classes > 0
        assert num_classes >= np.max(vector)

    result = np.zeros(shape=(len(vector), num_classes))
    result[np.arange(len(vector)), vector] = 1
    return result.astype(int)


from sklearn.preprocessing import LabelEncoder

# Converting label into one-hot vector
y_train = LabelEncoder().fit_transform(y_train)
y_train = convertToOneHot(y_train, 2)

y_test = LabelEncoder().fit_transform(y_test)
y_test = convertToOneHot(y_test, 2)

import tensorflow as tf
tf.compat.v1.disable_eager_execution()

def layer(input, n_input, n_output, name='hidden_layer'):
    W = tf.Variable(tf.random.truncated_normal([n_input, n_output], stddev=0.1), name='W')
    B = tf.Variable(tf.constant(0.1, dtype=tf.float32, shape=[n_output]), name='B')
    return tf.add(tf.matmul(input, W), B)


# TF Graph
x = tf.compat.v1.placeholder(tf.float32, shape=[None, 20], name="x")
y = tf.compat.v1.placeholder(tf.float32, shape=[None, 2], name="y")

hidden_1 = tf.nn.relu(layer(x, 20, 15, 'hidden_layer_1'))
hidden_2 = tf.nn.relu(layer(hidden_1, 15, 10, 'hidden_layer_2'))
hidden_3 = tf.nn.relu(layer(hidden_2, 10, 5, 'hidden_layer_3'))
output = layer(hidden_3, 5, 2, 'output')

# Calculating loss function (cross-entropy)
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=output, labels=y), name='xent')

# Training
optimizer = tf.compat.v1.train.GradientDescentOptimizer(learning_rate=1e-3)
train = optimizer.minimize(loss)

# Accuracy
correct_prediction = tf.equal(tf.argmax(output, 1), tf.argmax(y, 1), name="correct_prediction")
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name="accuracy")

sess = tf.compat.v1.Session()
init = tf.compat.v1.global_variables_initializer()
sess.run(init)

num_epochs = 1000
batch_size = 100
train_size = x_train.shape[0]

for epoch in range(num_epochs):
    avg_accuracy = 0.0
    total_batches = int(train_size // batch_size)
    for step in range(total_batches):
        offset = (step * batch_size) % train_size
        batch_data = x_train[offset:(offset + batch_size), :]
        batch_labels = y_train[offset:(offset + batch_size), :]
        _, ac = sess.run([train, accuracy], feed_dict={x: batch_data, y: batch_labels})
        avg_accuracy += ac / total_batches
    validation_accuracy = sess.run([accuracy], feed_dict={x: x_test, y: y_test})
    if epoch % 50 == 0:
        print("Epoch:{} training_accuracy={}".format(epoch + 1, avg_accuracy))
        print("Epoch:{} testing_accuracy={}".format(epoch + 1, validation_accuracy))
test_accuracy = sess.run([accuracy], feed_dict={x: x_test, y: y_test})
print("Testing accuracy = {}".format(test_accuracy))

# compare 4 algorithm with bar chart
fig = plt.figure()
ax = fig.add_axes([0.1, 0.05, 0.8, 0.9])
langs = ['Linear Regression', 'Random Forests', 'XGBoost', 'Neural Network']
algorithms = [score, random_accuracy, xgb_accuracy, test_accuracy]
ax.bar(langs, algorithms)
plt.show()
