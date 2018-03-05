

# Read training data
f = open('training.txt', 'r')


data = []

# Read all numbers into an array of arrays. Also convert the values to ints.
line = f.readline()
while line != '':
    data.append(map(int, line.strip('\n').split('\t'))) 
    line = f.readline()



