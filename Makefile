install:
	poetry install

lint:
	poetry run flake8 page_analyzer

dev:
	poetry run flask --app page_analyzer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

DATABASE_URL ?= postgres://page_analyzer_gncp_user:pNw56Lmv4950rmg5YVTP77YShLQuCJv1@dpg-cl7uht2uuipc73ellmig-a.oregon-postgres.render.com/page_analyzer_gncp
database:
	psql -a -d $DATABASE_URL -f database.sql
build:
	install database
