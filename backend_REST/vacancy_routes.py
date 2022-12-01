from flask import request

def create_vacancy_routes(app, graph):
    # add a vacancy to an enterprise
    @app.route("/enterprise/vacancy/add", methods=['POST'])
    def add_vacancy():
        data = request.form     # request contains : enterpriseID, mainterID (for security check), jobtitle, address, startdate, enddate
            # waarschijnlijk ook nog een lijst van skills
        print(data)
        # TODO: insert in rdf 
        return "add vacancy"

    # remove a vacancy from an enterprise
    @app.route("/enterprise/vacancy/remove", methods=['POST'])
    def remove_vacancy():
        data = request.form     # request contains : enterpriseID, vacancyID, mainterID (for security check)
        print(data)
        # TODO: remove in rdf 
        return "remove vacancy"

    # match a vacancy from parameters
    @app.route("/vacancy/match", methods=['POST'])
    def match_vacancy():
        data = request.form    # request contains : parameters to search a vacancy for