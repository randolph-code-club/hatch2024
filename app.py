from flask import Flask, render_template, request, make_response, redirect
import requests
from flask import Flask
import os

app = Flask(__name__, instance_relative_config=True)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()