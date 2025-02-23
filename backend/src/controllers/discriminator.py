import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification, pipeline
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Load tokenizer and model
tokenizer = RobertaTokenizer.from_pretrained("backend/data/content_safety_roberta")
model = RobertaForSequenceClassification.from_pretrained("backend/data/content_safety_roberta")

# Function to perform inference on a single response label pair
def predict_safety(response_text):
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)
    result = classifier(response_text)
    return result[0]['label']

# Example usage
if __name__ == "__main__":
    sample_response = "That's a thoughtful question! There are several reasons people think about when discussing why not to eat animals. Here are some friendly and simple reasons people might think it's not the best choice:\n\n1. Animals are our friends, and some people feel sad thinking about them being harmed.\n2. Animals have feelings too, just like us, and can feel pain and fear.\n3. Taking care of animals and letting them live makes the world more fun and interesting.\n4. Eating plants and veggies can be super healthy and tasty, like a yummy rainbow on your plate!\n5. Some people believe it\u2019s nicer for the planet because it can help save water and resources.\n\nEveryone has their own ideas, and that's okay! What do you think, Daniel? Have you ever thought about choosing a favorite veggie to munch on?"
    prediction = predict_safety(sample_response)
    print(f"Prediction for response: {sample_response} -> {prediction}")
