# Meta data API 

## Installation
0a. Ensure you have docker and docker-compose
0b. Optionally setup a virtual environment
1a. If running in production mode: 
```bash
docker-compose -f prod-docker-compose.yml up
```
1b. If running in development mode:
```bash
docker-compose -f dev-docker-compose.yml up
```
2. Access the api at the specified host and port (if not changed: http://localhost:5000/)

## Documentation
Use postman and import the documentation from the file "P5-Metadata-api.postman_collection.json"

## To make changes 
1) Clone the repository from [here](https://github.com/Knox-AAU/Metadata-api)
2) Make the changes you want to make
3) Push them into a branch
4) Make a pull request
5) Ensure pipelines pass

## To use linter
```bash
pylint ./**/*.py
```

## TODO
- Remove testing functions
- Remove testing functions from documentation