from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis import NgramAnalyzer
import os, os.path
import json
from feel_it import EmotionClassifier

ngramAnalizer = NgramAnalyzer(3)
emotion_classifier = EmotionClassifier()
schema = Schema(location=TEXT,
                city=TEXT(stored=True),
                title=TEXT,
                path=ID(stored=True), 
                content=TEXT(analyzer=ngramAnalizer), 
                sentiment=TEXT(stored=True))

if not os.path.exists("indexdirNgramAnalyzer"):
    os.mkdir("indexdirNgramAnalyzer")
ix = create_in("indexdirNgramAnalyzer", schema)

writer = ix.writer()

PATHS = ['Docs/Modena/', 'Docs/Bologna/', 'Docs/Reggio/', 'Docs/Parma/', 'Docs/Rimini/']
try:
    for dir in PATHS:
        files = os.listdir(dir)
        for file in files:
            pathStr = dir + os.sep + file
            with open(pathStr, "r") as json_file:
                document = json.loads(json_file.read())
                sentiment = emotion_classifier.predict([f"{document['title']} {document['body']}"])
                writer.add_document(location=document["location"],
                                    city=dir.replace("Docs/", "")[0:-1],
                                    title=document["title"], 
                                    path=pathStr, 
                                    content=document["body"],
                                    sentiment=sentiment[0])
except:
    writer.commit()
    print("Sono stati creati " + str(ix.doc_count_all()) + " documenti.")
        
writer.commit()
