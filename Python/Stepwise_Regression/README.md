# Purpose of this program
Perform bi-directional stepwise regression in line with what SAS performs using either linear or logistic regression, but which can be further refined for other distributions and link functions.

# Dependencies
- Pandas (https://pandas.pydata.org/docs/getting_started/install.html)
- Statsmodels (https://www.statsmodels.org/stable/install.html)
- Scipy (https://scipy.org/install/)

# StepwiseGLM function's Parameters
- _model_type_: it accepts either 'linear' or 'logistic' as arguments, and it defines whether it will develop a linear or logistic regression.
- _endog_: defines which pandas Series contains the values for the target variable.
- _reverse_y_: if this is set to True, the target variable will be transformed by applying the following function: endog = abs(endog−1).
- _exog_: defines which pandas DataFrame contains the various potential explanatory variables.
- _CLASS_TREATMENT_: it accepts either ‘drop’, ‘sas’, ‘dummy’ or ‘dummy_dropfirst’, and it defines the treatment performed for the categorical variables.
- _SCRITERIA_: it accepts either ‘z’, ‘aic’ or ‘bic’, and it defines whether it should only look at hypothesis testing results based on the z-statistic (‘z’), or if it should also consider either the Akaike Information Criterion (‘aic’) or Bayesian Information Criterion (‘bic’). It should be noted that, in the case of a logistic regression, the p-value calculations are based on the chi-square distribution with 1 degree of freedom.
- _SLENTRY_: defines the largest p-value amount accepted for a variable to be considered in the model.
- _SLSTAY_: defines the largest p-value amount required for a variable to remain in the model after being included.
