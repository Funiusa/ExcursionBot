# Makefile
DC = docker-compose
DC_RUN = docker-compose run --rm

api_add: # установить зависимости
	$(DC_RUN) -w /app/poetry api poetry add black $(ARGS)

bot_add: # установить зависимости
	$(DC_RUN) -w /app/poetry bot poetry add black $(ARGS)
up:
	$(DC) up

run_api:
	$(DC_RUN) api $(ARGS)

run_bot:
	$(DC_RUN) bot $(ARGS)

upd:
	$(DC_RUN) -d up $(ARGS)

build:
	$(DC) build

clean:
	$(DC) down;

re_api: clean build run_api

re_bot: clean build run_bot

fclean: clean
	docker system prune -a
