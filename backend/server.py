import json
import os
import sqlite3
from pathlib import Path
from threading import Thread

import nltk
import requests
import spacy

from flask import Flask, request
from flask_cors import cross_origin

from nltk.tokenize.treebank import TreebankWordTokenizer, TreebankWordDetokenizer

from scrapy import start_scrapy
from model import train_model, MODEL_PATH

app = Flask(__name__)
KEY = os.environ.get("MEGAINDEX_KEY")
URL = f"http://api.megaindex.com/visrep/lda_site"


@app.route("/tokenize", methods=["POST"])
@cross_origin()
def tokenize():
    text = request.json["text"]
    try:
        spans = list(TreebankWordTokenizer().span_tokenize(text))
    except LookupError:
        nltk.download('punkt')
        spans = list(TreebankWordTokenizer().span_tokenize(text))
    return {"tokens": [(s[0], s[1], text[s[0]:s[1]]) for s in spans]}


@app.route("/detokenize", methods=["POST"])
@cross_origin()
def detokenize():
    tokens = request.json["tokens"]
    return {"text": TreebankWordDetokenizer().detokenize(tokens)}


@app.route("/parse", methods=["POST"])
@cross_origin()
def run_scrapy():
    domain = request.json["domain"]
    json_response = requests.get(URL, params={
        "key": KEY,
        "domain": domain
    }).json()

    theme_id = int(sorted(json_response["data"][0]["topics"], key=lambda x: len(x["n"]))[0]["i"])
    cursor = sqlite3.connect(Path(__file__).resolve().parent / "classes.db").cursor()
    query = "SELECT class FROM theme_entity WHERE theme_id = ?"
    classes = []
    for row in cursor.execute(query, (theme_id,)):
        classes.append(row[0])
    thread = Thread(target=start_scrapy, args=(domain, json.dumps(classes)))
    thread.daemon = True
    thread.start()
    return {"started": True}


@app.route("/themes", methods=["GET"])
@cross_origin()
def get_themes():
    cursor = sqlite3.connect(Path(__file__).resolve().parent / "classes.db").cursor()
    data = []
    for row in cursor.execute("SELECT * FROM theme"):
        id, name = row
        data.append({"id": id, "name": name})
    return {"data": data}


@app.route("/classes/<theme_id>", methods=["POST"])
@cross_origin()
def get_ner_data(theme_id):
    nlp = spacy.load(MODEL_PATH)
    cursor = sqlite3.connect(Path(__file__).resolve().parent / "classes.db").cursor()
    query = "SELECT class FROM theme_entity WHERE theme_id = ?"
    classes = []
    for row in cursor.execute(query, (theme_id,)):
        classes.append(row[0])

    text = request.json["text"]
    doc = nlp(text)

    return {
        "classes": classes,
        "annotations": [
            text,
            {
                "entities": [
                    (
                        ent.start_char,
                        ent.end_char,
                        ent.label_
                    ) for ent in doc.ents if ent.label_ in classes
                ]
            }
        ]
    }


@app.route("/classes/<theme_id>/update-classes", methods=["POST"])
@cross_origin()
def save_new_entity_classes(theme_id):
    conn = sqlite3.connect(Path(__file__).resolve().parent / "classes.db")
    cursor = conn.cursor()
    query = "DELETE FROM theme_entity WHERE theme_id = ?"
    cursor.execute(query, (theme_id,))
    conn.commit()
    query = "INSERT INTO theme_entity ('theme_id', 'class') VALUES (?, ?)"
    values_to_insert = [(theme_id, class_) for class_ in request.json["classes"]]
    cursor.executemany(query, values_to_insert)
    conn.commit()
    return {"success": True}


@app.route("/train", methods=["POST"])
@cross_origin()
def retrain_ner_model():
    data = request.json["data"]
    thread = Thread(target=train_model, args=(data,))
    thread.daemon = True
    thread.start()
    return {"started": True}


if __name__ == "__main__":
    app.run(port=5555, debug=True)
