from flask import Flask, render_template, request, make_response, redirect
import requests
from flask import Flask
import os
import random

def list_genes():
    with open("gene_id.txt", 'r') as file:
        return file.readlines()
        

app = Flask(__name__, instance_relative_config=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results", methods = ['POST'])
def results():
    all_genes = list_genes()
    highest_chance = random.choice(all_genes)
    lowest_chance = random.choice(all_genes)
    highest_expression = random.choice(all_genes)
    lowest_expression = random.choice(all_genes)
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
    random_chance = random.randint(0, 100)
    random_strong = random.randint(0, 100)
    return render_template("results.html", sequence=sequence, sequence2=sequence2, random_chance=random_chance, random_strong=random_strong, highest_chance=highest_chance, lowest_chance=lowest_chance, highest_expression=highest_expression, lowest_expression=lowest_expression)

if __name__ == "__main__":
    app.run()