import numpy as np
import tensorflow as tf

# Generate sample data (list of integer arrays)
sequence_length = 3
data = [
    np.array([1, 2, 3, 4, 5, 6]),
    np.array([6, 7, 8, 9, 10, 6]),
    np.array([11, 12, 13, 14, 15, 6]),
    np.array([16, 17, 18, 19, 20, 6]),
    np.array([16, 17, 18, 19, 20, 3])
]

# Normalize data
# data_normalized = [sequence / int(max(sequence)) for sample in data]

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

# Generate a new sequence
def generate_sequence(model, seed_sequence, length):
    generated_sequence = seed_sequence.copy()

    for _ in range(length):
        # Reshape the input sequence
        input_sequence = np.reshape(generated_sequence[-sequence_length:], (1, sequence_length, 1))

        # Predict the next value
        predicted_value = model.predict(input_sequence)[0, 0]

        # Append the predicted value to the generated sequence
        generated_sequence = np.append(generated_sequence, predicted_value)

    return generated_sequence

# Generate a new sequence based on the trained model
seed_sequence = data[0][:sequence_length]
generated_sequence = generate_sequence(model, seed_sequence, length=5)

# Denormalize the generated sequence
#generated_sequence = generated_sequence * float(max(data[0]))

# Print the generated sequence
print("Generated Sequence:", np.array2string(generated_sequence))
for row in generated_sequence:
    if isinstance(row, int):
        print(row)
    else:
        print("Not an int")