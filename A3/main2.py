from __future__ import print_function
from random import randint
from math import log

N_ATTR = 6
VALUES = [1, 2];

TRAINING_DATA = 'training.txt'
TEST_DATA = 'test.txt'
ATTRIBUTES = [x for x in range(0,N_ATTR)]


class TreeNode:
    # A simple tree class.

    def __init__(self,label,classification):
        self.label = label
        self.children = []
        self.classification = classification

    def get_children(self):
        return self.children

    def get_label(self):
        return self.label

    def add_child(self, child):
        self.children.append(child)

    def set_label(self, label):
        self_label = label
    def set_classification(self, classi):
        self.classification = classi

def importance_random(attributes):
    return attributes[randint(0,len(attributes)-1)]


def B(q):
    if q == 1.0:
        return 0
    elif q == 0:
        return 0
    else:
        return -q*log(q,2) - (1.0-q)*log((1.0-q),2)

def entropy(data):
    p = 0
    n = float(len(data))

    if n==0:
        return 0

    for exs in data:
        if exs[N_ATTR] == 2:
            p += 1

    print(p,n)
    return B(p/n)
            


def entropy_attr(data, target_attr):
    """
    Calculates the entropy of the given data set for the target attribute.
    """
    l1 = []
    l2 = []


    # Calculate the frequency of each of the values in the target attr

    for exs in data:
        if exs[target_attr] == 1:
            l1.append(exs)
        elif exs[target_attr] == 2:
            l2.append(exs)

    print(l1,l2)
    entropy_l1 = (len(l1)/len(data))*entropy(l1)
    entropy_l2 = (len(l2)/len(data))*entropy(l2)

        
    return entropy_l1 + entropy_l2

def gain(data, attributes):
    """
    Calculates the information gain (reduction in entropy) that would
    result by splitting the data on the chosen attribute (attr).
    """
    target_entropy = entropy(data)
    attribute_gain = [-1] * N_ATTR 
    for attr in attributes:
        attribute_gain[attr] = target_entropy - entropy_attr(data, attr)


    index = 0
    value = -1
    print(attribute_gain)
    for attr in attributes:
        if attribute_gain[attr] > value:
            index = attr;
            value = attribute_gain[attr]
    return index
        
    
        
    
def importance_entropy(examples, attributes):
    attribute_gain = [-1] * N_ATTR

    for attr in attributes:
        attribute_gain[attr] = gain(examples,attributes)


    print("Gains: ", attribute_gain)

    val = -1
    index = 0
    for i in range(0,N_ATTR-1):
        if attribute_gain[i]>val:
            val = attribute_gain[i]
            index = i
    return i

def readAndParse(filename):
    # Read training data
    f = open(filename, 'r')

    # data file
    data = []

    # Read all numbers into an array of arrays. Also convert the values to ints.
    line = f.readline()
    while line != '':
        line = line.strip('\n').split('\t')
        for i in range(0,len(line)):
            line[i] = int(line[i])
        
        data.append(line)
        line = f.readline()

    return data

def plurality_classification(examples):
    #Function for finding the most commen classification among a set of examples
    if len(examples) == 0:
        return -1

    cat_1 = 0
    cat_2 = 0
    for ex in examples:
        if ex[N_ATTR] == 1:
            cat_1 = cat_1 + 1
        elif ex[N_ATTR] == 2:
            cat_2 = cat_2 + 1

    # Return the most commen classification:
    if cat_1 >= cat_2:
        return 1
    else:
        return 2

def all_equal_classification(examples):
    # Check if all the examples have the same classification
    if len(examples) == 0:
        return -1

    ex = examples[0]
    classification = ex[N_ATTR]

    for ex in examples:
        if ex[N_ATTR] != classification:
            return 0

    return classification



def decision_tree_learning(examples, attributes, parent_examples, importance):

    all_equal_class = all_equal_classification(examples)

    if len(examples) == 0:

        classification = plurality_classification(parent_examples)
        return TreeNode(-1, classification)

    elif all_equal_class > 0:
        return TreeNode(-1, all_equal_class)

    elif len(attributes) == 0:
        classification = plurality_classification(examples)
        return TreeNode(-1, classification)


    else:
        print(attributes)
        if importance:
            A = gain(examples, attributes)
        else:
            A = importance_random(attributes)
        print("Choosen attribute: ",A)
        tree = TreeNode(A, -1)
        attributes.remove(A)
        
        for value in VALUES:
            exs = []
            for ex in examples:
                if ex[A] == value:
                    exs.append(ex)
                
            sub_tree = decision_tree_learning(exs,list(attributes),examples, importance)
            if sub_tree != None: 
                sub_tree.set_classification(value)
                tree.add_child(sub_tree)   

            

    return tree




def print_tree_recursive(tree, level):
    if tree.get_children() == []:
        print('Label: ', tree.label, 'Branch: ', tree.branch)

    else:
        children = tree.get_children()
        for child in children:
            print_tree(child, level)

        print('')

def print_tree(root):
    current_level = root
    
    while current_level != [0]*len(current_level):
        next_level = [0] * 2 * len(current_level)
        for n in range(0,len(current_level)):
            if current_level[n] == 0:
                print("X", end = '')
            else:
                if current_level[n].label == -1:
                    print(''.join(('C',str(current_level[n].classification))), end = '')

                else:
                    print(''.join(('A',str(current_level[n].label))), end = '')

                children = current_level[n].get_children()

                for i in range(0,len(children)):
                    next_level[n*2+i]=children[i]
            
                
            
        current_level = next_level
        print('')
        


def classify(tree, example):
    current_tree = tree
    # while loop down the tree until we reach a classification node (label = -1)
    while current_tree.label != -1:
        # What is our value for this attribute?
        value = example[current_tree.label]
        # Continue traversin in right direction: Value = 1 means left node => children[0] and so on
        current_tree = current_tree.children[value-1]
    # Return the classification
    return current_tree.classification

def runTest(testData, decision_tree):
    # Allocate space for #of guesses and correct guesses.
    results= [0, 0]
    for examples in testData:
        results[0] += 1
        if classify(decision_tree,examples) == examples[N_ATTR]:
            results[1] += 1


    return results


if __name__ == '__main__':
    print("************************************************************************************")

    training_data = readAndParse(TRAINING_DATA)
    test_data = readAndParse(TEST_DATA)
    attributes = ATTRIBUTES

    final_tree = decision_tree_learning(training_data,attributes, [], importance = True)
    
    print_tree([final_tree])

    results = runTest(test_data, final_tree)

    print("Correct\Total: " + str(results[1]) + "\\" + str(results[0]))

