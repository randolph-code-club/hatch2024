from flask import Flask, render_template, request, make_response, redirect
import requests
from flask import Flask, send_file
import os
import random
import csv
import uuid

def list_genes():
    with open("gene_id.txt", 'r') as file:
        return file.readlines()
        
def select_mimic_genome(user_data):
    selected_genomes = []
    with open("mimic.csv", "r") as mimic_file:
        csv_reader = csv.DictReader(mimic_file, delimiter=",")
        for sample in csv_reader:
            if int(user_data["gender"]) == int(sample["gender"]) and int(user_data["race"]) == int(sample["race"]):
                if int(user_data["age"]) >= int(sample["age"]) - 3 and int(user_data["age"]) <= int(sample["age"]) + 3:
                    if int(user_data["cigs"]) >= int(round(float(sample["cigarettes_per_day"]))) - 2 and int(user_data["cigs"]) <= int(round(float(sample["cigarettes_per_day"]))) + 2:
                        selected_genomes.append(sample)
    return selected_genomes

def genome_file_name(id):
    return f"genome-{id}.csv"

app = Flask(__name__, instance_relative_config=True)

@app.route("/")
def index():
    error = request.args.get("error")
    if error == "true":
        message = "Please fill out all fields"
    else:
        message = ""
    return render_template("index.html", error_message=message)

@app.route("/download/<string:key>")
def download(key):
    return send_file(genome_file_name(key), as_attachment=True)

@app.route("/results", methods = ['POST'])
def results():
    try:
        # highest_chance = {'id':'', 'val':0}
        # lowest_chance = {}
        # highest_expression = {}
        # lowest_expression = {}
        form_data = request.form
        genome_id = str(uuid.uuid4())
        with open(genome_file_name(genome_id), "w") as genome_file:
        # Write each item from the list to the file
            first = True
            genomes = select_mimic_genome(form_data)
            for dict in genomes:
                if first:
                    for key in dict:
                        genome_file.write(f"{key},")
                    genome_file.write("\n")
                    first = False
                for key, item in dict.items():
                    genome_file.write(f"{item},")
                    # # if item > highest_chance['val']:
                    # #     highest_chance = {'id':key, 'val':int(item)}
                    # # if item < lowest_chance['val']:
                    # #     lowest_chance = {'id':key, 'val':int(item)}
                    # if item > highest_expression['val']:
                    #     highest_expression = {'id':key, 'val':int(item)}
                    # if item < lowest_expression['val']:
                    #     lowest_expression = {'id':key, 'val':int(item)}
                genome_file.write("\n")
    except Exception as e:
        return redirect("/?error=true")
        # total_expression = 0
        # for dict in genomes:
        #     total_expression += dict[highest_expression["id"]]
        # chance = total_expression / len(genomes)
    all_genes = list_genes()
    highest_chance = random.choice(all_genes).strip()
    highest_chance = highest_chance.split(".")[0]
    lowest_chance = random.choice(all_genes).strip()
    lowest_chance = lowest_chance.split(".")[0]
    highest_expression = random.choice(all_genes).strip()
    highest_expression = highest_expression.split(".")[0]
    lowest_expression = random.choice(all_genes).strip()
    lowest_expression = lowest_expression.split(".")[0]
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
    return render_template("results.html", strand1=strand1, strand2=strand2, strand3=strand3, strand4=strand4, random_chance=random_chance, random_strong=random_strong, highest_chance=highest_chance, lowest_chance=lowest_chance, highest_expression=highest_expression, lowest_expression=lowest_expression, genome_id=genome_id)

if __name__ == "__main__":
    app.run()