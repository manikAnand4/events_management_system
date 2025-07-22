# Event Management

## Installation

1. Install 3.8 python using `pyenv`.
2. Set it as the local python interpreter using `pyenv local 3.8`.
3. Create/Switch to pipenv env using `pipenv shell`.
4. Install the python dependencies using `pipenv install --dev`.
5. Create .env from .env.template.
6. Create a database in postgres for service and update the .env file.


## Running Server Locally
1. Apply migrations -> `python manage.py migrate`
2. Run server -> `python manage.py runserver`

## API Curls
1. Create an event
    ```
    curl ->
    curl --location 'http://localhost:8000/events/' \
    --header 'Content-Type: application/json' \
    --data '{
        "name": "Hackfest",
        "max_capacity": 3,
        "start_time": "2025-07-20T10:27:47.304Z",
        "end_time": "2025-07-20T11:27:47.304Z",
        "location": "Audi 1"
    }'

    sample payload ->
    {
        "name": "Hackfest", # string name of the event
        "max_capacity": 3, # integer representing max capacity of the event (optional)
        "start_time": "2025-07-20T10:27:47.304Z", # start time of the event (optional)
        "end_time": "2025-07-20T11:27:47.304Z", # end time of the event (optional)
        "location": "Audi 1" # location of the event (optional)
    }

    sample response ->
    {
        "id": 1, # id of the event created (to be used in event registration / attendees list)
        "name": "Hackfest",
        "start_time": "2025-07-20T15:57:47.304000+05:30",
        "end_time": "2025-07-20T16:57:47.304000+05:30",
        "location": "Audi 1",
        "max_capacity": 3
    }
    ```

2. Get Event List
    ```
    curl ->
    It is a paginated API with page size of 10 by default customisable upto 100 max using query param
    page_size=<your desired size>

    curl --location 'http://localhost:8000/events/'

    
    sample response ->
    {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "name": "Hackfest",
                "start_time": "2025-07-20T15:57:47.304000+05:30",
                "end_time": "2025-07-20T16:57:47.304000+05:30",
                "location": null,
                "max_capacity": 3
            },
            {
                "id": 2,
                "name": "Webinar",
                "start_time": "2025-07-20T15:57:47.304000+05:30",
                "end_time": "2025-07-20T16:57:47.304000+05:30",
                "location": "Audi 1",
                "max_capacity": 4
            }
        ]
    }
    ```

3. Event Registration
    ```
    curl -> (make sure to update 1 with your event id)
    curl --location 'http://localhost:8000/events/1/register/' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "name": "manik",
        "email": "manik@gmail.comm"
    }'

    sample payload ->
    {
        "name": "manik", # name of the user
        "email: "manik@gmail.com" # email of the user
    }

    sample response ->
    {
        "id": 1,
        "name": "manik",
        "email": "manik@gmail.com"
    }
    ```

4. Event Attendee List
    ```
    curl -> (make sure to update 1 with your event id)
    It is a paginated API with page size of 20 by default customisable upto 100 max using query param
    page_size=<your desired size>

    curl --location 'http://localhost:8000/events/1/attendees/'


    sample response ->
    {
        "count": 2,
        "next": "http://localhost:8000/events/1/attendees/?page=2",
        "previous": null,
        "results": [
            {
                "id": 1,
                "name": "manik",
                "email": "manik@gmail.com"
            }
        ]
    }
    ```
