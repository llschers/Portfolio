#!/usr/local/bin/python3
#
# decision_tree_orientation_classifier.py
#
# Code by: Leah Scherschel (llschers)
#
# Uses a decision tree to estimate the orientation.

# import os
# import sys
# import math
# import matplotlib
# import scipy
# import numpy


# Read in training data line by line
# Make lists of image vectors by orientation
def divide_training_by_orientation(training_file):
    vector_list0 = []
    vector_list90 = []
    vector_list180 = []
    vector_list270 = []
    data = open(training_file, "r")
    data1 = data.readlines()
    for line in data1:
        templine = line.split()
        orientation = int(templine[1])
        image_vector = list(map(int, templine[2:]))
        if orientation == 0:
            vector_list0.append(image_vector)
        elif orientation == 90:
            vector_list90.append(image_vector)
        elif orientation == 180:
            vector_list180.append(image_vector)
        elif orientation == 270:
            vector_list270.append(image_vector)
        else:
            pass
    data.close()
    return vector_list0, vector_list90, vector_list180, vector_list270


# select node that maximizes classification for each orientation
def node_training(image_vectors):
    node = [0, 0]
    length_of_vector = len(image_vectors[0])
    max_matches = 0
    for i in range(length_of_vector):
        for j in range(length_of_vector):
            current_matches = 0
            if i != j:
                for vector in image_vectors:
                    if vector[i] > vector[j]:
                        current_matches += 1
                if current_matches > max_matches:
                    max_matches = current_matches
                    node = [i, j]
    proportion_classified = max_matches/len(image_vectors)
    return [proportion_classified, node[0], node[1]]


# sort the list of nodes by the proportion_classified
def sort_nodes(node_list):
    sorted_list = sorted(node_list, key=lambda l:l[0])
    return sorted_list


# estimate an orientation for each image based on the nodes
def image_testing(vector, node_list):
    tempvector = vector.split()
    image_name = tempvector[0]
    orientation = int(tempvector[1])
    image_vector = list(map(int, tempvector[2:]))
    if image_vector[node_list[0][1]] > image_vector[node_list[0][2]]:
        est_orient = node_list[0][3]
    if image_vector[node_list[1][1]] > image_vector[node_list[1][2]]:
        est_orient = node_list[1][3]
    if image_vector[node_list[2][1]] > image_vector[node_list[2][2]]:
        est_orient = node_list[2][3]
    else:
        est_orient = node_list[3][3]
    if orientation == est_orient:
        correct = 1
    else:
        correct = 0
    return [image_name, est_orient, correct]


# Main function


if __name__ == "__main__":

    # currently have input file hard coded
    training_file = "train-data.txt"


    # make the list of training images with each orientation
    vector_list0, vector_list90, vector_list180, vector_list270 = divide_training_by_orientation(training_file)


    # train each node
    # add the orientation to each node
    node0 = node_training(vector_list0)
    node0.append(0)
    node90 = node_training(vector_list90)
    node90.append(90)
    node180 = node_training(vector_list180)
    node180.append(180)
    node270 = node_training(vector_list270)
    node270.append(270)


    # put the nodes in a list and sort based on the proportion correct by splitting the training data on that node
    node_list = [node0, node90, node180, node270]
    node_list = sort_nodes(node_list)


    # read in the test data line by line
    test_file = open("test-data.txt", "r")
    test_data = test_file.readlines()


    # create an output file to write to
    out_file = open("output.txt", "w")


    # variable to keep track of how many estimated orientations are correct
    num_correct = 0


    # pass the test data through the model, keeping track of the number correct
    for vector in test_data:
        [image_name, est_orient, correct] = image_testing(vector, node_list)
        num_correct += correct
        print(image_name, est_orient, file=out_file)

    test_file.close()
    out_file.close()


    # calculate the number of test images correctly classified
    accuracy = num_correct/len(test_data)

    print("Test completed with accuracy:", accuracy)