import numpy as np
import tensorflow as tf
import os

directory_path = 'column_files/'

# Generate sample data (list of integer arrays)
sequence_length = 3
# data = [
#     np.array([1, 2, 3, 4, 5, 6]),
#     np.array([6, 7, 8, 9, 10, 6]),
#     np.array([11, 12, 13, 14, 15, 6]),
#     np.array([16, 17, 18, 19, 20, 6]),
#     np.array([16, 17, 18, 19, 20, 3])
# ]

# for each file in column files directory
# read the file and create an array from each line in the file
# add that array to data
files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

data = []

for file_name in files[:10]:
    sample = []
    file_path = os.path.join(directory_path, file_name)
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines[5638:6638]:
            sample.append(int(line.strip()))
    data.append(np.array(sample))
            

# Normalize data
#data_normalized = [sample / float(max(sample)) for sample in data]

# Create sequences and labels
def create_sequences_and_labels(data, sequence_length):
    sequences, labels = [], []
    for sequence in data:
        for i in range(len(sequence) - sequence_length):
            seq = sequence[i : i + sequence_length]
            label = sequence[i + sequence_length]
            sequences.append(seq)
            labels.append(label)
    return np.array(sequences), np.array(labels)

sequences, labels = create_sequences_and_labels(data, sequence_length)

# Reshape data for LSTM input (batch_size, sequence_length, features)
sequences = np.reshape(sequences, (sequences.shape[0], sequence_length, 1))

# Build the LSTM model
model = tf.keras.Sequential([
    tf.keras.layers.LSTM(50, input_shape=(sequence_length, 1)),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(sequences, labels, epochs=100, batch_size=1)
model.summary()
model.save("gene.keras")
