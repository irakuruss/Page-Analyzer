# Page Analyzer

### Hexlet tests and linter status:
[![Actions Status](https://github.com/irakuruss/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/irakuruss/python-project-83/actions)
[![Python CI](https://github.com/irakuruss/python-project-83/actions/workflows/main.yml/badge.svg)](https://github.com/irakuruss/python-project-83/actions/workflows/main.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/adcd1a65ef458b8e6b9f/maintainability)](https://codeclimate.com/github/irakuruss/python-project-83/maintainability)

https://page-analyzer-lcbc.onrender.com
___
### Description
Page Analyzer is a site that analyzes specified pages for SEO suitability

Build with:

- Python
- Flask
- Jinja2
- Flake8
- Poetry
- Bootstrap
- Beautiful Soup
- Requests
- PostgreSQL
- Psycopg
- Gunicorn
- Python-dotenv
___
### Installation
You must have Python 3.8 and newer, Poetry and PostgreSQL installed to work properly
1. Clone project:
```
git@github.com:irakuruss/python-project-83.git
```
2. Database creation:
```
sudo -u postgres createuser --createdb {username} 
createdb {databasename}
```
3. Secret keys.
The site requires two environment variables: SECRET_KEY - Flask app secret key, DATABASE_URL - database connection url. These can be defined using the .env file:
```
DATABASE_URL='postgresql://{username}:{password}@{host}:{port}/{databasename}'
SECRET_KEY='{your secret key}'
```
4. Installing dependencies and customizing the database:
```
export DATABASE_URL='postgresql://{username}:{password}@{host}:{port}/{databasename}'
make build
```
5. Running a dev server:
```
make dev
```
6. Starting production server:
```
make start
```
