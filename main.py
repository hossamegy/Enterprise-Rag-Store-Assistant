from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn as nn
from layers.IntentClassfierLayer import IntentClassfierLayer
from layers.PreprocessingLayer import PreprocessingLayer
from core.MessageContext import MessageContext
import pickle

# Load label classes
with open("DL_Models/IntentClassfier/label_encoder_classes.pkl", "rb") as f:
    label_classes = pickle.load(f)

num_classes = len(label_classes)

# Load tokenizer and BERT
model_name = "aubmindlab/bert-base-arabertv02"
tokenizer = AutoTokenizer.from_pretrained(model_name)
bert_model = AutoModel.from_pretrained(model_name)

# Define the same Classifier architecture
class Classifier(nn.Module):
    def __init__(self, bert_model, hidden_dim=128, num_classes=num_classes, dropout=0.3):
        super().__init__()
        self.bert = bert_model
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(self.bert.config.hidden_size, hidden_dim)
        self.relu = nn.ReLU()
        self.out = nn.Linear(hidden_dim, num_classes)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        cls_embedding = outputs.last_hidden_state[:, 0, :]
        x = self.dropout(cls_embedding)
        x = self.fc(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.out(x)
        return x

# Instantiate and load weights
model = Classifier(bert_model=bert_model, hidden_dim=128, num_classes=num_classes)
model.load_state_dict(torch.load(r"DL_Models\IntentClassfier\arabic_intent_model.pt", map_location="cpu"))
model.eval()

# Preprocessing and Intent Classifier layers
layer1 = PreprocessingLayer()
layer2 = IntentClassfierLayer()

# Example input
context = MessageContext(raw_input="سيشب سشيبسشيبشسيبسيشبسشيبسشيبسش لبسي لسي ")
processed_context = layer1.handle(context)
layer2.handle(processed_context, model=model, tokenizer=tokenizer, label_class=label_classes)

print("Processed input:", processed_context.processed_input)
print("Predicted intent:", processed_context.question_intent)