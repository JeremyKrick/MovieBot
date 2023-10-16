from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
import secrets
from flask_bootstrap import Bootstrap5
from flask_wtf.csrf import CSRFProtect
from ChatForm import ChatForm
from extentions import csrf
import os

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]
def create_app():
    app = Flask(__name__)
    app_secret = secrets.token_urlsafe(16)
    app.config['SECRET_KEY'] = app_secret
    app.config['SESSION_COOKIE_DOMAIN'] = False
    return app
app = create_app()
# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
csrf.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ChatForm()
    print(form.content)
    print("form content: ", form.content.data)
    if form.validate_on_submit():
        print("form submitted")
    #     print("Request: ", request)
    #     print("form data", form)
        # messages.append({'title': form.name.data, 'content': form.message.data})
        # form.name.data = ''
        # form.message.data = ''
    if request.method == 'POST':
        print("Post requested: ", form)
        # request.form['content'] = form.content.data
        

    return render_template('index.html', form=form)

@app.route('/read-form', methods=['POST'])
def read_form():
    data = request.form['content']
    print("data: ", data)
    return {
        "data": data
    }

@app.route('/call', methods=['GET', 'POST'])
def callOpenAI():
    api_key = os.environ.get('OPENAI_API_KEY')
    print("api_key: ", api_key)  
    return render_template('form.html', messages=messages, response="response")