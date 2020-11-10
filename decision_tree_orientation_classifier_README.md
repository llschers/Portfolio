## Decision-Tree Model
 
My program first reads in the training data, line by line. It then assigns 
each line (vector) to a list based on the image's orientation. This is 
completed in the divide_training_by_orientation() function. 

For each of those lists of training vectors (one for each orientation), the 
node_training() function then iterates through the vectors 8X8X3 dimensions, 
finding where dimention_i > dimention_j for the most vectors in that list. 
This becomes the node of the tree used to classify that orientation. In 
order to keep track of which node is which, the orientation is appended 
to the node.

Next, the nodes are sorted based on the proportion of the vector list they 
correctly classified. 

The program then reads in the test data, line by line, and creates an 
output file. 

In order to calculated accuracy, the variable num_correct is initiated 
to keep track of how many test images are correctly estimated.

Then, each image vector in the test data is passed through the 
image_testing() function, which uses the trained nodes to estimate the 
orientation of each image. This is written line by line to the output file. 

Lastly, both test and output files are closed, and the proportion of test 
images correctly estimated is calculated. 

Notes

-I chose to keep the decision tree very simple, creating one node per 
classification. I also decided that the nodes would only be based on 
whether one value within the image vector was larger than another. 
By choosing to only make "greater than" comparisons, I was able to avoid 
choosing nodes that may have come from comparing a value to itself. 

-With the way the training data is given, with each image in the dataset 
4 times, once at each orientation, it ended up that the proportion of the 
correctly classified vector list for each orientation was the same. 
This makes sorting the nodes to use whichever one is most accurate first 
a moot point in this example. 

-The decision tree model currently estimates image orientation correctly 
only 40.1% of the time. While this is certainly better than blind chance 
(25%), it is not awe inspiring. 
