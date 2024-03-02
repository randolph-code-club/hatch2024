import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.utils import to_categorical

model = keras.models.load_model('gene.keras')

sequence_length = 3

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
seed_sequence = [0, 0, 0]
generated_sequence = generate_sequence(model, seed_sequence, length=5)

# Denormalize the generated sequence
#generated_sequence = generated_sequence * float(max(data[0]))

# Print the generated sequence
print("Generated Sequence:", np.array2string(generated_sequence))