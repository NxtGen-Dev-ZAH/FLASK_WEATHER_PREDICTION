from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    jaccard_score,
    f1_score,
    log_loss,
)
import sklearn.metrics as metrics

app = Flask(__name__)

# Load and preprocess the data
df_weather = pd.read_csv("Weather_Data.csv")
df_weather.drop(
    columns=["WindGustDir", "WindDir9am", "WindDir3pm", "Date"], axis=1, inplace=True
)
df_weather.replace(["No", "Yes"], [0, 1], inplace=True)
df_weather = df_weather.astype(float)

features = df_weather.drop(columns="RainTomorrow", axis=1).values
Y = df_weather["RainTomorrow"].values

x_train, x_test, y_train, y_test = train_test_split(
    features, Y, test_size=0.2, random_state=10
)

# Train models
LinearReg = LinearRegression().fit(x_train, y_train)
KNN = KNeighborsClassifier(n_neighbors=4).fit(x_train, y_train)#CLUSTERS
Tree = DecisionTreeClassifier(random_state=10).fit(x_train, y_train)#CLASSIFICATION
LR = LogisticRegression(solver="liblinear").fit(x_train, y_train)
SVM = svm.SVC().fit(x_train, y_train)


# Define a function to make predictions based on the selected model
def make_prediction(model, input_data):
    return np.asanyarray(model.predict([input_data]))[0]


@app.route("/")
def index():
    return render_template("profile2.html")


# Flask route to handle predictions
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json["input_data"]
        selected_model = request.json["selected_model"]

        if not data:
            return jsonify({"error": "Input data is required"}), 400

        if selected_model == "Linear Regression":
            model = LinearReg
        elif selected_model == "KNN":
            model = KNN
        elif selected_model == "Decision Tree":
            model = Tree
        elif selected_model == "Logistic Regression":
            model = LR
        elif selected_model == "SVM":
            model = SVM
        else:
            return jsonify({"error": "Invalid model selected"}), 400

        prediction = make_prediction(model, data)
        return jsonify({"prediction": prediction})
    except Exception as e:
        print(f"Error: {str(e)}")  # Add this line
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
