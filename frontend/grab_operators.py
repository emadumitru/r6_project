import os
import json

# Define paths to the attacker and defender directories
attacker_path = 'data/operators_images/att'
defender_path = 'data/operators_images/def'
output_path = 'data'  # Directory where JSON files will be saved

# Function to create a dictionary of operators from a directory
def get_operators(directory):
    operators = {}
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            # Extract the operator name by removing the prefix and extension
            operator_name = filename.split('-')[1].replace('.png', '')
            # Store the operator name and corresponding image path
            operators[operator_name.capitalize()] = f"https://r6operators.marcopixel.eu/icons/svg/{operator_name.lower()}.svg"
    return operators

# Get dictionaries of attackers and defenders
attackers = get_operators(attacker_path)
defenders = get_operators(defender_path)

# Save the dictionaries as JSON files
def save_dict_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Saving the attackers and defenders dictionaries
save_dict_to_json(attackers, os.path.join(output_path, 'attackers.json'))
save_dict_to_json(defenders, os.path.join(output_path, 'defenders.json'))

# Display the resulting dictionaries (for debugging purposes)
print("Attackers:", attackers)
print("Defenders:", defenders)
