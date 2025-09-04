import numpy as np
import math
import os
from . import SG

# Use relative path to find the simulation output file
current_dir = os.path.dirname(os.path.abspath(__file__))
sim_file_path = os.path.join(current_dir, "output.sim")

# Check if output.sim exists in current directory, if not check parent directory
if not os.path.exists(sim_file_path):
    sim_file_path = os.path.join(os.path.dirname(current_dir), "output.sim")

file = open(sim_file_path, "r")
files_tokens = file.readlines()
files_tokens_of_tokens = []

for i in range(len(files_tokens)):
    # Simple tokenization by splitting on commas and stripping whitespace
    tokens = [token.strip() for token in files_tokens[i].split(',')]
    files_tokens_of_tokens.append(tokens)

z = 0
for i in range(len(files_tokens_of_tokens)):
    if int(files_tokens_of_tokens[i][0]) > int(z):
        z = files_tokens_of_tokens[i][0]

t = np.arange(math.floor(int(z)*1.5))
SG.graph_all_outs(t,files_tokens_of_tokens, len(files_tokens) , int(int(z)*1.5) , 5)
