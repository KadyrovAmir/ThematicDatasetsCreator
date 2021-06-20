from datetime import datetime
import random
from pathlib import Path

import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding

MODEL_PATH = Path(__file__).resolve().parent.parent / "model"


def train_model(data):
    nlp = spacy.load(MODEL_PATH)
    ner = nlp.get_pipe('ner')

    # Adding labels to the `ner`
    for class_ in data["classes"]:
        if class_ not in ner.labels:
            ner.add_label(class_)

    # Training model
    examples = []
    x = 1
    for text, entities in data["annotations"]:
        examples.append(Example.from_dict(nlp.make_doc(text), entities))
        nlp.initialize(lambda: examples)
        for i in range(10):
            random.shuffle(examples)
            for batch in minibatch(examples, size=compounding(1.0, 32.0, 1.001)):
                nlp.update(batch)
            print(f"Iteration {i} of 10 completed! Number of text: {x} of {len(data['annotations'])} | Time: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        x += 1

    nlp.to_disk(MODEL_PATH)
    print("Training completed!")
