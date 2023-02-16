from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, AndGroup, QueryParser, OrGroup
from whoosh.analysis import LanguageAnalyzer
from whoosh import scoring
from autocorrect import Speller
import os, os.path
import json

ix = open_dir("../indexdirLangAnalyzer")

searcher = ix.searcher(weighting=scoring.BM25F())
parser = MultifieldParser(["city", "content", "modena"], schema=ix.schema, group=AndGroup)
speller = Speller('it')

itAnalyzer = LanguageAnalyzer('it')
queryStr = "sushi fresco modena"
possibleCorrection = speller.autocorrect_sentence(queryStr)

if not queryStr == possibleCorrection:
    print(f"Did you mean {possibleCorrection}") 

query = parser.parse(" ".join([token.text for token in itAnalyzer(queryStr)]))
print(query)
query = parser.parse(queryStr)

results = searcher.search(query, limit=10)
newRank = []
for res in results:
    if res.fields()["sentiment"] == "joy":
        res.score *= 3
    newRank.append(res)

newRank.sort(key = lambda x: x.score, reverse=True)
for res in newRank:
    print(res.score)
    print(res.fields()["path"])
    try:
        with open(res.fields()["path"].replace("Š", "è").replace("…", "à"), "r") as f:
            doc = json.loads(f.read())
            print(res.fields()["city"])
            print(doc["location"])
            print(doc["title"])
            print(doc["body"])
            print(res.fields()["sentiment"] + "\n")
    except:
        print("GRAVE ERRORE")