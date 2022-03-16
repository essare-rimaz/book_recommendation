### How to run it

Install the context and library management
```commandline
pip install pipenv
```
When in the project root start a venv
```commandline
pipenv shell
```
Use Pipfile and Pipfile.lock to install the dependencies
```commandline
pipenv install
```
Start the project using `run.py` and follow the instructions
provided within the command line (input etc.)

### TODO

- create pdoc - improve documentation
- ~~make a visualization of the distribution of all ratings~~
- make a visualization of the distribution of mean ratings
- allow multiple arguments for argparse to avoid ambiguity
- resolve duplicated book-titles + authors
- build a database
- turn it into a flask/django web app
  - https://medium.com/@joseortizcosta/search-utility-with-flask-and-mysql-60bb8ee83dad
- version history?