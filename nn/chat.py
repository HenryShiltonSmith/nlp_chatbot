import random
import json
import torch
import os

from nn.model import NeuralNet
from nn.nltk_utils import word_bag, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

from pathlib import Path

os.chdir(Path(__file__).parent)

with open('intents.json', 'r') as f:
    intents = json.load(f)
    
FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

def chat(sentence):
    while True:     
        sentence = tokenize(sentence)
        X = word_bag(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)    
        
        output = model(X)
        
        _, predicted = torch.max(output, dim=1)
        tag = tags[predicted.item()]
        
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        
        if prob.item() > 0.75:
            for intent in intents["intents"]:
                if tag == intent["tag"]:
                    return intent["tag"], random.choice(intent["responses"])
        else:
            return "I don't quite understand."