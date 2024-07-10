import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

class CricketMatchPredictor:
    def __init__(self, data):
        self.df = data
        self.df['Match Boolean'] = self.df['Match Boolean'].astype(int)
        self.y = self.df['Match Boolean']
        self.X = self.df.drop(['Match Boolean', 'id'], axis=1)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        self.scaler = StandardScaler()
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        self.models = {
            'Logistic Regression': LogisticRegression(random_state=42),
            'Decision Tree': DecisionTreeClassifier(random_state=42),
            'Random Forest': RandomForestClassifier(random_state=42)
        }
        self.trained_models = {}

    def train_models(self):
        for name, model in self.models.items():
            model.fit(self.X_train_scaled, self.y_train)
            self.trained_models[name] = model

    def evaluate_models(self):
        for name, model in self.trained_models.items():
            y_pred = model.predict(self.X_test_scaled)
            accuracy = accuracy_score(self.y_test, y_pred)
            report = classification_report(self.y_test, y_pred)
            print(f"Model: {name}")
            print(f"Accuracy: {accuracy:.2f}")
            print(f"Classification Report:\n{report}\n")

    def predict(self, features):
        # Assuming 'features' is a list of values for your predictor
        scaled_features = self.scaler.transform([features])
        print("scaled features \n")
        print(scaled_features)
        predictions = {}
        probabilities = {}
        for name, model in self.trained_models.items():
            if hasattr(model, 'predict_proba'):
                pred_prob = model.predict_proba(scaled_features)
                probabilities[name] = pred_prob.tolist()[0]  # Convert numpy array to list
                pred = model.predict(scaled_features)
                predictions[name] = int(pred[0])
            else:
                pred = model.predict(scaled_features)
                predictions[name] = int(pred[0])
        return predictions, probabilities



df = pd.read_csv('output.csv')
predictor = CricketMatchPredictor(df)
predictor.train_models()
predictor.evaluate_models()

# Overs remaining,Runs Scored,Wickets Remaining,Runs required

predictions = predictor.predict([5, 200, 5, 150])
print(predictions)
