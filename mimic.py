import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
import numpy as np
import os
import csv
import uuid


# Generate more synthetic data using the trained model
new_samples = 100
new_age = np.random.randint(21, 100, new_samples)
new_cig = np.random.uniform(0, 10, new_samples)
new_gen = np.random.randint(0, 2, size=new_samples)
new_race = np.random.randint(0, 5, size=new_samples)

new_data = np.column_stack((new_age, new_cig, new_gen, new_race))

# Split the data into training and testing sets
random_labels = np.random.randint(0, 1, size=new_samples)
X_train, _, _, _ = train_test_split(new_data, random_labels, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
_ = scaler.fit_transform(X_train)
new_data_scaled = scaler.transform(new_data)

mimic_genes = {}
gene_ids = []

with open("gene_id.txt", 'r') as file:
	lines = file.readlines()
	for line in lines:
		gene_id = line.strip()
		mimic_genes[gene_id] = []
		# Predict the gene for the new data
		model_path = f"models/pii_{gene_id}.keras"
		if os.path.exists(model_path):
			gene_ids.append(gene_id)
			model = keras.models.load_model(model_path)
			new_predictions = model.predict(new_data_scaled)

			for i in range(new_samples):
				mimic_genes[gene_id].append(new_predictions[i][0])

# # Display the results
# for i in range(new_samples):
# 		print(f"Age: {new_age[i]}, Cigarettes: {new_cig[i]}, Gender: {new_gen[i]}, Gene: {new_predictions[i][0]}")

with open("mimic.csv", 'w') as file:
	file.write("age,cigarettes_per_day,gender,race")
	for gene_id in gene_ids:
		file.write(f",{gene_id}")
	file.write('\n')
	for i in range(new_samples):
		file.write(f"{new_age[i]},{new_cig[i]},{new_gen[i]},{new_race[i]}")
		for gene_id in gene_ids:
			file.write(f",{int(mimic_genes[gene_id][i])}")
		file.write('\n')
