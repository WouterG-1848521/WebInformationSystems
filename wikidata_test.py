from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")


def get_professions():
    query = """
    SELECT ?profession ?professionLabel
    WHERE {
        ?profession wdt:P31 wd:Q28640 . # instance of profession
        ?profession wikibase:sitelinks ?linkcount .
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
        FILTER (?linkcount >= 60)
    } 
    GROUP BY ?profession ?professionLabel ?linkcount
    ORDER BY DESC(?linkcount)
    LIMIT 50
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    results_df = pd.json_normalize(results['results']['bindings'])
    print(results_df)
    results_json = results_df[['profession.value',
                               'professionLabel.value']].to_json()
    print(results_json)

    # Write pretty print JSON data to file
    with open("wikidata/professions.json", "w") as outfile:
        outfile.write(results_json)


def get_skills():
    query = """
    SELECT ?skill ?skillLabel
    WHERE {
        ?skill wdt:P279 ?class . # subclass(wdt:p279) of skill(wd:Q205961) or self-managment(wd:Q2267710)
        ?skill wikibase:sitelinks ?linkcount .
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
        FILTER (?class IN (wd:Q205961, wd:Q2267710) && ?linkcount >= 1)
    } 
    GROUP BY ?skill ?skillLabel ?linkcount
    ORDER BY DESC(?linkcount)
    LIMIT 50
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    results_df = pd.json_normalize(results['results']['bindings'])
    print(results_df)
    results_json = results_df[['skill.value',
                               'skillLabel.value']].to_json()
    print(results_json)

    # Write pretty print JSON data to file
    with open("wikidata/skills.json", "w") as outfile:
        outfile.write(results_json)


def get_languages():
    query = """
    SELECT ?language ?languageLabel
    WHERE {
        ?language wdt:P31 wd:Q34770 . # instance of language
        ?language wikibase:sitelinks ?linkcount .
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
        FILTER (?linkcount >= 100) .
    } 
    GROUP BY ?language ?languageLabel ?linkcount
    ORDER BY DESC(?linkcount)
    LIMIT 50
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    results_df = pd.json_normalize(results['results']['bindings'])
    results_json = results_df[['language.value',
                               'languageLabel.value']].to_json()

    print(results_json)
    # Write pretty print JSON data to file

    with open("wikidata/languages.json", "w") as outfile:
        outfile.write(results_json)


def get_disciplines():
    query = """
    SELECT ?discipline ?disciplineLabel
    WHERE {
        ?discipline wdt:P31 wd:Q11862829 . # instance of academic discipline
        ?discipline wikibase:sitelinks ?linkcount .
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
        FILTER (?linkcount >= 125) .
    } 
    GROUP BY ?discipline ?disciplineLabel ?linkcount
    ORDER BY DESC(?linkcount)
    LIMIT 50
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    results_df = pd.json_normalize(results['results']['bindings'])
    results_json = results_df[['discipline.value',
                               'disciplineLabel.value']].to_json()

    print(results_json)
    # Write pretty print JSON data to file

    with open("wikidata/disciplines.json", "w") as outfile:
        outfile.write(results_json)


# get_professions()
# get_skills()
# get_languages()
get_disciplines()
