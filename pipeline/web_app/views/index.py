from flask import render_template, request, redirect, Blueprint

index = Blueprint("index", __name__)


#endpoint for home
@index.route('/', methods=['GET', 'POST'])
def index_home():
    return render_template('/index.html')
