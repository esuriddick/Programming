# What is a (probability) tree diagram?
A <code>(probability) tree diagram</code> allows a person to better assess the probabilities underlying random events that happen in a pre-defined time sequence. Two important features underlying the probabilities in the nodes of the tree are: i) conditional probabilities (<code>Bayes Theorem</code>); and ii) the fact that the multiplication of the probabilities along the nodes provides the probability of the intersection of the events along the nodes.

# Purpose of this program
Provide the basis to easily create a custom tree diagram within R, which can be exported as an image.

# Dependencies
<code><a href="https://cran.r-project.org/web/packages/data.tree/">data.tree</a></code>: this library, including its dependencies, are required to properly create the tree diagram.

# Functions
<code>AddNode</code>: allows to create a new node on the tree diagram. There are 7 arguments to this function, namely:
* <code>parentnode</code>: identifies the full name of the node from which the new node will start from. The value for <code>parentnode</code> should be <code>NA</code> only when we are adding a root node to the tree.
* <code>name</code>: the name to be considered for the new node/event. It should always be filled in.
* <code>prob</code>: the probability underlying the node (e.g., the probability of reaching the node). The value for <code>prob</code> should be <code>NA</code> only when we are adding a root node to the tree.
* <code>tree_level</code>: indicates at what level of the tree will be the new node. For the root node, a value of <code>0</code> should be assigned.
* <code>node_type</code>: indicates whether the new node will be <code>start</code> (root node), <code>decision_node</code> (intermediate node) or <code>terminal</code> (final node). It should be noted that for every last node, a node named <code>overall</code> should be created and classified as a terminal node. As the number of levels to be displayed in the tree are customisable, you may hide these "artificial" nodes in the final tree diagram (see the example in the code for a better understanding).
* <code>overall_prob</code>: it should always be defined as <code>FALSE</code> for the nodes classified as <code>start</code> or <code>terminal</code>.
* <code>prob_rank</code>: determines the ranking of the probabilities (e.g., which one is the highest, second highest and so on). It should always be set to <code>NA</code>. In the function <code>MakeTree</code>, this variable is automatically filled for the <code>terminal</code> nodes.

<code>MakeTree</code>: draws a tree diagram based on 4 arguments, namely:
* <code>df</code>: the dataframe with the data created according to the function <code>AddNode</code>. By default, the value assigned in the code to this dataframe is <code>data</code>.
* <code>display_level</code>: the amount of levels of the tree to be displayed. By default, the maximum available number of levels are considered (<code>max(data$tree_level)</code>).
* <code>show_rank</code>: whether to show the ranking of the probabilities underlying the intersection of the events (that is, the probability of reaching a specific <code>overall</code> node).
* <code>direction</code>: whether to draw the tree diagram from left to right (<code>'LR'</code>), right to left (<code>'RL'</code>) or from top to bottom (<code>'TB'</code>). In order to draw from top to bottom, it does not really matter what you write, as long as you do not write <code>'LR'</code> or <code>'RL'</code>.

# Additional information
The code created is based on the explanation and example provided in <a href="https://www.datakwery.com/project/tree/">DataKwery</a>, where one of the authors explains how to use the library data.tree with a dataframe for the purpose of drawing a tree diagram.
