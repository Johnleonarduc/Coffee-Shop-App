# The Coffee Shop Full Stack App

## Introduction
This is the final project of the Identity and Access Management Module in Udacity's Full Stack Web Development Course.
I forked the starter folder which already includes a working ionic frontend that is fully reliant on the backend APIs and authentication and access level strategies i was meant to implement. It also included some basic setup code and project instructions.

The Coffee Shop App is a new digitally enabled cafe that Udacity decide to develop for students to order drinks, socialize, and study hard. But they need help setting up their menu experience.

That's where I came in and helped to finish the Coffee Shop app to help them setup their new experiences. 

The application does the following:

1. Display graphics representing the ratios of ingredients in each drink.
2. Allow public users to view drink names and graphics.
3. Allow the shop baristas to see the recipe information.
4. Allow the shop managers to create new drinks and edit existing drinks.

## About the Stack

This application is built with Python, Flask, SqlAlchemy, and an sqllite local database for Backend and the ionic framework for Frontend.

This app can be run locally for now. To run the app locally, you must first setup the backend requirements and start the server, then install the frontend requirements and start its server likewise.

## Backend Setup Steps - Coffee Shop App

### Installing Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for the app in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - Instructions for setting up a virtual environment for the app can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```
#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `__init__.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension used to handle cross-origin requests from our frontend server.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Seting up the Database
The database is already setup.

### Setup Auth0
This app uses third party authentication Auth0. Visit [auth0.com](auth0.com) on how to go about the following steps:

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:drinks`
   - `get:drinks-detail`
   - `post:drinks`
   - `patch:drinks`
   - `delete:drinks`
6. Create new roles for:
   - Barista
     - can `get:drinks-detail`
     - can `get:drinks`
   - Manager
     - can perform all actions

### Testing with Postman
   - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection_updated.json` into postman. Get Postman [https://www.postman.com/](https://www.postman.com/).
   - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including your JWT in the token field 
   - Run the collection


### Run your Server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```
or

```bash
set FLASK_APP=api.py;
```
Then,

```bash
set FLASK_ENV=development;
```

Finally,
To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


## Setting Up The Frontend

### Intall Dependences:
1. **Installing Node and NPM**
   This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/). It is advisable to make use of Node Version Manager(NVM) to manage your node versions, as this project uses node version 14.17.5. you can install NVM via [https://github.com/nvm-sh/nvm](https://github.com/nvm-sh/nvm). Ensure you switch to node version 14.17.5 before moving to the next step.

2. **Installing Ionic Cli**
   The Ionic Command Line Interface is required to serve and build the frontend. Instructions for installing the CLI is in the [Ionic Framework Docs](https://ionicframework.com/docs/installation/cli).

3. **Installing project dependencies**
   This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

    ```bash
    npm install
    ```

    > _tip_: **npm i** is shorthand for **npm install**

3. **Configure Environment Variables**
   Ionic uses a configuration file to manage environment variables. These variables ship with the transpiled software and should not include secrets.

   - Open `./src/environments/environments.ts` and ensure each variable reflects the system you stood up for the backend.
  
4. **Run Your Frontend in Dev Mode**
    Ionic ships with a useful development server which detects changes and transpiles as you work. The application is then accessible through the browser on a localhost port. To run the development server, cd into the `frontend` directory and run:

    ```bash
    ionic serve
    ```

    > _tip_: Do not use **ionic serve** in production. Instead, build Ionic into a build artifact for your desired platforms.
    > [Checkout the Ionic docs to learn more](https://ionicframework.com/docs/cli/commands/build)


# API Endpoints and Documentation

## All GET Endpoint

`GET '/drinks'`

- Fetches a list of drinks with few details.
- It is a public route.
- Request Parameters: None
- Response Body: status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks or appropriate status code indicating reason for failure

```json
{
  "success": "True",
  "drinks":{
    "id": 1,
    "title": "matcha shake",  
    "recipe": [
          {
            "name": "milk",
            "color": "grey",
            "parts": 1
          }]
}
```

---

`GET '/drinks-detail'`

- Fetches list of drinks with more details drinks with few details.
- It requires the 'get:drinks-detail' permission
- Request Parameters: None
- Response Body: status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks or appropriate status code indicating reason for failure

```json
{
  "success": "True",
  "drinks":{
    "id": 1,
    "title": "matcha shake",  
    "recipe": [
          {
            "name": "milk",
            "color": "grey",
            "parts": 1
          }]
}
```

---
## POST Endpoint

`POST '/drinks'`

- it creates a new row in the drinks table
- it requires the 'post:drinks' permission
- Request Body:

```json
{
    "id": -1,
    "title": "matcha shake",  
    "recipe": [
          {
            "name": "milk",
            "color": "grey",
            "parts": 1
          }]
}
```

- Response body: it returns a single new drink object

```json
{
  "success": "True",
  "drinks":{
    "id": 1,
    "title": "matcha shake",  
    "recipe": [
          {
            "name": "milk",
            "color": "grey",
            "parts": 1
          }]
}
```


---
## PATCH Endpoint

`PATCH '/drinks/<id>'`

- it updates a drinks row
- it requires the 'patch:drinks' permission
- Request Parameter: `id` - integer
- Request Body:

```json
{
    "id": 1,
    "title": "matcha shake",  
    "recipe": [
          {
            "name": "milk",
            "color": "grey",
            "parts": 1
          }]
}
```

- Response body: it returns the patched drink object

```json
{
  "success": "True",
  "drinks":{
    "id": 1,
    "title": "matcha shake",  
    "recipe": [
          {
            "name": "milk",
            "color": "grey",
            "parts": 1
          }]
}


```
## Delete Endpoint

`DELETE '/drinks/<id>'`

- Deletes a specified drink using the id of the drink
- it requires the 'delete:drinks' permission
- Request Parameter: `id` - integer
- Response body:  

```json
{
  "success": True, 
  "delete": id
}
```

Thank you for viewing my project. Enjoy!
---
