# Social Network App

## Guide followed
https://dev.to/bredmond1019/getting-started-with-flask-7de

## Virtual Environment
Install: `pip install virtualenv`  
Create: `virtualenv venv`  
Activate (windows): `"./venv/Scripts/activate"`  
  
Install requirements: `pip install -r requirements.txt`

## Flask
Run command: `flask run`  
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
