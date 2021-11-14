# What is a Transition Matrix?
A <code>Transition Matrix</code> presents data about the number of observations that started in a specific segment or status (typically, the rows) and in which segment or status they ended up in within a certain time period (normally, the columns).

# Purpose of this program
Provide the basis to create transition matricces for n-time periods.

# Dependencies
None.

# Functions
<code>TransitionMatrix</code>: Creates a matrix with the observations' starting status in the rows, and the final status in the columns. If you do not want to change the status of missing values, you may write <code>convertNA = FALSE</code> when calling the function.

<code>MissingConversion</code>: Converts a missing observation into a specific segment or pool (pre-defined to be "Others").

# Additional information
It is expected for each observation to have a segment or status defined within each time period under assessment, and the variable must be defined within the vector <code>segments</code>.
