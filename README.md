# ProjetoSD_Grupo1

## Running this project:
1. Choose a path to put tutorial.db. Change the path in the "volumes" property in docker-compose.yml to match the path of tutorial.db in the host
2.
```
docker swarm init
docker stack deploy -c docker-compose.yml friendlyname
```
3. In case of errors rebuild each images and try step 2 again
```
docker build -t image .
docker tag <image> username/repository:tag
docker push username/repository:tag
```

Project done with python for Distributed Systems course. Universidade da Madeira 2017/2018
- Rúben França
- Igor Figueira
- Joaquim Abreu
