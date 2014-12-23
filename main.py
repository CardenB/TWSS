from flask import Flask
from flask import request
from flask import render_template
from TWSS import TWSS

app = Flask(__name__)
twss = TWSS()


@app.route('/')
def my_form():
    return render_template("my-form.html",
                           result="")


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.lower()
    if twss(processed_text):
        r = "That's what she said!"
    else:
        r = "Try something else."
    print r
    return render_template("my-form.html",
                           result=r)

if __name__ == '__main__':
    app.run()
