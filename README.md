# Meta data API 

## Installation
0. Ensure you have docker and docker-compose
1. Optionally setup a virtual environment
2. If running in production mode: 
```bash
docker-compose -f prod-docker-compose.yml up
```
3. If running in development mode:
```bash
docker-compose -f dev-docker-compose.yml up
```
4. Access the api at the specified host and port (if not changed: http://localhost:5000/)

## Documentation
Use Postman and import the documentation from the file "P5-Metadata-api.postman_collection.json"

## To make changes 
1) Clone the repository from [here](https://github.com/Knox-AAU/Metadata-api)
2) Make the changes you want to make
3) Update the api documentation
4) Push them into a branch
5) Make a pull request
6) Ensure pipelines pass

## To use linter
```bash
pylint ./**/*.py
```

## TODO
See: https://github.com/orgs/Knox-AAU/projects/26/