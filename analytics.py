# Task 3: Predictive Analytics for Resource Allocation
# Dataset: Breast Cancer (Wisconsin) - treated as proxy for "issue priority"
# Goal: Predict priority (High/Medium/Low) based on tumor features

# Import libraries
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt

# Step 1: Load and inspect data
data = load_breast_cancer()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target  # 0 = malignant, 1 = benign

print("Dataset shape:", df.shape)
print("\nClass distribution (original):")
print(pd.Series(data.target).value_counts().sort_index())

# Step 2: Create "Priority" Labels (High/Medium/Low)
# Assumption: Larger tumor radius = higher urgency = higher priority
# We'll use 'mean radius' to define priority tiers
radius = df['mean radius']

# Define priority bins: top 30% = High, middle 40% = Medium, bottom 30% = Low
df['priority'] = pd.qcut(radius, q=[0, 0.3, 0.7, 1.0], labels=['Low', 'Medium', 'High'])

print("\nPriority distribution (created):")
print(df['priority'].value_counts().sort_index())

# Visualize priority vs. radius
plt.figure(figsize=(8, 4))
sns.boxplot(data=df, x='priority', y='mean radius', order=['Low', 'Medium', 'High'])
plt.title("Tumor Radius by Assigned Priority Level")
plt.show()

# Step 3: Preprocess Data
X = df.drop(['target', 'priority'], axis=1)  # All features except labels
y = df['priority']  # Our new 3-class target

# Encode labels (optional, but good practice)
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Split data (stratified to preserve class distribution)
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)

print(f"\nTraining set size: {X_train.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")

# Step 4: Train Random Forest Classifier
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Step 5: Evaluate Model
y_pred = rf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average='weighted')  # Use weighted for multi-class

print(f"\n=== MODEL PERFORMANCE ===")
print(f"Accuracy : {accuracy:.4f}")
print(f"F1-Score : {f1:.4f}")

print("\nDetailed Classification Report:")
target_names = le.classes_  # ['Low', 'Medium', 'High']
print(classification_report(y_test, y_pred, target_names=target_names))

# Step 6: Feature Importance (Optional Insight)
importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
plt.figure(figsize=(10, 6))
sns.barplot(x=importances[:10], y=importances[:10].index)
plt.title("Top 10 Features by Importance")
plt.xlabel("Importance")
plt.show()