from datetime import datetime
from backend_REST.graph import WIKIDATA

import json
import re


class Validator():
    def valid_email(email):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

        # Check email string
        if re.search(regex, email):
            return True
        else:
            return False

    def valid_date(date):
        # Check date with multiple formats
        for fmt in ('%Y-%m-%d', '%Y/%m/%d'):
            try:
                datetime.strptime(date, fmt)
                return True
            except ValueError:
                pass
        return False

    def valid_degree(degree):
        if degree == 'bachelor' or degree == 'master':
            return True
        else:
            return False

    def same_password(password, password_confirmation):
        return password == password_confirmation

    def inside_json_list(URI, subject):
        file_path = "wikidata/" + subject + "s.json"
        column_name = subject + ".value"

        with open(file_path) as json_file:
            json_text = json.load(json_file)
            URI_list = list(json_text[column_name].values())

            for URI_list_item in URI_list:
                if URI_list_item == URI:
                    return True
        return False

    def valid_skill(skill_id):
        skill_URI = WIKIDATA + skill_id

        return Validator.inside_json_list(skill_URI, "skill")

    def valid_language(language_id):
        language_URI = WIKIDATA + language_id

        return Validator.inside_json_list(language_URI, "language")

    def valid_profession(profession_id):
        profession_URI = WIKIDATA + profession_id

        return Validator.inside_json_list(profession_URI, "profession")

    def valid_discipline(discipline_id):
        discipline_URI = WIKIDATA + discipline_id

        return Validator.inside_json_list(discipline_URI, "discipline")
