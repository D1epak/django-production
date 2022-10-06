install:
	 sudo apt-get update & sudo apt-get install docker docker-compose
build:
	sudo docker-compose build
down:
	sudo docker-compose down
rm:
	sudo docker-compose down & sudo docker system prune -a & docker image prune -a
ps:
	sudo docker ps -a
im:
	sudo docker images -a
