# What is a (probability) tree diagram?
A <code>(probability) tree diagram</code> allows a person to better assess the probabilities underlying random events that happen in a pre-defined time sequence. Two important features underlying the probabilities in the nodes of the tree are: i) conditional probabilities (<code>Bayes Theorem</code>); and ii) the fact that the multiplication of the probabilities along the nodes provides the probability of the intersection of each event along the nodes.

# Purpose of this program
Provide the basis to easily create a custom tree diagram within R, which can be exported as an image.

# Dependencies
<code><a href="https://cran.r-project.org/web/packages/data.tree/">data.tree</a></code>: this library, including its dependencies, are required to properly create the tree diagram.

# Functions
<code>AddNode</code>: allows to create a new node on the tree diagram. There are 7 arguments to this function, namely:
* <code>parentnode</code>: identifies the full name of the node from which the new node will start from. The value for <code>parentnode</code> should be <code>NA</code> only when we are adding a root node to the tree.
* teste
parentnode = NA, 
                   name,
                   prob = NA,
                   tree_level,
                   node_type,
                   overall_prob = FALSE,
                   prob_rank = NA
