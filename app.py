from flask import Flask, render_template, request, make_response, redirect
import requests
from flask import Flask
import os
import random

app = Flask(__name__, instance_relative_config=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results", methods = ['POST'])
def results():
    sequence = ''.join(random.choice('CTAG') for _ in range(20))
    sequence2 = ""
    for nucleotide in sequence:
        if nucleotide == "A":
            sequence2 += "T"
        elif nucleotide == "T":
            sequence2 += "A"
        elif nucleotide == "C":
            sequence2 += "G"
        elif nucleotide == "G":
            sequence2 += "C"
    return render_template("results.html", sequence=sequence, sequence2=sequence2)

if __name__ == "__main__":
    app.run()