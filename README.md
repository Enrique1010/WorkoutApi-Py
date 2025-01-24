# Python and FastAPI workout tracker backend service with automated deployment

## Requirements
* Docker
* Docker-compose
* Python >=3.13
* Poetry (python-poetry)

# Features

- User authentication (with registration)
- Create workout routines with associated exercises
- Track routes on certain exercises (like cardio)
- Client side flexibility to send and receive updates

## Setup

### First: Add ENV variables

Create a file '.env' (in the root folder) with this properties:

```bash
HOST='localhost'
DATABASE="YOUR_DATABAsE_NAME"
DB_USER="YOUR_USER_NAME"
DB_PASSWORD="YOUR_USER_PASSWORD"
SECRET_KEY="random string"
```

### Second: Start the containers

Start by running:

```bash
docker-compose up -d
```
The Database and the app will be started. The app is accessible on port 8000

### Endpoints

You can see the regular endpoints on "localhost:8000/docs#/" from default fastAPI swagger.

### Tracking with websockets

To access to this service you need to create a websocket gateway like this: ws://{YOUR_HOST}:8000/api/v1/exercise/ws/tracking/{tracking_data_id}
- First you need to 'connect' for the service to start
- Then send this json to receive and update tracking information
```JSON
{
    "update_tracking_data": false,
    "map_point": {
        "lat": -69.77323424,
        "lon": 70.32342435
    },
    "updated_tracking_data": {} // you can see the creation model on swagger docs
}
```
- If any error ocurred the websocket connection is lost or you will see a json like this:
```JSON
{"status": False, "message": "The tracking has stopped."}
```

## Authentication

To access endpoints that require authentication, you need to include a valid JWT token in the `Authorization` header. This will generate a new token.

### Running Linter Checks

To run linter checks, follow these steps (inside workout-api folder)::

1. **Install dependencies**
   
  If not done in the previous step install dependencies locally:
  ```bash
  poetry install
  ```

2. **Run `pylint`**
  
  ```bash
  poetry run pylint *.py **/*.py
  ```

### Testing

pytest is used for running tests. To run the tests, follow these steps (in workout-api directory):

1. **Install dependencies
```bash
poetry install --with dev
```

2. Run the tests (you can run all the tests)
```bash
poetry run pytest -v
```

Linter check (run this inside workout-api directory)
```bash
poetry run pylint *.py **/*.py
```

That's all folks!!
