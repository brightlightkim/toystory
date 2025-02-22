import torch
import pandas as pd
from datasets import load_dataset, Dataset
from transformers import RobertaTokenizer, RobertaForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split

data = load_dataset("nvidia/Aegis-AI-Content-Safety-Dataset-2.0")

# Extract relevant columns
data = data["train"].to_pandas()
data = data.dropna(subset=['prompt', 'response', 'response_label'])

# Extract relevant columns
responses = data['response'].fillna('')  # Handle null values
labels = data['response_label'].map({'safe': 0, 'unsafe': 1})  # Convert labels to binary

# Split dataset into train and test
train_texts, val_texts, train_labels, val_labels = train_test_split(responses, labels, test_size=0.1, random_state=42)

# Load tokenizer
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')

# Tokenize data
def tokenize_function(texts):
    return tokenizer(texts, padding="max_length", truncation=True, max_length=512)

train_encodings = tokenize_function(train_texts.tolist())
val_encodings = tokenize_function(val_texts.tolist())

# Convert to PyTorch dataset
class ContentSafetyDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels
    
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels.iloc[idx])
        return item

train_dataset = ContentSafetyDataset(train_encodings, train_labels)
val_dataset = ContentSafetyDataset(val_encodings, val_labels)

# Load model
model = RobertaForSequenceClassification.from_pretrained("roberta-base", num_labels=2)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=4,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=100,
)

# Define trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer
)

# Train model
trainer.train()

# Save the fine-tuned model
model.save_pretrained("backend/data/content_safety_roberta")
tokenizer.save_pretrained("backend/data/content_safety_roberta")

print("Fine-tuning complete. Model saved to './content_safety_roberta'")
