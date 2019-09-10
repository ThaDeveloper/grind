MANAGE:=docker-compose run app python src/manage.py
DOCKER_UP:=docker-compose up

build:
	@${DOCKER_UP} --build
migrations:
	@${MANAGE} makemigrations
migrate:
	@${MANAGE} migrate
run:
	@${DOCKER_UP}
postgres:
	@docker exec -it grind_db_1 psql -U postgres
