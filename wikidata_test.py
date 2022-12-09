from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")


def get_professions():
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

    print(results_df)


def get_skills():
    query = """
    SELECT ?skill ?skillLabel
    WHERE {
        ?skill wdt:P31 wd:Q205961 .
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
    } 
    LIMIT 3
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    results_df = pd.io.json.json_normalize(results['results']['bindings'])
    results_df[['skill.value', 'skill.value']].head()

    print(results_df)


def get_languages():
    query = """
    SELECT ?language ?languageLabel
    WHERE {
        ?language wdt:P31 wd:Q34770 .
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
    } 
    LIMIT 3
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    results_df = pd.io.json.json_normalize(results['results']['bindings'])
    results_df[['language.value', 'language.value']].head()

    print(results_df)


# get_professions()
# get_skills()
get_languages()
