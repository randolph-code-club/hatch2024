import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
import os
import csv

gender_map = {
	"male": 0,
	"female": 1,
}

race_map = {
	"not reported": 0,
	"white": 1,
	"black or african american": 2,
	"american indian or alaska native": 3,
	"asian": 4
}

directory_path = 'column_files/'
files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

gene_ids = []
with open("gene_id.txt", 'r') as file:
	gene_ids = file.readlines()

luad_metadata = []
with open("LUAD_metadata.csv", 'r', newline='', ) as csvfile:
	csv_reader = csv.DictReader(csvfile, delimiter="\t")
	for row in csv_reader:
		luad_metadata.append(row)

def create_model(gene_row):
	labels = []
	ages = []
	cigarettes = []
	genders = []
	race = []
	gene_id = gene_ids[gene_row].strip()

	for file_name in files:
			file_path = os.path.join(directory_path, file_name)
			with open(file_path, 'r') as file:
					lines = file.readlines()
					sample_id = lines[0].strip()
					for row in luad_metadata:
						if row["external_id"] == sample_id:
								year_of_birth = row["gdc_cases.demographic.year_of_birth"].strip()
								cigarettes_per_day = row["gdc_cases.exposures.cigarettes_per_day"].strip()
								if year_of_birth != "" and year_of_birth != "NA":
									ages.append(2024 - int(year_of_birth))
									if cigarettes_per_day == "NA":
										cigarettes_per_day = "0"
									cigarettes.append(float(cigarettes_per_day))
									genders.append(gender_map[row["gdc_cases.demographic.gender"]])
									race.append(race_map[row["gdc_cases.demographic.race"]])
									labels.append(int(lines[gene_row].strip()))

	ages = np.array(ages)
	cigarettes = np.array(cigarettes)
	genders = np.array(genders)
	race = np.array(race)
	labels = np.array(labels)

	# for i in range(len(ages)):
	# 	print(f"Age: {ages[i]}, Cigarettes: {cigarettes[i]}, Gender: {genders[i]}, Race: {race[i]}, Gene: {labels[i]}")

	# Combine features into a matrix
	X = np.column_stack((ages, cigarettes, genders, race))

	# Split the data into training and testing sets
	X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

	# Standardize features
	scaler = StandardScaler()
	X_train_scaled = scaler.fit_transform(X_train)
	X_test_scaled = scaler.transform(X_test)

	# Build a simple regression model using TensorFlow
	model = tf.keras.Sequential([
			tf.keras.layers.Input(shape=(4,)),
			tf.keras.layers.Dense(64, activation='relu'),
			tf.keras.layers.Dense(1)
	])

	model.compile(optimizer='adam', loss='mse')

	# Train the model
	model.fit(X_train_scaled, y_train, epochs=50, batch_size=32, validation_data=(X_test_scaled, y_test))

	print(f"##### {i} - {gene_id}")
	model.summary()
	model.save(f"models/pii_{gene_id}.keras")

for i in range(5638+1000, 5638+2000):
	create_model(i)
