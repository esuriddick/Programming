#/****************************************************************************************/#
#/ MODERN PORTFOLIO THEORY
#/****************************************************************************************/#

#/ MODULES
#/****************************************************************************************/#
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.optimize as sco
import yfinance as yf
from datetime import datetime

#/ INPUTS
#/****************************************************************************************/#
#Parameters
tickerSymbols = ['XOM', 'SHW', 'JPM', 'AEP', 'UNH', 'AMZN',
                 'KO', 'BA', 'AMT', 'DD', 'TSN', 'SLG']
start_date = datetime.strptime('13/09/2011', "%d/%m/%Y")
end_date = datetime.strptime('20/09/2021', "%d/%m/%Y")
number_simulations = 10000
workdays = 252  #Working days in a year
seed = 101

#Historical data
dict_hist_price = {}
dict_hist_dividends = {}

##Get data of the tickers
for x in tickerSymbols:
    #Obtain the historical close prices for this ticker (adjusted for splits and dividend and/or capital gain distributions)
    dict_hist_price[x] = yf.Ticker(x).history(period='1d',
                                              start=start_date,
                                              end=end_date)['Close']
    #Obtain the dividends for this ticker
    dict_hist_dividends[x] = yf.Ticker(x).history(period='1d',
                                                  start=start_date,
                                                  end=end_date)['Dividends']
    
#Create dataframe with adjusted closing prices and dividends
closing_prices_dict = {k: dict_hist_price.get(k, 0) + dict_hist_dividends.get(k, 0) for k in dict_hist_price.keys() | dict_hist_dividends.keys()}
closing_prices = pd.DataFrame(closing_prices_dict)

#Calculate returns
dict_returns = {}
for x in tickerSymbols:
    #Obtain the logarithmic returns from the closing prices
    dict_returns[x] = np.log(closing_prices[x] / closing_prices[x].shift(1))
returns = pd.DataFrame(dict_returns)
returns = returns.iloc[1: , :]  #To drop the missing values in the first row

#Determine the (annualised) covariance matrix
cov_matrix = returns.cov() * workdays

#Basic functions
def port_return_calc(factor):
    value = np.sum(returns.mean() * factor)
    value = (1 + value) ** workdays - 1
    return(value)

def port_sd_calc(factor):
    return(np.sqrt(np.dot(factor.T, np.dot(cov_matrix, factor))))

#/ APPROACH: MONTE-CARLO SIMULATION
#/****************************************************************************************/#
#Basic setup
np.random.seed(seed)
portfolios_weights = np.zeros((number_simulations, len(returns.columns)))
portfolios_returns = np.zeros((number_simulations))
portfolios_risk = np.ones((number_simulations))
sharpe_ratio = np.zeros((number_simulations))

#Engine
for x in range(number_simulations):
    # Portfolio weights
    weights = np.random.uniform(size=len(returns.columns))
    weights = weights / np.sum(weights)
    portfolios_weights[x, :] = weights

    # Portfolio return
    portfolio_return = port_return_calc(weights)
    portfolios_returns[x] = portfolio_return

    # Portfolio risk
    portfolio_sd = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    portfolios_risk[x] = portfolio_sd

    # Portfolio Sharpe Ratio, assuming 0% Risk Free Rate
    ratio = portfolio_return / portfolio_sd
    sharpe_ratio[x] = ratio

    # Save portfolios of interest (min var, max return and max SR)
    if ratio >= max(sharpe_ratio[0:-1]):
        max_sharpe_ratio_return = portfolio_return
        max_sharpe_ratio_risk = portfolio_sd
        max_sharpe_ratio_weights = weights
        max_sharpe_ratio = ratio

    if portfolio_return >= max(portfolios_returns[0:-1]):
        max_return_return = portfolio_return
        max_return_risk = portfolio_sd
        max_return_weights = weights

    if portfolio_sd <= min(portfolios_risk[0:-1]):
        min_variance_return = portfolio_return
        min_variance_risk = portfolio_sd
        min_variance_weights = weights

#/ APPROACH: PROBLEM OPTIMISATION
#/****************************************************************************************/#
#Maximum Sharpe-ratio Portfolio
##Objective function (negative sign since it is a minimisation problem)
def sharpe_fun(factor):
    return(-port_return_calc(factor) / port_sd_calc(factor))

##Constraints
###Sum of weights must be equal to 1
constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})  #Sum of weights must be equal to 1
###Weights must be between 0 and 1
bounds = tuple((0, 1) for w in weights)

##Starting point (relevant for local minimum)
starting_weights = np.array([1 / len(tickerSymbols)] * len(tickerSymbols))

##Optimisation (local minimum)
opt_max_sharpe_ratio_weights = sco.minimize(
    fun = sharpe_fun,
    x0 = starting_weights,
    method = 'SLSQP',
    bounds = bounds,
    constraints = constraints)['x']
opt_max_sharpe_ratio_return = port_return_calc(opt_max_sharpe_ratio_weights)
opt_max_sharpe_ratio_risk = port_sd_calc(opt_max_sharpe_ratio_weights)

#Minimum Variance Portfolio
opt_min_variance_weights = sco.minimize(
    fun = port_sd_calc,
    x0 = starting_weights,
    method = 'SLSQP',
    bounds = bounds,
    constraints = constraints)['x']
opt_min_variance_return = port_return_calc(opt_min_variance_weights)
opt_min_variance_risk = port_sd_calc(opt_min_variance_weights)

#/ EFFICIENT FRONTIER
#/****************************************************************************************/#
#Parameters
number_of_points = 700

#Returns to plot in the efficient frontier
target = np.linspace(
    start = opt_min_variance_return, 
    stop = opt_min_variance_return + 0.2,
    num = number_of_points
    )

#Constraints
##Portfolio return must match the target return & sum of weights must be equal to 1
constraints = (
    {'type': 'eq', 'fun': lambda x: port_return_calc(x) - target},
    {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
    )
##Weights must be between 0 and 1
bounds = tuple(
    (0, 1) for w in weights
    )

#Initialize empty container for the objective values to be minimized
obj_sd = []

#For loop to minimize objective function
for target in target:
  min_result_object = sco.minimize(
      fun = port_sd_calc,
      x0 = starting_weights,
      method = 'SLSQP',
      bounds = bounds,
      constraints = constraints
      )
  # Extract the objective value and append it to the output container
  obj_sd.append(min_result_object['fun'])
#End of for loop

#Convert list to array
obj_sd = np.array(obj_sd)
obj_sd[0] = opt_min_variance_risk   #To ensure that the MVP is the first point

# Rebind target to a new array object
target = np.linspace(
    start = opt_min_variance_return, 
    stop = opt_min_variance_return + 0.2,
    num = number_of_points
    )

#/ GRAPHICAL DEPICTION
#/****************************************************************************************/#
#Join returns and standard deviation into a single dataframe
graphical_data = pd.DataFrame(data ={'std': obj_sd, 'return': target})

#Create a lagged variable for std
graphical_data['lag_std'] = graphical_data['std'].shift(periods = 1)

#Create function to determine whether the std value is repeated
def is_x_value_repeated(t, lag_t):
    if pd.isna(lag_t):
        return(0)
    elif round(t, ndigits=6) == round(lag_t, ndigits=6):
        return(1)
    else:
        return(0)

#Create flag for x-value repetition (6 digits)
graphical_data['flag'] = graphical_data.apply(lambda x: is_x_value_repeated(x['std'], x['lag_std']), axis=1)

#Select only non-repeatable x-values (with 6 decimal places) and drop additional columns
graphical_data = graphical_data[graphical_data['flag'] == 0]
graphical_data.drop(['lag_std', 'flag'], axis = 1, inplace = True)

#Create a scatterplot for the Efficient Frontier
sns.scatterplot(x = 'std', y = 'return', data = graphical_data)
plt.xlabel('Standard Deviation')
plt.ylabel('Returns of the portfolio')
plt.title('Efficient Frontier')