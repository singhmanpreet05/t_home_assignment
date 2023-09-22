# Start with new database and new images
Make sure to delete any stale volume
`docker volume rm teslanow_my-db;`


In case you get an error deleting that its already used by the container then remove the container for e.g

```buildoutcfg
manpreet@Manpreets-MacBook-Pro TeslaNow % docker volume rm teslanow_my-db;                                                  
Error response from daemon: remove teslanow_my-db: volume is in use - [e9fe9d4d34b22c3cf198af056a46abd7e6412269922d9d813b05a30d10f41eed]
manpreet@Manpreets-MacBook-Pro TeslaNow % docker stop e9fe9d4d34b22c3cf198af056a46abd7e6412269922d9d813b05a30d10f41eed
e9fe9d4d34b22c3cf198af056a46abd7e6412269922d9d813b05a30d10f41eed
manpreet@Manpreets-MacBook-Pro TeslaNow % docker rm e9fe9d4d34b22c3cf198af056a46abd7e6412269922d9d813b05a30d10f41eed
e9fe9d4d34b22c3cf198af056a46abd7e6412269922d9d813b05a30d10f41eed
manpreet@Manpreets-MacBook-Pro TeslaNow % docker volume rm teslanow_my-db;                                          
teslanow_my-db
```

Make sure docker is built from latest code

`docker-compose build --no-cache;`

Start the server

`docker-compose up app`

# Start/Restart with existing database and existing images

`docker-compose up app`

# How can the client connect to server ?
Example session 
```buildoutcfg
manpreet@Manpreets-MacBook-Pro TeslaNow % nc localhost 8000 
read Etc/UTC
2022-11-14T03:19:20+00:00
upsert my_custom_timezone,10
1
read my_custom_timezone
2022-11-14T03:21:19+00:00
upsert my_custom_timezone,20
2
read my_custom_timezone
2022-11-14T03:21:36+00:00
delete my_custom_timezone
1
read my_custom_timezone
null
read Asia/Hong_Kong;America/New_York
2022-11-14T11:23:28+08:00;2022-11-13T22:23:28-05:00
upsert Foo,1320;Bar,-600
2
read Foo;Bar
2022-11-14T03:45:59+00:00;2022-11-14T03:13:59+00:00
read UTC
2022-11-14T03:24:06+00:00
```

# How to change datasource
In `docker-compose.yml` `service` `app` `environment` `DATASOURCE` 

set that variable to `MYSQL` to connect to mysql

set that variable to `REDIS` to connect to redis

# Starting redis afresh
This overrides the redis database with standard timezones
`cp src/datasources/redis/dump.rdb src/datasources/redis/redis-dump/dump.rdb`

# Starting mysql afresh
delete the volume
`docker volume rm teslanow_my-db`

# Benchmark
This can be run locally

`python3 src/scripts/benchmark_client.py`


## Results
### REDIS
```
593 records about to be processed for read, write and delete
Read Execution time in seconds: 1.2712628841400146
Write Execution time in seconds: 1.176785945892334
Delete Execution time in seconds: 1.1449120044708252
```

### MYSQL
```
593 records about to be processed for read, write and delete
Read Execution time in seconds: 1.4030909538269043
Write Execution time in seconds: 2.2387189865112305
Delete Execution time in seconds: 2.293421983718872
```

# Running unit tests
Ensure that the containers are running by calling 

`docker-compose build --no-cache;docker-compose up app-test dbserver-test`

Find the app server container 
```buildoutcfg
manpreet@Manpreets-MacBook-Pro TeslaNow % docker ps
CONTAINER ID   IMAGE               COMMAND                  CREATED          STATUS          PORTS                                         NAMES
39751768f6e5   teslanow_app-test   "python3 src/main.py…"   26 seconds ago   Up 26 seconds   8001/tcp, 0.0.0.0:8001->8000/tcp              teslanow_app-test_1
2db766ec6367   mysql:5.7           "docker-entrypoint.s…"   2 minutes ago    Up 26 seconds   3307/tcp, 33060/tcp, 0.0.0.0:3307->3306/tcp   teslanow_dbserver-test_1
```

Now call 

`docker exec -it 39751768f6e5 python3 -m unittest discover src`