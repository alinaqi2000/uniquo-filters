debug:
	docker compose build && docker compose up db -d
	docker run --network uniquo-filters_backnet -v $(CURDIR)/backend:/code -p 5001:5000 -e MYSQL_ROOT_PASSWORD=$(cat db/password.txt) uniquo-filters-backend:latest
start:
	docker compose build && docker compose up -d
stop:
	docker-compose down