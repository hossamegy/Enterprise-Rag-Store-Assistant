import pickle
import torch
import torch.nn.functional as F
from sklearn.preprocessing import LabelEncoder
from transformers import AutoModel, AutoTokenizer

from src.config.logger import logger
from src.core.ports.base_classfier_model import BaseClassfierModel
from src.core.models.classfier_model import Classifier


class ClassfierModel(BaseClassfierModel):

    def __init__(self, bert_model_path: str, model_path: str, tokenizer_path: str, classes_path: str, num_classes: int, device: str):
        self.bert_model_path = bert_model_path
        self.model_path = model_path
        self.tokenizer_path = tokenizer_path
        self.classes_path = classes_path
        self.num_classes = num_classes
        self.device = device
        self.load()

    def load(self):
        try:
            logger.info(f'Loading BERT backbone from {self.bert_model_path}')
            try:
                self.bert_model = AutoModel.from_pretrained(self.bert_model_path, use_safetensors=True)
            except Exception:
                self.bert_model = AutoModel.from_pretrained(self.bert_model_path)
            self.model = Classifier(self.bert_model, num_classes=self.num_classes).to(self.device)
            self.tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_path)
            self.label_encoder = LabelEncoder()
            with open(self.classes_path, 'rb') as f:
                classes = pickle.load(f)
                self.label_encoder.classes_ = classes
            logger.info(f'Loading classifier weights from {self.model_path}')
            self.model.load_state_dict(torch.load(self.model_path, map_location=self.device, weights_only=False), strict=False)
            self.model.eval()
            logger.info('Classifier model loaded successfully.')
        except Exception as e:
            logger.critical(f'Failed to load classifier model: {str(e)}')
            raise RuntimeError(f'Classifier initialization failed. Ensure model files exist at {self.model_path}') from e

    def predict(self, text: str) -> tuple[str, float]:
        inputs = self.tokenizer(text, return_tensors='pt', padding='max_length', truncation=True, max_length=128)
        input_ids = inputs['input_ids'].to(self.device)
        attention_mask = inputs['attention_mask'].to(self.device)
        with torch.no_grad():
            logits = self.model(input_ids, attention_mask)
            probs = F.softmax(logits, dim=1)
            max_prob, pred_class_tensor = torch.max(probs, dim=1)
            max_prob = max_prob.item()
            pred_class = pred_class_tensor.item()
            pred_label = self.label_encoder.inverse_transform([pred_class])[0]
        return (pred_label, max_prob)