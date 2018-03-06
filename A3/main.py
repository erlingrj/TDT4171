from random import random

N_ATTR = 6
VALUES = [1, 2];

TRAINING_DATA = 'training.txt'
TEST_DATA = 'test.txt'
ATTRIBUTES = [x for x in range(0,N_ATTR)]


class TreeNode:
    # A simple tree class.
    parent = None
    children = []
    label = None
    branch = ''

    def __init__(self,parent, label):
        self.parent = parent
        self.label = label

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children

    def get_label(self):
        return self.label

    def add_parent(self, parent):
        self_parent = parent

    def add_child(self, child):
        self.children.append(child)

    def set_label(self, label):
        self_label = label
    def set_branch(self, branch):
        self_branch = branch



def importance_random(examples, attribute):
    return random()


def readAndParse(filename):
    # Read training data
    f = open(filename, 'r')

    # data file
    data = []

    # Read all numbers into an array of arrays. Also convert the values to ints.
    line = f.readline()
    while line != '':
        data.append(map(int, line.strip('\n').split('\t')))
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


def decision_tree_learning(examples, attributes, parent_examples):

    all_equal_class = all_equal_classification(examples)

    if len(examples) == 0:

        label = plurality_classification(parent_examples)
        tree = TreeNode(parent=None, label = label)
        return tree

    elif all_equal_class > 0:

        tree= TreeNode(parent=None, label = all_equal_class)
        return tree

    elif len(attributes) == 0:
        label = plurality_classification(examples)
        tree = TreeNode(parent=None, label = label)
        return tree


    else:
        # Find most important attribute
        check = -1
        most_important_attr = -1
        for attr in attributes:
            importance = importance_random(examples, attr)
            if importance > check:
                check=importance
                most_important_attr = attr

        A = most_important_attr
    
        tree = TreeNode(parent=None, label = str(A))

        # LES HERIFRA
        for value in VALUES:
            exs_ = []
            for ex in examples:
                if ex[A] == value:
                    exs.append(ex)

            print("A: ", A)
            print("value: ",value)
            print("Number of examples: ", len(examples), len(exs))
            
            new_attributes = attributes[:]
            new_attributes.remove(A)
            print("remaining attributes: ", new_attributes)
            print('\n')
                
            sub_tree = decision_tree_learning(exs,new_attributes,examples)

            sub_tree.add_parent(tree)
            tree.add_child(sub_tree)

            branch = str(A) + "=" + str(value)
            sub_tree.set_branch(branch)

        attributes.remove(A)

        return tree

        # TIL HIT: NOE ER FEIL.



def print_tree(tree):
    print(tree)
    print(tree.children[0])
    print(tree.children[0].children[0])



if __name__ == '__main__':

    examples = readAndParse(TRAINING_DATA)
    attributes = ATTRIBUTES

    final_tree = decision_tree_learning(examples,attributes, [])

    print_tree(final_tree)
