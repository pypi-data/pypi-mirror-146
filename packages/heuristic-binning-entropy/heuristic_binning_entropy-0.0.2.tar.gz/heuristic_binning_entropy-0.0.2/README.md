# heuristic-binning-entropy

pip install heuristic-binning-entropy

from heuristic_binning_entropy.entHeuristicBinning import entropyHeuristicBinning


import numpy as np
inp = np.random.random(200)*100

a , b , c , d = entropyHeuristicBinning.heuristicbinning(inp)

### suggested number of bins
a

### steps of number of bins for plotting
b

### entropy measure by number of bins for plotting
c

### logistic function fitted , measure of entropy for plotting
d
