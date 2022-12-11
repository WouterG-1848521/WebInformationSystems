from flask import request
from pandas import DataFrame    

from .queries import query_getVacancy, query_personByDiscipline, check_valid_vacancy, check_person, query_personByDiploma
from .queries import query_getDiplomasFromVacancy, query_getSkillsFromVacancy, query_personBySkill, query_getLanguagesFromVacancy, query_personByLanguage
from .queries import query_getExperiencesFromPerson, query_getDiplomasFromPerson, query_getSkillsFromPerson, query_getLanguagesFromPerson, query_getExperienceFromVacancy
from .queries import query_personByExperience, query_vacancyByDiploma, query_vacancyBySkill, query_vacancyByLanguage, query_vacancyByExperience
from .queries import query_getDisciplinesFromVacancy, query_vacancyByDiscipline, query_getDisciplinessFromPerson, query_getSkillsFromexperiencesOfVacancy, query_getSkillsFromexperiencesOfPerson


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

def getPersonsWithDiscipline(graph, discipline):
    out = {}
    query = query_personByDiscipline(discipline)
    result = graph.query(query)
    df = DataFrame(result, columns=result.vars)
    for row in df.values:
        if not (row[0] == None):
            personID = row[0].n3()
            out[personID] = row
    return out

def getPersonWithSkill(graph, skill):
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

def getVacanciesForDiscipline(graph, discipline):
    out = []
    query = query_vacancyByDiscipline(discipline)
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
    print(vacancies)
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
                    if (row.iloc[j] != None):
                        matches[vacancy][key] = row.iloc[j].n3()
            else:
                for j in range(len(row)):
                    key = df.keys()[j].n3()
                    if (row.iloc[j] == None):
                        continue
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
##################################################################

# TODO @wouter: testen
# DONE @wouter: matching van vacancies enkel als ze open zijn en bij personen enkel als ze ze willen
# DONE @wouter: experience heeft ook skills, deze ook matchen met de skills? of gewoon op experience matchen
# TODO @wouter: checken dat het toch niet beter kan via dataframe tojson


def matchOnVacancy_anyParameters(graph, vacancyID):
        # check if the vacancy exists
        if not check_valid_vacancy(graph, vacancyID):
            return "Vacancy not found", 404

        matches = {} # we use the uri as a key and assume that it's the first value returned
        # find matches on diploma
        query = query_getDiplomasFromVacancy(vacancyID)
        result = graph.query(query)
        diplomas = [row.diploma.n3() for row in result]
        # print("diplomas: ", diplomas)
        for diploma in diplomas:
            result = getPersonsWithDiploma(graph, diploma)
            print("result: ", result)
            for key in result:
                if not (result[key].all() == None):
                    row = result[key]
                    personID = row[0].n3()
                    matches[personID] = row
        # print("after diploma: ", matches)

        # find matches on skills
        query = query_getSkillsFromVacancy(vacancyID)
        result = graph.query(query)
        skills = [row.skill.n3() for row in result]
        # print("skills: ", skills)
        for skill in skills:
            result = getPersonWithSkill(graph, skill)
            for key in result:
                if not (result[key].all() == None):
                    row = result[key]
                    personID = row[0].n3()
                    matches[personID] = row
        # print("after skills: ", matches)

        # find matches on experience
        query = query_getExperienceFromVacancy(vacancyID)
        result = graph.query(query)
        experiences = [row.exp.n3() for row in result]
        # print("experiences: ", experiences)
        for experience in experiences:
            result = getPersonWithExperience(graph, experience)
            for key in result:
                if not (result[key].all() == None):
                    row = result[key]
                    personID = row[0].n3()
                    matches[personID] = row
        # print("after experiences: ", matches)

        # find matches on languages
        query = query_getLanguagesFromVacancy(vacancyID)
        result = graph.query(query)
        languages = [row.lang.n3() for row in result]
        # print("languages: ", languages)
        for language in languages:
            result = getPersonWithLanguage(graph, language)
            for key in result:
                if not (result[key].all() == None):
                    row = result[key]
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

        return returnString

def matchOnVacancy_allParameters(graph, vacancyID):
    # check if the vacancy exists
    if not check_valid_vacancy(graph, vacancyID):
        return "Vacancy not found", 404

    matches = {} # we use the uri as a key and assume that it's the first value returned
    filled = False

    # find matches on diploma
    query = query_getDisciplinesFromVacancy(vacancyID)
    result = graph.query(query)
    disciplines = [row.discipline.n3() for row in result]
    # print("disciplines: ", disciplines)
    temp = matches.copy()
    for disciplines in disciplines:
        result = getPersonsWithDiscipline(graph, disciplines)
        if (len(matches) == 0 and not filled): # first time we just add everything
            temp = result
            filled = True
        else:
            for key in matches:
                if not (key in result):
                    del temp[key]
        matches = temp.copy()
                
    # print("after disciplines: ", matches)

    # find matches on skills
    query = query_getSkillsFromVacancy(vacancyID)
    result = graph.query(query)
    skills = [row.skill.n3() for row in result]
    # print("skills: ", skills)
    temp = matches.copy()
    for skill in skills:
        result = getPersonWithSkill(graph, skill)
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

# get all the persons that match the diplomas of the vacancy
def matchVacancy_diploma(graph, vacancyID):
    # check the vacancy exists
    if not (check_valid_vacancy(graph, vacancyID)):
        return "vacancy not found", 404


    # get all the diploma of the vacnacy
    query = query_getDiplomasFromVacancy(vacancyID)
    result = graph.query(query)
    diplomas = [row.diploma.n3() for row in result]

    if (len(diplomas) == 0):
        return "vacancy has no diplomas", 404

    # get all the vacancies that require this diploma
    persons = []
    for i in range(len(diplomas)):
        result = getPersonsWithDiploma(graph, diplomas[i])
        for el in result:
            persons.append(el)

    df = DataFrame(persons, columns=['person'])
    df = df.drop_duplicates()

    return df.to_json(orient='index', indent=2)

# get all the persons that match the discipline of the vacancy
def matchVacancy_discipline(graph, vacancyID):
    # check the vacancy exists
    if not (check_valid_vacancy(graph, vacancyID)):
        return "vacancy not found", 404


    # get all the diploma of the vacnacy
    query = query_getDisciplinesFromVacancy(vacancyID)
    result = graph.query(query)
    disciplines = [row.discipline.n3() for row in result]
    disciplines = list(set(disciplines))

    if (len(disciplines) == 0):
        return "vacancy has no disciplines", 404

    # get all the vacancies that require this diploma
    persons = []
    for i in range(len(disciplines)):
        result = getPersonsWithDiscipline(graph, disciplines[i])
        for el in result:
            persons.append(el)

    df = DataFrame(persons, columns=['person'])
    df = df.drop_duplicates()

    return df.to_json(orient='index', indent=2)

# get all the persons that match the skills of the vacancy
def matchVacancy_skill(graph, vacancyID):
    # check the vacancy exists
    if not (check_valid_vacancy(graph, vacancyID)):
        return "vacancy not found", 404


    # get all the diploma of the vacnacy
    query = query_getSkillsFromVacancy(vacancyID)
    result = graph.query(query)
    skills = [row.skill.n3() for row in result]

    if (len(skills) == 0):
        return "vacancy has no skills", 404

    # get all the vacancies that require this diploma
    persons = []
    for i in range(len(skills)):
        result = getPersonWithSkill(graph, skills[i])
        for el in result:
            persons.append(el)

    df = DataFrame(persons, columns=['person'])
    df = df.drop_duplicates()

    return df.to_json(orient='index', indent=2)

# get all the persons that match the languages of the vacancy
def matchVacancy_language(graph, vacancyID):
    # check the vacancy exists
    if not (check_valid_vacancy(graph, vacancyID)):
        return "vacancy not found", 404


    # get all the langauges of the vacnacy
    query = query_getLanguagesFromVacancy(vacancyID)
    result = graph.query(query)
    languages = [row.lang.n3() for row in result]

    if (len(languages) == 0):
        return "vacancy has no languages", 404

    # get all the vacancies that require this diploma
    persons = []
    for i in range(len(languages)):
        result = getPersonWithLanguage(graph, languages[i])
        for el in result:
            persons.append(el)

    df = DataFrame(persons, columns=['person'])
    df = df.drop_duplicates()

    return df.to_json(orient='index', indent=2)

# get all the persons that match the experience of the vacancy
# deprecated
def matchVacancy_experience(graph, vacancyID):
    # check the vacancy exists
    if not (check_valid_vacancy(graph, vacancyID)):
        return "vacancy not found", 404


    # get all the experience of the vacnacy
    # query = query_getExperienceFromVacancy(vacancyID)
    query = query_getSkillsFromexperiencesOfVacancy(vacancyID)
    result = graph.query(query)
    skills = [row.skill.n3() for row in result]

    if (len(skills) == 0):
        return "vacancy has no experiences skills", 404

    skills = list(set(skills))

    # get all the vacancies that require this diploma
    persons = []
    for i in range(len(skills)):
        result = getPersonWithSkill(graph, skills[i])
        for el in result:
            persons.append(el)

    df = DataFrame(persons, columns=['person'])
    df = df.drop_duplicates()

    return df.to_json(orient='index', indent=2)

# get all the vacanies that match the diplomas of the person
def matchPerson_discipline(graph, personID):
    # check the person exists
    if not (check_person(graph, personID)):
        return "person not found", 404

    # get all the diploma of the person
    query = query_getDisciplinessFromPerson(personID)
    result = graph.query(query)
    disciplines = [row.discipline.n3() for row in result]
    disciplines = list(set(disciplines))
    # print(disciplines)

    if (len(disciplines) == 0):
        return "person has no disciplines", 404

    # get all the vacancies that require this discipline
    vacancies = []
    for i in range(len(disciplines)):
        result = getVacanciesForDiscipline(graph, disciplines[i])
        for el in result:
            vacancies.append(el)

    return getVacanciesByIDs(graph, vacancies)

# get all the vacanies that match the skills of the person
def matchPerson_skill(graph, personID):
    # check the skill exists
    if not (check_person(graph, personID)):
        return "person not found", 404

    # get all the skills of the person
    query = query_getSkillsFromPerson(personID)
    result = graph.query(query)
    skills = [row.skill.n3() for row in result]

    if (len(skills) == 0):
        return "person has no skills", 404

    # get all the vacancies that require these skills
    vacancies = []
    for i in range(len(skills)):
        result = getVacanciesForSkill(graph, skills[i])
        for el in result:
            vacancies.append(el)

    return getVacanciesByIDs(graph, vacancies)

# get all the vacanies that match the langauages of the person
def matchPerson_language(graph, personID):
    # check the language exists
    if not (check_person(graph, personID)):
        return "person not found", 404

     # get all the lang of the person
    query = query_getLanguagesFromPerson(personID)
    result = graph.query(query)
    langs = [row.lang.n3() for row in result]

    if (len(langs) == 0):
        return "person has no languages", 404

    # get all the vacancies that require this language
    vacancies = []
    for i in range(len(langs)):
        result = getVacanciesForLanguage(graph, langs[i])
        for el in result:
            vacancies.append(el)
    
    return getVacanciesByIDs(graph, result)

# get all the vacanies that match the skills in the  experience of the person
def matchPerson_experience(graph, personID):
    # check the experience exists
    if not (check_person(graph, personID)):
        return "person not found", 404

    # get all the diploma of the person
    # query = query_getExperiencesFromPerson(personID)
    query = query_getSkillsFromexperiencesOfPerson(personID)
    result = graph.query(query)
    skills = [row.skill.n3() for row in result]
    print(skills)

    if (len(skills) == 0):
        return "person has no skills in their experiences", 404

    # get all the vacancies that require this diploma
    vacancies = []
    for i in range(len(skills)):
        result = getVacanciesForSkill(graph, skills[i])
        for el in result:
            vacancies.append(el)

    return getVacanciesByIDs(graph, vacancies)