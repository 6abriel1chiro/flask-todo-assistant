from flask import Flask, render_template , url_for, request


app = Flask(__name__)

@app.route("/")
def home():
        return render_template('home.html')

@app.route("/login", methods=['GET','POST'])
def login():
        return render_template('login.html')
