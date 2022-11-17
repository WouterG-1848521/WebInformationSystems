

def create_routes(app):
    
    @app.route("/")
    def get_users():
        return "Hello World!"