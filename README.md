<h1>Here is an API for To do project.</h1></p></p>


## API

[📚 Documentation 📚](https://documenter.getpostman.com/view/22115905/UzdzTk6e)


## Dependencies [pipenv]

The __Pipifile__ and __Pipfile.lock__ files contains info about project dependencies.
To install all dependencies form a __Pipifile__ the __pipenv__ package required.

Install the __pipenv__ package:
```
pip install pipenv
```

Once __pipenv__ is installed, 
the following command will create virtual enviroment and install all project dependencies:
```
pipenv install
```


## Dependencies [pip]

To install all dependencies form a __requirements.txt__ file enter the following command:
```
pip install -r requirements.txt
```


## Enviroment Variables

__.flaskenv__ file contains enviroment variables for flask, such as:
* `FLASK_ENV=development` to run server in development mode 
* `FLASK_APP=manage` to run server from a specific file

So by exporting the last one it becomes possible to run server simply with a command:
```
flask run
```
Instead of specifying the file name in a command.


There are also __.env__ file in use, whitch wasn't pushed to the repo.
This file contains the next varibles:
* `SECRET_KEY=` - contains secret key for flask


## Code

The `~src` folder contains source code for the Flask REST API.

