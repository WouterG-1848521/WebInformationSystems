date_formats = "Y/M/D or Y-M-D"


class Response():
    def unauthorized_access_not_logged_in():
        return f"Unauthorized Access (Need to login first)"

    def unauthorized_access_wrong_user():
        return f"Unauthorized Access (Wrong user)"

    def start_date_not_valid():
        return f"Start date not valid. (Formats: {date_formats})"

    def end_date_not_valid():
        return f"End date not valid. (Formats: {date_formats})"

    def email_not_valid():
        return f"Email not valid."

    def email_not_available():
        return f"Email already in use."

    def degree_not_valid():
        return f"Degree not valid."
    
    def user_not_exist():
        return f"This user does not exists."
