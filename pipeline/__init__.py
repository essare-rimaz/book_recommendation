r"""
# How to read this documentation
Normally my go-to method of commenting would be just the boring `# in-code comment` in the code I wrote.
However, I wanted to learn *pdoc* so I decided to use this case study as an opportunity.
This case study does not reflect my knowledge on how documentation of classes and methods should be done. It
was just a fun thing to do.
You can read all the comments in the `pipeline.classifier` submodule or directly from source in an IDE.

### Disclaimer
You can follow the guide on how to use `pipenv` or just install the libraries listed in `Pipfile` via `pip`.
In any case in order to run the code, you can follow the instructions at the end of this document.

# How to run this case study
This case study has a few assumptions
- project will be imported as is somewhere
- libraries and dependencies will be installed via pipenv

### Importing the project
Simply extract the zipped project directory on a computer
### Installing via pipenv
Pipenv is an alternative to pip. It comes with some solutions to pip so I prefer to use it.
It is very easy to use. Following is done within cmd or powershell:
- type the command `pip install pipenv`
- go to the project directory
- type `pipenv install`

The last command will:
- create a virtual environment
- install the libraries and dependencies I have used

Hopefully this will ensure we have the same ecosystem and you can run the case study smoothly.

# How to execute the pipeline
When all previous steps are done add the original dataset in the `data` folder and run
`python .\run.py`

"""