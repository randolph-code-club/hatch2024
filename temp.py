import numpy as np
import tensorflow as tf
import os

# Generate sample data
num_samples = 100
sequence_length = 1000

directory_path = 'column_files/'
files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

data = []

for file_name in files[0:num_samples]:
    sample = []
    file_path = os.path.join(directory_path, file_name)
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines[5638:(5638 + sequence_length)]:
            sample.append(int(line.strip()))
    data.append(np.array(sample))

print(np.max(data))

# # Creating a list of arrays containing 1000 integers
# data = [np.random.randint(0, 100, sequence_length) for _ in range(num_samples)]

# Convert the list of arrays to a NumPy array
data_array = np.array(data)

# Create a target variable (e.g., sum of integers in the array)
target = np.sum(data_array, axis=1)

# Split the data into training and testing sets
split_ratio = 0.8
split_index = int(num_samples * split_ratio)

X_train, X_test = data_array[:split_index], data_array[split_index:]
y_train, y_test = target[:split_index], target[split_index:]

# Build the neural network model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(sequence_length,)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)  # Output layer for regression
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# Evaluate the model on the test set
mse = model.evaluate(X_test, y_test)
print(f'Mean Squared Error on Test Set: {mse}')

# Generate a new integer array with the trained model
new_data = np.random.randint(0, 24393951, (1, sequence_length))
predicted_sum = model.predict(new_data)[0, 0]

print("\nGenerated New Integer Array:")
print(new_data)
print("\nPredicted Sum of the New Integer Array:", int(predicted_sum))
