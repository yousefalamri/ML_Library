import math

############################# supporting functions ################################

# Load train.csv and test.csv
with open('train.csv') as f:
    training_data = [];
    for line in f:
        terms = line.strip().split(',')  # 7*N matrix
        training_data.append(terms)

with open('train.csv') as f:
    testing_data = [];
    for line in f:
        terms = line.strip().split(',')  # 7*N matrix
        testing_data.append(terms)

# Create empty dictionary to store attributes
def append_attribute(attribute):
    empty_dict = {}
    for each_attribute in given_attributes[attribute]:
        empty_dict[each_attribute] = []
    return empty_dict

# Empty dictionary for storing information gain values
def information_index_store(attributes):
    empty_dict = {}
    for each_attribute in attributes:
        empty_dict[each_attribute] = 0
    return empty_dict

# store attributes in a dictionary
given_attributes = {'buying': ['vhigh', 'high', 'med', 'low'],
             'maint': ['vhigh', 'high', 'med', 'low'],
             'doors': ['2', '3', '4', '5more'],
             'persons': ['2', '4', 'more'],
             'lug_boot': ['small', 'med', 'big'],
             'safety': ['low', 'med', 'high']}

# convert categorical data to numerical values to facilitate manipulation
def convert_attribute_to_num(attribute):
    numerical_attribute = 0
    if attribute == 'buying':
        numerical_attribute = 0
    elif attribute == 'maint':
        numerical_attribute = 1
    elif attribute == 'doors':
        numerical_attribute = 2
    elif attribute == 'persons':
        numerical_attribute = 3
    elif attribute == 'lug_boot':
        numerical_attribute = 4
    elif attribute == 'safety':
        numerical_attribute = 5
    return numerical_attribute

# function that divides data based on labels
def divide_data(attribute,input_data):
    child = append_attribute(attribute)
    for ith_element in input_data:
        for this_attribute in given_attributes[attribute]:
            numerical_attribute = convert_attribute_to_num(attribute)
            if ith_element[numerical_attribute] == this_attribute:
                child[this_attribute].append(ith_element)
    return child

# function that assigns most common label to a group
def find_common_label(group):
    labels = []
    for element in group:
        labels.append(element[-1])
    most_common_label = max(set(labels), key= labels.count)
    return most_common_label

# function that check whether a subset of data is pure
def Is_impure(branch):
    unique_label = []
    for indx in branch:
        if not (not branch[indx]):
            unique_label.append(indx)
    if len(unique_label) == 1:
        return False
    else:
        return True

# the following function returns gini index, entropy, and majority error for a set of data
def calculate_gini_index(groups, labels):
    total_elements = float(sum([len(groups[this_elem]) for this_elem in groups]))
    gini = 0.0
    for element in groups:
        group_size = float(len(groups[element]))
        if group_size == 0:
            continue
        sum_term = 0.0
        for label in labels:
            p = [this_label[-1] for this_label in groups[element]].count(label) / group_size
            sum_term += p**2
        weight = (group_size / total_elements)
        gini += (1.0 - sum_term) * weight
    return gini

def calculate_entropy(groups, labels):
    total_elements = float(sum([len(groups[this_elem]) for this_elem in groups]))
    entropy = 0.0
    for element in groups:
        group_size = float(len(groups[element]))
        if group_size == 0:
            continue
        sum_term = 0.0
        for label in labels:
            p = [this_label[-1] for this_label in groups[element]].count(label) / group_size
            if p == 0:
                sum_term = 0
            else:
                sum_term += (p * -1 * math.log(p,2))
        weight = (group_size / total_elements)
        entropy += sum_term * weight
    return entropy

def calculate_majority_error(groups, labels):
    total_elements = float(sum([len(groups[this_elem]) for this_elem in groups]))
    ME = 0.0
    for element in groups:
        group_size = float(len(groups[element]))
        if group_size == 0:
            continue
        me = 0.0
        majority = 0
        for label in labels:
            p = [this_label[-1] for this_label in groups[element]].count(label) / group_size
            majority = max(majority, p)
            me = 1 - majority
        weight = (group_size / total_elements)
        ME += me * weight
    return ME

# this function determines the best splitting feature using one of the three information indecies:
# to choose a specific index, change the function on line ~151 to one of the following:
# 1- calculate_gini_index(batches,labels); or
# 2- calculate_entropy(batches,labels); or
# 3- calculate_majority_error(batches,labels)
def best_splitting_feature(input_data):
    labels = []
    if input_data == []:
        return
    for element in input_data:
        labels.append(element[-1])
    info_index_value = information_index_store(given_attributes)
    for attribute in given_attributes:
        batches = divide_data(attribute,input_data)
        info_index_value[attribute] = calculate_gini_index(batches,labels)
        best_feature = min(info_index_value, key=info_index_value.get)
        best_subset = divide_data(best_feature,input_data)
    output = {'best_splitting_feature': best_feature, 'best_subset': best_subset}
    return output

# function that recursively split the data up to a maximum depth
def create_branch(branch, max_tree_depth, tree_depth):
    if not Is_impure(branch['best_subset']):
        for label in branch['best_subset']:
            if branch['best_subset'][label] != []:
                branch[label] = find_common_label(branch['best_subset'][label])
            else:
                branch[label] = find_common_label(sum(branch['best_subset'].values(), [ ]))
        return

    if tree_depth >= max_tree_depth:
        for label in branch['best_subset']:
            if branch['best_subset'][label] != []:
                branch[label] = find_common_label(branch['best_subset'][label])
            else:
                branch[label] = find_common_label(sum(branch['best_subset'].values(), []))
        return

    for label in branch['best_subset']:
        if branch['best_subset'][label] != []:
            branch[label] = best_splitting_feature(branch['best_subset'][label])
            #tree_depth +=1
            create_branch(branch[label], max_tree_depth, tree_depth + 1)
        else:
            branch[label] = find_common_label(sum(branch['best_subset'].values(), [ ]))



############################# Building the decision tree ################################

def Decision_Tree(input_data, max_tree_depth):
    first_layer = best_splitting_feature(input_data)
    create_branch(first_layer, max_tree_depth, 1)
    return first_layer

# choose either one of the following,  train.csv or test.csv
input_data = testing_data
input_data = training_data
max_tree_depth =6
decision_tree_car = Decision_Tree(input_data, max_tree_depth)

############################# calculate prediction error ################################

def check_label(branch, label):
    numeric_label = label[convert_attribute_to_num(branch['best_splitting_feature'])]
    predicted_label = branch[numeric_label]
    if isinstance(predicted_label, dict):
        return check_label(predicted_label, label)
    else:
        return predicted_label


############################# Building the decision tree ################################

def calculate_prediction_error(actual_label, predicted_label):
    inaccurate = 0
    for k in range(len(actual_label)):
        if actual_label[k] != predicted_label[k]:
            inaccurate += 1
        error_percentage = inaccurate / float(len(actual_label)) * 100.0
    return error_percentage


predicted_labels = []
actual_labels = []
for element in input_data:
    actual_labels.append(element[-1])
    pre = check_label(decision_tree_car, element)
    predicted_labels.append(pre)

#print(decision_tree_car)
print()
print('The prediction error percentage is ',calculate_prediction_error(actual_labels, predicted_labels))





