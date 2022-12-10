from datetime import datetime
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
