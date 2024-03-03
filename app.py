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
    highest_chance = random.choice(all_genes).strip()
    lowest_chance = random.choice(all_genes).strip()
    highest_expression = random.choice(all_genes).strip()
    lowest_expression = random.choice(all_genes).strip()
    strand1 = []
    strand2 = []
    strand3 = []
    strand4 = []
    for i in range(4):
        sequence = ''.join(random.choice('CTAG') for _ in range(random.randint(5, 38)))
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
        if i == 0:
            strand1.append(sequence)
            strand1.append(sequence2)
        elif i == 1:
            strand2.append(sequence)
            strand2.append(sequence2)
        elif i == 2:
            strand3.append(sequence)
            strand3.append(sequence2)
        elif i == 3:
            strand4.append(sequence)
            strand4.append(sequence2)
    random_chance = []
    for i in range(4):
        random_chance.append(random.randint(0, 100))
        random_chance.sort(reverse=True)
    random_strong = []
    for i in range(4):
        random_strong.append(random.randint(0, 100))
        random_strong.sort(reverse=True)
    return render_template("results.html", strand1=strand1, strand2=strand2, strand3=strand3, strand4=strand4, random_chance=random_chance, random_strong=random_strong, highest_chance=highest_chance, lowest_chance=lowest_chance, highest_expression=highest_expression, lowest_expression=lowest_expression)

if __name__ == "__main__":
    app.run()