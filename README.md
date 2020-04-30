# ds-unit-3-sprint-3-twitoff

## Setup
TODO: virtual env set up

DB setup:
```sh
export FLASK_APP=web_app
flask db init
flask db migrate
flask db upgrade
```

TODO: heroku deployment commands

## Usage
```sh
export FLASK_APP=web_app
flask run
```

## Heroku CLI useful commands
```sh
heroku run bash
heroku restart
heroku logs --tail
heroku open
```