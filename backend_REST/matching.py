from flask import request
from pandas import DataFrame    

from backend_REST.models.vacancy import Vacancy

from .queries import query_getVacancy, check_diploma, check_experience, check_valid_vacancy, check_person, query_personByDiploma
from .queries import query_getDiplomasFromVacancy, query_getSkillsFromVacancy, query_personBySkill, query_getLanguagesFromVacancy, query_personByLanguage
from .queries import query_getExperiencesFromPerson, query_getDiplomasFromPerson, query_getSkillsFromPerson, query_getLanguagesFromPerson, query_getExperienceFromVacancy
from .queries import query_personByExperience, query_vacancyByDiploma, query_vacancyBySkill, query_vacancyByLanguage, query_vacancyByExperience
from .queries import check_language, check_skill


def getPersonsWithDiploma(graph, diploma):
    out = {}
    query = query_personByDiploma(diploma)
    result = graph.query(query)
    df = DataFrame(result, columns=result.vars)
    for row in df.values:
        if not (row[0] == None):
            personID = row[0].n3()
            out[personID] = row
    return out

def getPersonWithSill(graph, skill):
    out = {}
    query = query_personBySkill(skill)
    result = graph.query(query)
    df = DataFrame(result, columns=result.vars)
    for row in df.values:
        if not (row[0] == None):
            personID = row[0].n3()
            out[personID] = row
    return out

def getPersonWithLanguage(graph, language):
    out = {}
    query = query_personByLanguage(language)
    result = graph.query(query)
    df = DataFrame(result, columns=result.vars)
    for row in df.values:
        if not (row[0] == None):
            personID = row[0].n3()
            out[personID] = row
    return out

def getPersonWithExperience(graph, experience):
    out = {}
    query = query_personByExperience(experience)
    result = graph.query(query)
    df = DataFrame(result, columns=result.vars)
    for row in df.values:
        if not (row[0] == None):
            personID = row[0].n3()
            out[personID] = row
    return out

def getVacanciesForDiploma(graph, diploma):
    out = []
    query = query_vacancyByDiploma(diploma)
    result = graph.query(query)
    df = DataFrame(result, columns=result.vars)
    for row in df.values:
        if not (row[0] == None):
            out.append(row[0].n3())
    return out

def getVacanciesForSkill(graph, skill):
    out = []
    query = query_vacancyBySkill(skill)
    result = graph.query(query)
    df = DataFrame(result, columns=result.vars)
    for row in df.values:
        if not (row[0] == None):
            out.append(row[0].n3())
    return out

def getVacanciesForLanguage(graph, language):
    out = []
    query = query_vacancyByLanguage(language)
    result = graph.query(query)
    df = DataFrame(result, columns=result.vars)
    for row in df.values:
        if not (row[0] == None):
            out.append(row[0].n3())
    return out

def getVacanciesForExperience(graph, experience):
    out = []
    query = query_vacancyByExperience(experience)
    result = graph.query(query)
    df = DataFrame(result, columns=result.vars)
    for row in df.values:
        if not (row[0] == None):
            out.append(row[0].n3())
    return out

def getVacanciesByIDs(graph, vacancyIDs):
    # for every vacancy get all the information
    vacancies = list(set(vacancyIDs))
    matches = {}
    for vacancy in vacancies:
        query = query_getVacancy(vacancy)
        result = graph.query(query)
        df = DataFrame(result, columns=result.vars)

        for i in range(len(df)):
            row = df.iloc[i]
            if not (vacancy in matches):
                matches[vacancy] = {}
                for j in range(len(row)):
                    key = row.keys()[j].n3()
                    matches[vacancy][key] = row.iloc[j].n3()
            else:
                for j in range(len(row)):
                    key = df.keys()[j].n3()
                    val = row.iloc[j].n3()
                    if not (key in matches[vacancy]):
                        matches[vacancy][key] = val
                    else:
                        # check if its already in the list
                        if (not (val in matches[vacancy][key])):
                            matches[vacancy][key] += ", " + val

    returnString = "{\n"
    for key in matches:
        returnString += key + ": {\n"
        for skey in matches[key]:
            val = matches[key][skey]
            returnString += skey + " : " + val + ",\n"
        returnString += "},\n"
    returnString += "}"

    return returnString

##################################################################
# public functions
# TODO: kijken met updates waar deze allemaal opgeroepen moeten worden
##################################################################

# TODO : testen

# DONE : pass queries aan met equivalent skills
# TODO : experience heeft ook skills, deze ook matchen met de skills? of gewoon op experience matchen
# DONE : groepeer returned values per person/vacancy
# DONE : add column names
# TODO : checken dat het toch niet beter kan via dataframe tojson

# DONE : ik check by vacancies that ze available zijn via "availability = 'true'"
#      Dit lijkt enkel te werken als we specifieren dat het een boolean is? via local:availability "true"^^xsd:boolean 
#  -> ofwel schrijven we "true"^^xsd:boolean ofwel gewoon true (zonder quotes) en dan wordt het automatisch een boolean

# TODO : vervangen door helper functies
def matchOnVacancy_anyParameters(graph, vacancyID):
        # check if the vacancy exists
        if not check_valid_vacancy(graph, vacancyID):
            return "Vacancy not found", 404

        # TODO: equivalent dingen staan nog niet in query

        matches = {} # we use the uri as a key and assume that it's the first value returned
        # find matches on diploma
        query = query_getDiplomasFromVacancy(vacancyID)
        result = graph.query(query)
        diplomas = [row.diploma.n3() for row in result]
        # print("diplomas: ", diplomas)
        for diploma in diplomas:
            query = query_personByDiploma(diploma)
            result = graph.query(query)
            df = DataFrame(result, columns=result.vars)
            for row in df.values:
                if not (row[0] == None):
                    personID = row[0].n3()
                    matches[personID] = row
        # print("after diploma: ", matches)

        # find matches on skills
        query = query_getSkillsFromVacancy(vacancyID)
        result = graph.query(query)
        skills = [row.skill.n3() for row in result]
        # print("skills: ", skills)
        for skill in skills:
            query = query_personBySkill(skill)
            result = graph.query(query)
            df = DataFrame(result, columns=result.vars)
            for row in df.values:
                if not (row[0] == None):
                    personID = row[0].n3()
                    matches[personID] = row
        # print("after skills: ", matches)

        # find matches on experience
        query = query_getExperienceFromVacancy(vacancyID)
        result = graph.query(query)
        experiences = [row.exp.n3() for row in result]
        # print("experiences: ", experiences)
        for experience in experiences:
            query = query_personByExperience(experience)
            result = graph.query(query)
            df = DataFrame(result, columns=result.vars)
            for row in df.values:
                if not (row[0] == None):
                    personID = row[0].n3()
                    matches[personID] = row
        # print("after experiences: ", matches)

        # find matches on languages
        query = query_getLanguagesFromVacancy(vacancyID)
        result = graph.query(query)
        languages = [row.lang.n3() for row in result]
        # print("languages: ", languages)
        for language in languages:
            query = query_personByLanguage(language)
            result = graph.query(query)
            df = DataFrame(result, columns=result.vars)
            for row in df.values:
                if not (row[0] == None):
                    personID = row[0].n3()
                    matches[personID] = row
        # print("after languages: ", matches)


        # print("matches: ", matches)

        returnString = "{"
        for key in matches:
            returnString += key + ": {"
            for val in matches[key]:
                returnString += val.n3() + ", "
            returnString += "}, "
        returnString += "}"

        # df = DataFrame.from_dict(matches, orient='index', columns=matches.keys())

        # return df.to_json(orient='index', indent=2)
        # return json.dumps(matches, indent = 4) 
        return returnString

def matchOnVacancy_allParameters(graph, vacancyID):
    # check if the vacancy exists
    if not check_valid_vacancy(graph, vacancyID):
        return "Vacancy not found", 404

    matches = {} # we use the uri as a key and assume that it's the first value returned
    filled = False

    # find matches on diploma
    query = query_getDiplomasFromVacancy(vacancyID)
    result = graph.query(query)
    diplomas = [row.diploma.n3() for row in result]
    # print("diplomas: ", diplomas)
    temp = matches.copy()
    for diploma in diplomas:
        result = getPersonsWithDiploma(graph, diploma)
        if (len(matches) == 0 and not filled): # first time we just add everything
            temp = result
            filled = True
        else:
            for key in matches:
                if not (key in result):
                    del temp[key]
        matches = temp.copy()
                
    # print("after diploma: ", matches)

    # find matches on skills
    query = query_getSkillsFromVacancy(vacancyID)
    result = graph.query(query)
    skills = [row.skill.n3() for row in result]
    # print("skills: ", skills)
    temp = matches.copy()
    for skill in skills:
        result = getPersonWithSill(graph, skill)
        if (len(matches) == 0 and not filled): # first time we just add everything
            temp = result
            filled = True
        else:
            for key in matches:
                if not (key in result):
                    del temp[key]
        matches = temp.copy()
    # print("after skills: ", matches)

    # find matches on experience
    query = query_getExperienceFromVacancy(vacancyID)
    result = graph.query(query)
    experiences = [row.exp.n3() for row in result]
    # print("experiences: ", experiences)
    temp = matches.copy()
    for experience in experiences:
        result = getPersonWithExperience(graph, experience)
        if (len(matches) == 0 and not filled): # first time we just add everything
            temp = result
            filled = True
        else:
            for key in matches:
                if not (key in result):
                    del temp[key]
        matches = temp.copy()
    # print("after experiences: ", matches)

    # find matches on languages
    query = query_getLanguagesFromVacancy(vacancyID)
    result = graph.query(query)
    languages = [row.lang.n3() for row in result]
    # print("languages: ", languages)
    temp = matches.copy()
    for language in languages:
        result = getPersonWithLanguage(graph, language)
        print("lang",result)
        if (len(matches) == 0 and not filled): # first time we just add everything
            temp = result
            filled = True
        else:
            for key in matches:
                if not (key in result):
                    del temp[key]
        matches = temp.copy()
    # print("after languages: ", matches)


    # print("matches: ", matches)

    returnString = "{"
    for key in matches:
        returnString += key + ": {"
        for val in matches[key]:
            returnString += val.n3() + ", "
        returnString += "}, "
    returnString += "}"

    # df = DataFrame.from_dict(matches, orient='index', columns=matches.keys())

    # return df.to_json(orient='index', indent=2)
    # return json.dumps(matches, indent = 4) 
    return returnString

def matchOnPerson(graph, personID):
        if not (check_person(graph, personID)):
            return "Person not found", 404

        matches = {} # we use the uri as a key and assume that it's the first value returned
        vacancies = []

        # find on diploma
        query = query_getDiplomasFromPerson(personID)
        result = graph.query(query)
        diplomas = [row.diploma.n3() for row in result]
        for diploma in diplomas:
            result = getVacanciesForDiploma(graph, diploma)
            for el in result:
                vacancies.append(el)
        # print("after diploma: ", vacancies)

        # find on experience
        query = query_getExperiencesFromPerson(personID)
        result = graph.query(query)
        experiences = [row.exp.n3() for row in result]
        for experience in experiences:
            result = getVacanciesForExperience(graph, experience)
            for el in result:
                vacancies.append(el)
        # print("after experience: ", vacancies)

        # find on skills
        query = query_getSkillsFromPerson(personID)
        result = graph.query(query)
        skills = [row.skill.n3() for row in result]
        for skill in skills:
            result = getVacanciesForSkill(graph, skill)
            for el in result:
                vacancies.append(el)
        # print("after skills: ", vacancies)

        # find on languages
        query = query_getLanguagesFromPerson(personID)
        result = graph.query(query)
        languages = [row.lang.n3() for row in result]
        for language in languages:
            result = getVacanciesForLanguage(graph, language)
            for el in result:
                vacancies.append(el)
        # print("after languages: ", vacancies)

        # for every vacancy get all the information
        vacancies = list(set(vacancies))
        for vacancy in vacancies:
            query = query_getVacancy(vacancy)
            result = graph.query(query)
            df = DataFrame(result, columns=result.vars)
            for i in range(len(df)):
                row = df.iloc[i]
                if not (vacancy in matches):
                    matches[vacancy] = {}
                    for j in range(len(row)):
                        key = row.keys()[j].n3()
                        matches[vacancy][key] = row.iloc[j].n3()
                else:
                    for j in range(len(row)):
                        key = df.keys()[j].n3()
                        val = row.iloc[j].n3()
                        if not (key in matches[vacancy]):
                            matches[vacancy][key] = val
                        else:
                            # check if its already in the list
                            if (not (val in matches[vacancy][key])):
                                matches[vacancy][key] += ", " + val

        
        # print("matches: ", matches)

        # matches = groupByVacancy(matches)
        # convert to json
        returnString = "{\n"
        for key in matches:
            returnString += key + ": {\n"
            for skey in matches[key]:
                val = matches[key][skey]
                returnString += skey + " : " + val + ",\n"
            returnString += "},\n"
        returnString += "}"

        return returnString

# get all the vacancies that match the given diploma
def matchVacancy_diploma(graph, diplomaID):
    # check the diploma exists
    if not (check_diploma(graph, diplomaID)):
        return "Diploma not found", 404

    # get all the vacancies that require this diploma
    result = getVacanciesForDiploma(graph, diplomaID)

    return getVacanciesByIDs(graph, result)
    
# get all the vacancies that match the given skill
def matchVacancy_skill(graph, skillID):
    # check the skill exists
    if not (check_skill(graph, skillID)):
        return "skill not found", 404

    # get all the vacancies that require this skill
    result = getVacanciesForSkill(graph, skillID)
    
    return getVacanciesByIDs(graph, result)

# get all the vacancies that match the given language
def matchVacancy_language(graph, languageID):
    # check the language exists
    if not (check_language(graph, languageID)):
        return "skill not found", 404

    # get all the vacancies that require this language
    result = getVacanciesForLanguage(graph, languageID)
    
    return getVacanciesByIDs(graph, result)

# get all the vacancies that match the given experience
def matchVacancy_experience(graph, experienceID):
    # check the experience exists
    if not (check_experience(graph, experienceID)):
        return "skill not found", 404

    # get all the vacancies that require this experience
    result = getVacanciesForExperience(graph, experienceID)
    
    return getVacanciesByIDs(graph, result)

def matchPerson_diploma(graph, diplomaID):
    # check the diploma exists
    if not (check_diploma(graph, diplomaID)):
        return "skill not found", 404

    # get all the vacancies that require this diploma
    result = getPersonsWithDiploma(graph, diplomaID)
    
    return getVacanciesByIDs(graph, result)

def matchPerson_skill(graph, skillID):
    # check the skill exists
    if not (check_skill(graph, skillID)):
        return "skill not found", 404

    # get all the vacancies that require this skill
    result = getPersonWithSill(graph, skillID)
    
    return getVacanciesByIDs(graph, result)

def matchPerson_language(graph, languageID):
    # check the language exists
    if not (check_language(graph, languageID)):
        return "skill not found", 404

    # get all the vacancies that require this language
    result = getPersonWithLanguage(graph, languageID)
    
    return getVacanciesByIDs(graph, result)

def matchPerson_experience(graph, experienceID):
    # check the experience exists
    if not (check_experience(graph, experienceID)):
        return "skill not found", 404

    # get all the vacancies that require this experience
    result = getPersonWithExperience(graph, experienceID)
    
    return getVacanciesByIDs(graph, result)