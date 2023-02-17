from argparse import ArgumentParser
from whoosh.query import And, AndNot, Not, AndMaybe, Term
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, AndGroup, OrGroup, QueryParser
from whoosh.analysis import LanguageAnalyzer
from whoosh import scoring
from autocorrect import Speller
import os, os.path
import json

## Init argparser
argParser = ArgumentParser()
argParser.add_argument('query', nargs='*', type=str, help="The search terms")
argParser.add_argument(
    '-f', 
    '--fields', 
    nargs='*', 
    choices=["location", "city", "title", "content"],
    default=["title", "content"],
    help="Fields to search the terms into"
)
group = argParser.add_mutually_exclusive_group()
group.add_argument('-l', choices=["joy", "fear", "sadness", "anger"], help="Sentiment with low negative impact")
group.add_argument('-m', choices=["joy", "fear", "sadness", "anger"], help="Sentiment with low positive impact")
group.add_argument('-L', choices=["joy", "fear", "sadness", "anger"], help="Sentiment with high negative impact")
group.add_argument('-M', choices=["joy", "fear", "sadness", "anger"], help="Sentiment with high positive impact")
argParser.add_argument(
    '-a',
    '--andquery',
    default=False,
    action='store_true',
    help="Search terms with AND logic, default is OR"
)
argParser.add_argument(
    '-c'
    '--autocorrect',
    default=False,
    action='store_true',
    help="Enable autocorrect with most confident correction"
)
argParser.add_argument(
    '--limit',
    type=int,
    default=10,
    help="Limit the number of results, default 10"
)
argParser.add_argument(
    '-t',
    default=False,
    action='store_true', 
    help="Switch to TF-IDF scoring"
)

args = argParser.parse_args()
print(args)

## Init search
ix = open_dir("../indexdir")
print(ix.doc_count_all())

scorer = scoring.TF_IDF() if args.t else scoring.BM25F()
searcher = ix.searcher(weighting=scorer)
searchType = AndGroup if args.andquery else OrGroup
parser = MultifieldParser(args.fields, schema=ix.schema, group=searchType)
speller = Speller('it')
itAnalyzer = LanguageAnalyzer('it')

## Query construction
queryStr = args.query if type(args.query) is str else " ".join(args.query)
possibleCorrection = speller.autocorrect_sentence(queryStr)

if not queryStr == possibleCorrection:
    print(f"Did you mean {possibleCorrection}?")
    if args.c__autocorrect:
        print("Query autocorrected")
        queryStr = possibleCorrection

if("*" in queryStr):
    query = parser.parse(queryStr)
else:
    query = parser.parse(" ".join([token.text for token in itAnalyzer(queryStr)]))

## Sentiment fitlering
if args.M:
    query = And([Term("sentiment", args.M), query])

if args.L:
    query = AndNot(query, Term("sentiment", args.L))

if args.m:
    query = AndMaybe(query, Term("sentiment", args.m))
    query = AndMaybe(query, Term("sentiment", args.m))

if args.l:
    query = AndMaybe(query, Not(Term("sentiment", args.l)))
    query = AndMaybe(query, Not(Term("sentiment", args.l)))
    
    
## Retrieving
print(f"Searching for query {query} ...")
results = searcher.search(query, limit=args.limit)

for res in results:
    print(res.score)
    print(res.fields()["path"])
    try:
        # Replaces comes from an issue indexing on MacOs and searching on Windows
        with open(res.fields()["path"]
                    .replace("Š", "è")
                    .replace("…", "à")
                    .replace("—", "ù"), "r") as f:
            doc = json.loads(f.read())
            print(res.fields()["city"])
            print(doc["location"])
            print(doc["title"])
            print(doc["body"])
            print(res.fields()["sentiment"] + "\n")
    except:
        print("Error reading document")
print(len(results))