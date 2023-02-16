# Progetto gestione dell'informazione

Progetto di:
- Simone Degli Esposti \<matricola>
- Messori Davide 152540

## Guida all'installazione

### Prerequisiti

- Python

Nota: l'indice è stato creato in python 3.10 e potrebbe risultare deserializzabile solo nella stessa versione o superiore. 

I moduli necessari andranno installati attraverso uno dei seguenti comandi:
``` cmd
pip install <module>

python3 -m pip install <module>
```
Dipendenze e versioni utilizzate:
```python
Package     Version
----------  ------
Scrapy      2.7.1
feel-it     1.0.4
Whoosh      2.7.4
autocorrect 2.6.1
```

## Costruzione dell'index

Il dataset scelto è composto da 73.268 recensioni di ristoranti su tripadvisor divise tra le 5 provincie di Modena, Reggio Emilia, Bologna, Parma e Rimini, ottenuto attraverso scraping del sito.

### Scraping
La prima cosa da fare è indicare l'url da cui si vuole iniziare lo scraping, cambiando la variabile urls in [scraper.py](./scraper.py)
``` python
 def start_requests(self):
        urls = ['https://www.tripadvisor.it/Restaurants-g187804-Parma_Province_of_Parma_Emilia_Romagna.html']
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
```

E poi eseguire lo scraper con il seguente comando:
``` bash
python3 -m scrapy runspider scraper.py
```
Esso si occuperà di raccogliere tutte le recensioni in file json.


Ottenuto il dataset voluto si può passare all'indexing.

### Indexing

Una volta organizzati i documenti in una cartella Docs contenente una sottocartella con il nome della città scelta per ognuna e creata una cartella src con il file [Indexing.py](./src/Indexing.py) si può proseguire all'indexing
```
    .
    ├── Docs
    │   ├── Bologna
    │   ├── Modena
    │   ├── Parma
    │   ├── Reggio
    │   └── Rimini
    └── src

``` 
eseguendo
```
python3 Indexing.py
```

Nota: viene fornito un file alternativo [IndexingWhooshQGrams.py](./src/IndexingWhooshQGrams.py) per la creazione di un indice basato su q-grammi.

## Ricerca

## Benchmark