import argparse
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "app", "model")
os.makedirs(MODEL_DIR, exist_ok=True)

def load_dataset(path):
    df = pd.read_csv(path)
    df = df.dropna(subset=["intent", "text"])
    return df

def train(path, test_size=0.2, random_state=42):
    df = load_dataset(path)
    X = df["text"].astype(str)
    y = df["intent"].astype(str)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1,2), max_features=5000)),
        ("clf", LogisticRegression(max_iter=1000))
    ])

    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)

    print("EVALUATION:")
    print(classification_report(y_test, preds))

    model_path = os.path.join(MODEL_DIR, "nlu_pipeline.joblib")
    joblib.dump(pipeline, model_path)
    print(f"Saved model to {model_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="dataset.csv", help="Path to dataset csv")
    args = parser.parse_args()
    train(args.data)
