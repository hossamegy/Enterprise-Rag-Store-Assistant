import json

with open(r"G:\enterprise-rag-store-assistant\jupyter_notebook\classfiy_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

texts = [item["question"] for item in data]
labels = [item["intent"] for item in data]

print(f"Number of samples: {len(texts)}")
print(f"Number of classes: {len(set(labels))}")
print(f"Classes: {set(labels)}")