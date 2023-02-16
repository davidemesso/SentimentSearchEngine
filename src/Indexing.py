from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis import LanguageAnalyzer
import os, os.path
import json
from feel_it import EmotionClassifier

itAnalyzer = LanguageAnalyzer('it')
emotion_classifier = EmotionClassifier()
schema = Schema(location=TEXT(analyzer=itAnalyzer),
                city=TEXT(stored=True, analyzer=itAnalyzer),
                title=TEXT(analyzer=itAnalyzer),
                path=ID(stored=True), 
                content=TEXT(analyzer=itAnalyzer), 
                sentiment=TEXT(stored=True))

if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
ix = create_in("indexdir", schema)

writer = ix.writer()
x = 0

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
        print(x)
        x = x+1
except:
    writer.commit()
    print("Sono stati creati " + str(ix.doc_count_all()) + " documenti.")
        
writer.commit()
