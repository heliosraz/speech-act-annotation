import os
import re
import json
from nltk.tokenize import sent_tokenize, word_tokenize
from typing import List

special_char = ["\\", ".", "+", "*", "?", "^", "$", "(", ")", "[", "]", "{", "}", "|"]


def process(file_name: str, root: str):
    document = ""
    with open(os.path.join(root, file_name), "r") as f:
        print(re.split("([A-Z]+:|[A-z]+ [A-z]+:)", f.read()))
        # for line in f:
        #     speaker = re.search(r"[A-z]+:", line)
        #     if speaker:
        #         document += line
    with open("../data/processed_" + root.split("/")[-1] + ".json", "a") as f:
        print(json.dumps({"data": document}), file=f)
    print(document)


def write_json(file_path, values):
    with open(file_path, "a", encoding="utf-8") as f:
        print(json.dumps(values) + ",", file=f)


def preannotation():
    document_sentences_dict = {}
    for root, dirs, files in os.walk("../data/storycorps"):
        for name in files:
            document_sentences = []
            print(name)
            if name == ".DS_Store":
                continue
            with open(os.path.join(root, name), "r", encoding="utf-8") as f:
                for line in f:
                    temp = line.split(":")
                    if len(temp) > 1:
                        dialogue = ":".join(temp[1:])
                    else:
                        dialogue = "".join(temp)
                    sentences = sent_tokenize(dialogue)
                    if sentences:
                        for s in sentences:
                            document_sentences.append(s)
            document_sentences_dict[name] = document_sentences
    result = []
    for root, dirs, files in os.walk("../data/storycorps"):
        for name in files:
            print(name)
            spans = []
            if name == ".DS_Store":
                continue
            with open(os.path.join(root, name), "r", encoding="utf-8") as f:
                content = f.read()
                sentences = document_sentences_dict[name]
                for s in set(sentences):
                    s = s.lstrip(": ")
                    for c in special_char:
                        s = s.replace(c, "\\" + c)
                    try:
                        # finding the indices for the span
                        # print(name, [match for match in re.finditer(s, content)])
                        for match in re.finditer(s, content):
                            start = match.start()
                            end = match.end()
                            spans.append(
                                {'value': {'start': start, 'end': end, 'text': s, 'labels': ['Turn']},
                                 'from_name': 'Turn', 'to_name': 'text', 'type': 'labels'})
                    except re.error:
                        continue
            if spans:
                spans.sort(key=lambda x: x["value"]["start"])
                starts = set()
                temp = []
                for x in spans:
                    if not x["value"]["start"] in starts:
                        starts.add(x["value"]["start"])
                        temp.append(x)
                spans = temp
                value = {'data': {'text': content}, 'predictions': [{"model_version": "one", "result": spans}]}
                result.append(value)
        with open("../data/processed_" + root.split("/")[-1] + ".json", "a", encoding="utf-8") as f:
            print(json.dumps(result), file=f)


if __name__ == "__main__":
    preannotation()
