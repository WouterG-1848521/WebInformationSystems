# Social Network App

## Guide followed
https://dev.to/bredmond1019/getting-started-with-flask-7de

## Virtual Environment
Install: `pip install virtualenv`  
Create: `virtualenv venv`  
Activate (windows): `"./venv/Scripts/activate"`  
  
Install requirements: `pip install -r requirements.txt`

## Flask
Set flaskapp: `set FLASK_APP=app.py`  
Run: `flask run`  
Run debug: `flask --debug run`   
GraphQL View: http://localhost:5000/graphql

## PostgreSQL
Download: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads  
  
**Default user**: postgres  
**Password**: admin *(chosen)*  

Create Database: pgAdmin software

### Migration
Init DB: `flask db init`  
Add migration: `flask db migrate -m <message>`  
Upgrade DB *(to next migration)*: `flask db upgrade`  
Downgrade DB *(to previous migration)*: `flask db downgrade`  

## React
Run command: `yarn run start`

## GitHub:
- Flask: https://github.com/pallets/flask
- Flask-SQLAlchemy: https://github.com/pallets-eco/flask-sqlalchemy  
- Graphene-SQLAlchemy: https://github.com/graphql-python/graphene-sqlalchemy  
- Flask-GraphQL: https://github.com/graphql-python/flask-graphql  
- Flask-Migrate: https://github.com/miguelgrinberg/Flask-Migrate

## bijkomende installs:
- pip install owlrl


## Front-end setup
Install tainwindcss: `npm install -D tailwindcss`

Compile and watch for changes in Tailwind CSS files: `npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css --watch`


# API Reference
## Available URI's and supported methods:
- `"/index` GET
- `"/login"` POST, GET
- `"/sign-up"` POST, GET
- `"/users/<int:user_id>/profile/show"` GET
- `"/users/<int:user_id>/profile"` GET, PUT, POST

- `"/enterprises/all"` GET
- `"/enterprises/id/<int:id>"` GET
- `"/enterprises/name/<string:name>"` GET
- `"/enterprises/address/<string:address>"` GET
- `"/enterprises"` POST
- `"/enterprises<int:id>"` PUT
- `"/enterprises"` DELETE
- `"/enterprises/transfer"` PUT
- `"/enterprises/maintainer/add"` POST
- `"/enterprises/maintainer/remove""` PUT
- `"/enterprises/location/<int:location>"` GET
- `"/enterprises/locationLL/<float:lat>/<float:long>/<float:distance>"` GET
- `"/enterprises/locationLL/<float:lat>/<float:long>/<int:distance>"` GET

- `"/users/<int:user_id>/matches"` GET
- `"/users/<int:user_id>/matches/skills"` GET
- `"/users/<int:user_id>/matches/discipline"` GET
- `"/users/<int:user_id>/matches/languages"` GET
- `"/users/<int:user_id>/matches/experience"` GET
- `"/vacancies/<int:vacancy_id>/matches"` GET
- `"/vacancies/<int:vacancy_id>/matchesAll"` GET
- `"/vacancies/<int:vacancy_id>/matches/skills"` GET
- `"/vacancies/<int:vacancy_id>/matches/discipline"` GET
- `"/vacancies/<int:vacancy_id>/matches/languages"` GET

- `"/users"` GET, POST
- `"/users/<int:user_id>"` GET, DELETE
