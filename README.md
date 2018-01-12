# ProjetoSD_Grupo1

Running this project:
1 - Choose a path to put tutorial.db. Change the path in the "volumes" property in docker-compose.yml to match the path of tutorial.db in the host
2 - docker swarm init
3 - docker stack deploy -c docker-compose.yml friendlyname
