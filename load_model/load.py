from transformers import BertTokenizer, BertForSequenceClassification
import torch
from safetensors.torch import load_file
import pandas as pd
import os

versi_model = 6

model_dir = os.path.abspath('./results/v_' + str(versi_model))
if not os.path.exists(model_dir):
    raise ValueError(f"Directory {model_dir} does not exist. Please check the path.")

# Load the saved tokenizer
tokenizer = BertTokenizer.from_pretrained(model_dir)

# Load the model weights from the safetensors file
model_path = os.path.join(model_dir, 'model.safetensors')
state_dict = load_file(model_path)

# Initialize the model and load the state dict
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=3, state_dict=state_dict)

# Move the model to the appropriate device (CPU or GPU)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

def predict(text):
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    
    # Move the input tensors to the appropriate device
    inputs = {key: value.to(device) for key, value in inputs.items()}
    
    # Get the model's predictions
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Get the predicted class
    predictions = torch.argmax(outputs.logits, dim=-1)
    
    # Map the predicted class to the actual label (assuming you have a mapping)
    label_mapping = {0: 'tidak puas', 1: 'netral', 2: 'puas'}
    predicted_label = label_mapping[predictions.item()]
    
    return predicted_label

# Test the model
while True:
    user_input = input("Tanyakan sesuatu (atau ketik 'exit' untuk keluar): ")
    if user_input.lower() == 'exit':
        print("Terima kasih! Sampai jumpa!")
        break
    answer = predict(user_input)
    print(f"Jawaban: {answer}")