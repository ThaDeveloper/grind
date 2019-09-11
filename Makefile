MANAGE:=docker-compose run app python src/manage.py
DOCKER_UP:=docker-compose up

# APP_NAME:= ${1};
# @if [[ ${APP_NAME} == app ]]; then\
#     ARGS:=grind_app_1;\
# @elif [[ ${APP_NAME} == db ]]; then\
# 	ARGS:=grind_db_1 psql -U postgres;\
# fi

build:
	@${DOCKER_UP} --build
migrations:
	@${MANAGE} makemigrations
migrate:
	@${MANAGE} migrate
run:
	@echo "Starting Grind ..."
	@${DOCKER_UP}
db:
	@docker exec -it grind_db_1 psql -U grind
app:
	@docker exec -it grind_app_1 bash
