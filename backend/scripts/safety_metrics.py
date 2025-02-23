import torch
import numpy as np
import pandas as pd
from datasets import load_dataset
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split

# Detect MPS device (Apple Silicon)
device =  torch.device("cpu")
print(f"Using device: {device}")

# Load the dataset
data = load_dataset("nvidia/Aegis-AI-Content-Safety-Dataset-2.0")["train"].to_pandas()
data = data.dropna(subset=['prompt', 'response', 'response_label'])

# Prepare test data
responses = data['response'].fillna('')
labels = data['response_label'].map({'safe': 0, 'unsafe': 1})  # Convert labels to binary
_, test_texts, _, test_labels = train_test_split(responses, labels, test_size=0.1, random_state=42)

# Load tokenizer and model
model_path = "backend/data/content_safety_roberta"
tokenizer = RobertaTokenizer.from_pretrained(model_path)
model = RobertaForSequenceClassification.from_pretrained(model_path)
model.to(device)  # Move model to MPS or CPU
model.eval()

# Tokenize test data
def tokenize_function(texts):
    return tokenizer(texts, padding="max_length", truncation=True, max_length=512, return_tensors="pt")

test_encodings = tokenize_function(test_texts.tolist())

# Move input tensors to the correct device
for key in test_encodings:
    test_encodings[key] = test_encodings[key].to(device)

# Perform inference
with torch.no_grad():
    outputs = model(**test_encodings)
    logits = outputs.logits
    predictions = torch.argmax(logits, dim=-1).cpu().numpy()  # Move back to CPU for evaluation

# Compute metrics
accuracy = accuracy_score(test_labels, predictions)
precision, recall, f1, _ = precision_recall_fscore_support(test_labels, predictions, average="binary")

# Display metrics
metrics = {
    "Accuracy": accuracy,
    "Precision": precision,
    "Recall": recall,
    "F1 Score": f1
}

print("Evaluation Metrics on Test Set:")
for key, value in metrics.items():
    print(f"{key}: {value:.4f}")