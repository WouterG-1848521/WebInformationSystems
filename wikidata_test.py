from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

query = """
SELECT ?profession ?professionLabel
WHERE {
    ?profession wdt:P31 wd:Q28640 .
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
} 
LIMIT 3
"""

sparql.setQuery(query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

results_df = pd.io.json.json_normalize(results['results']['bindings'])
results_df[['profession.value', 'profession.value']].head()

print(results_df.to_json())
