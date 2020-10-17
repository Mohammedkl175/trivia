# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

For windows : 
```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## Endpoints

### GET /categories

- Returns a dictionary of categories and success value.

#### Sample

`curl -X GET http://127.0.0.1:5000/categories`

```
"categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

### GET /categories/category_id/questions

- Returns a current category, list of questions in the given category, success value, and total number of questions
- Results are paginated in group of 10. Include a request argument to choose page number, starting from 1.
- Error of status code 404 will be thrown when there is no question on the given page.

#### Sample

`curl -X GET http://127.0.0.1:5000/categories/1/questions?page=2`

```
"current_category": {
    "id": 1,
    "type": "Science"
  },
  "questions": [
    {
      "answer": "The Liver",
      "category": "1",
      "difficulty": 4,
      "id": 16,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": "1",
      "difficulty": 3,
      "id": 17,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": "1",
      "difficulty": 4,
      "id": 18,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

### GET /questions

- Returns a dictionary of categories, a list of questions,current category = `null`, success value and total number of questions.
- Results are paginated in group of 10. Include a request argument to choose page number, starting from 1.
- Error of status code 404 will be thrown when there is no question on the given page.

#### Sample

`curl -X GET http://127.0.0.1:5000/questions?page=2`

```
"categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Agra",
      "category": "3",
      "difficulty": 2,
      "id": 11,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": "2",
      "difficulty": 1,
      "id": 12,
      "question": "Which Dutch graphic artist-initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": "2",
      "difficulty": 3,
      "id": 13,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": "2",
      "difficulty": 4,
      "id": 14,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": "2",
      "difficulty": 2,
      "id": 15,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "The Liver",
      "category": "1",
      "difficulty": 4,
      "id": 16,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": "1",
      "difficulty": 3,
      "id": 17,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": "1",
      "difficulty": 4,
      "id": 18,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Scarab",
      "category": "4",
      "difficulty": 4,
      "id": 19,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

### POST /questions

#### Create Question
- Creates a new question when submitted question is click on, should be fill question, answer, difficulty and category.
- Returns all paremeters of created question and success value.
- Error of status code 405 will be thrown when there is no paremeter filled on the new question.

#### Sample

`curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question":"Who Won world cup 2018?","answer":"France","difficulty":2,"category":6}'` 

```
{
"answer": "France",
  "category": "6",
  "difficulty": 2,
  "question": "Who Won world cup 2018?",
  "success": true
}
```

### POST /questions/search

#### Search Question/s
- if `searchTerm` is filled in json body, that will return question/s in case sensisitive with database values, if `searchTerm` is not filled, that will returns all questions, and return current category, success value and total_questions.
- Error of status code 404 will be thrown if you search for question not included in database.

#### Sample

`curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"Hematology is a branch"}' http://127.0.0.1:5000/questions/search` 

```
{
 "current_category": [
    "1"
  ],
  "questions": [
    {
      "answer": "Blood",
      "category": "1",
      "difficulty": 4,
      "id": 18,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 1
}

```

### DELETE /questions/`question_id`

- Deletes the question at given Id if it exists. Returns the id of the deleted question and success value
- If the question at given Id does not exist, error of status code 404 is returned.

#### Sample

`curl -X DELETE http://127.0.0.1:5000/questions/20` 

```
{
  "id": 5,
  "success": true
}

```

### POST /quizzes

- Returns one randomly chosen questions at given category (if specefied) and success value.
- If `previous_questions` is provided in request body, whey will be excluded from selecting process. 
- `question` is returned `null` if there is no more questions which has not previously played in the category. 

#### Sample

`curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"quiz_category":{"type":"Art","id":2},"previous_questions":[6]}'` 

```
{
  "question": {
    "answer": "Escher",
    "category": "2",
    "difficulty": 1,
    "id": 12,
    "question": "Which Dutch graphic artist-initials M C was a creator of optical illusions?"
  },
  "success": true
}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```