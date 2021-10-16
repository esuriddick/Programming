# What is Monte-Carlo simulation?
As presented in Investopedia (<a href="https://www.investopedia.com/terms/m/montecarlosimulation.asp">HERE</a>):

"<code>Monte Carlo simulations</code> are used to model the probability of different outcomes in a process that cannot easily be predicted due to the intervention of random variables. It is a technique used to understand the impact of risk and uncertainty in prediction and forecasting models.

A <code>Monte Carlo simulation</code> can be used to tackle a range of problems in virtually every field such as finance, engineering, supply chain, and science. It is also referred to as a multiple probability simulation."

# Purpose of this program
Provide the basis to run a Monte-Carlo simulation. Normal distributions are used in both functions, which are easily changed to another distribution that suits your needs (see for other distributions: https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Distributions.html).

# Dependencies
None.

# Functions
<code>generate.path</code>: based on the initial value, it applies either a cumulative product or cumulative sum process in order to determine what the final value would be after "x" timesteps. By default, it assumes a cumulative product process, since the variable typically modelled for asset evaluation is returns, which is in percentage.

<code>generate.values</code>: provides "x" amount of outcomes according to the underlying statistical distribution.

# Additional information
None.
