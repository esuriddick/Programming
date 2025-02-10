#-----------------------------------------------------------------------------#
# MODULES
#-----------------------------------------------------------------------------#
import pandas as pd
import statsmodels.api as sm
from scipy.stats import chi2
import warnings

#-----------------------------------------------------------------------------#
# DATA
#-----------------------------------------------------------------------------#

# Load inputs
#-----------------------------------------------------------------------------#
df = pd.read_csv(r"C:\Users\...\example.csv")

# Define the independent (X) and dependent (y) variables
#-----------------------------------------------------------------------------#
y = df['BAD'].copy()
x_columns = list(df.loc[:1, (df.columns != 'BAD')].columns
                 .values)
X = df[x_columns].copy()

#-----------------------------------------------------------------------------#
# STEPWISE REGRESSION
#-----------------------------------------------------------------------------#
def StepwiseGLM(MODEL_TYPE = 'linear' #'logistic' or 'linear'
                ,ENDOG = y
                ,EXOG = X
                ,REVERSE_Y = False
                ,CLASS_TREATMENT = 'sas' #'drop', 'sas','dummy' or 'dummy_dropfirst'
                ,SCRITERIA = 'z' #'z', 'aic' or 'bic'
                ,SLENTRY = 0.05
                ,SLSTAY = 0.05):
    r"""
    Function that performs bi-directional stepwise regression in line with what SAS performs using either linear or logistic regression, but which can be further refined for other distributions and link functions.
    
    Parameters
    ----------
    MODEL_TYPE : string
    
    It accepts the values 'linear' (default) or 'logistic'. In the absence of a valid value, a linear regression model is assumed.
    
    ENDOG : pd.Series or list
    
    List or pd.Series containing the values of the target variable.
    
    EXOG : pd.DataFrame
    
    pd.DataFrame containing the values for each of the independent variables.
    
    REVERSE_Y : bool
    
    if this is set to True, the target variable will be transformed by applying the following function: ENDOG = abs(ENDOG−1). This functionality is only intended for binary target variables with a value of 0 or 1.
    
    CLASS_TREATMENT : string
    
    It accepts either 'drop', 'sas' (default), 'dummy' or 'dummy_dropfirst', and it defines the treatment performed for the categorical variables.
    
    SCRITERIA : string
    
    It accepts either 'z', 'aic' or 'bic', and it defines whether it should only look at hypothesis testing results based on the z-statistic ('z'), or if it should also consider either the Akaike Information Criterion ('aic') or Bayesian Information Criterion ('bic').
    
    'aic' is generally preferred when the primary goal is prediction accuracy since it is more lenient in allowing additional parameters, which can lead to more complex models being selected, while 'bic' is often recommended when the focus is on model selection with a stricter penalty for overfitting, especially in large datasets, as it tends to favor simpler models.
    
    It should be noted that, in the case of a logistic regression, the p-value calculations are based on the chi-square distribution with 1 degree of freedom.
    
    SLENTRY : integer or float
    
    Defines the largest p-value amount accepted for a variable to be considered in the model. It must be contained in the interval [0; 1].
    
    SLSTAY : integer or float
    
    Defines the largest p-value amount required for a variable to remain in the model after being included. It must be contained in the interval [0; 1].
    """
    
    
    #-------------------------------------------------------------------------#
    # FUNCTIONS
    #-------------------------------------------------------------------------#
    
    # Regression Model
    #-------------------------------------------------------------------------#
    def regressor(y, X, MODEL_TYPE = MODEL_TYPE):
        if MODEL_TYPE.lower() == 'linear':
            family = sm.families.Gaussian(link = sm.families.links.Identity())
        elif MODEL_TYPE.lower() == 'logistic':
            family = sm.families.Binomial(link = sm.families.links.Logit())
        regressor = sm.GLM(endog = y
                           ,exog = X
                           ,missing = 'drop'
                           ,family = family).fit(method = 'IRLS'
                                                 ,tol = 1e-08
                                                 ,maxiter = 100
                                                 ,use_t = False
                                                 ,warn_convergence = True)
        return regressor
       
    # P-values Storage
    #-------------------------------------------------------------------------#
    def store_results_pvals(df
                            ,col_name
                            ,col_var
                            ,var_name
                            ,var_value):
        new_row = {col_name: var_name
                   ,col_var: var_value}
        df.loc[len(df.index)] = new_row
        return
    
    # (Additional) Stopping Criteria
    #-------------------------------------------------------------------------#
    def stopping_criterion_check(ENDOG
                                 ,EXOG
                                 ,SCRITERIA
                                 ,old_vars
                                 ,new_vars):
        
        # Default value
        var_pass = False
        
        # Was either AIC or BIC selected?
        if SCRITERIA.lower() == 'aic' or SCRITERIA.lower() == 'bic':
        
            # Run both models
            old_model = regressor(ENDOG, EXOG[old_vars] * 1)
            new_model = regressor(ENDOG, EXOG[new_vars] * 1)
            
            # Akaike Information Criterion (AIC)
            if SCRITERIA.lower() == 'aic':
                
                # Compute AIC
                old_model_aic = old_model.aic
                new_model_aic = new_model.aic
                
                # Determine whether AIC improved
                if new_model_aic < old_model_aic:
                    var_pass = True
                    old_model_aic = round(old_model_aic, 4)
                    new_model_aic = round(new_model_aic, 4)
                    intro = "Stopping Criterion: "
                    outcome = f"AIC improved ({old_model_aic} -> {new_model_aic})"
                    message_log = intro + outcome + "\n"
                else:
                    old_model_aic = round(old_model_aic, 4)
                    new_model_aic = round(new_model_aic, 4)
                    intro = "Stopping Criterion: "
                    outcome = f"AIC deteriorated ({old_model_aic} -> {new_model_aic})"
                    message_log = intro + outcome + "\n"
            
            # Bayesian Information Criterion (BIC)
            else:
                # Compute AIC
                old_model_bic = old_model.bic_llf
                new_model_bic = new_model.bic_llf
                
                # Determine whether BIC improved
                if new_model_bic < old_model_bic:
                    var_pass = True
                    old_model_bic = round(old_model_bic, 4)
                    new_model_bic = round(new_model_bic, 4)
                    intro = "Stopping Criterion: "
                    outcome = f"BIC improved ({old_model_bic} -> {new_model_bic})"
                    message_log = intro + outcome + "\n"
                else:
                    old_model_aic = round(old_model_bic, 4)
                    new_model_aic = round(new_model_bic, 4)
                    intro = "Stopping Criterion: "
                    outcome = f"BIC deteriorated ({old_model_bic} -> {new_model_bic})"
                    message_log = intro + outcome + "\n"
            
        # No AIC or BIC selected
        else:
            var_pass = True
            message_log = "Stopping Criterion: AIC or BIC was not used.\n"
        
        return var_pass, message_log
    
    #-------------------------------------------------------------------------#
    # INPUTS VALIDATION
    #-------------------------------------------------------------------------#
    if type(MODEL_TYPE) != str or MODEL_TYPE.lower() not in ['linear', 'logistic']:
        MODEL_TYPE = 'linear'
        warnings.warn("MODEL_TYPE value is inadequate. Value 'linear' was assigned."
                      ,UserWarning)
    
    if type(ENDOG) == list:
        ENDOG = pd.Series(ENDOG)
    elif type(ENDOG) != type(pd.Series()):
        raise ValueError("ENDOG value is not a list or pd.Series.")
        return
    
    if type(EXOG) != type(pd.DataFrame()):
        raise ValueError("EXOG value is not a pd.DataFrame.")
        return
    
    if type(REVERSE_Y) != bool:
        REVERSE_Y = False
        warnings.warn("REVERSE_Y value is inadequate. Value False was assigned."
                      ,UserWarning)
        
    if CLASS_TREATMENT.lower() not in ['drop', 'sas', 'dummy', 'dummpy_dropfirst']:
        CLASS_TREATMENT = 'sas'
        warnings.warn("CLASS_TREATMENT value is inadequate. Value 'sas' was assigned."
                      ,UserWarning)
    
    if type(SCRITERIA) != str:
        raise ValueError("SCRITERIA value is not a string.")
        return
    elif SCRITERIA.lower() not in ['z', 'aic', 'bic']:
        SCRITERIA = 'z'
        warnings.warn("SCRITERIA value is inadequate. Value 'z' was assigned."
                      ,UserWarning)
        
    if type(SLENTRY) != int and type(SLENTRY) != float:
        raise ValueError("SLENTRY value is neither an integer or a float.")
        return
    else:
        SLENTRY = max(0, min(1, SLENTRY))
        
    if type(SLSTAY) != int and type(SLSTAY) != float:
        raise ValueError("SLSTAY value is neither an integer or a float.")
        return
    else:
        SLSTAY = max(0, min(1, SLSTAY))
    
    
    #-------------------------------------------------------------------------#
    # DATA PRE-PROCESSING
    #-------------------------------------------------------------------------#
    
    # Logging - Start
    #-------------------------------------------------------------------------#
    line_sep = "*------------------------------------------------------------*"
    iterations_log = ''
    
    # Reverse (Binary) Target Variable
    #-------------------------------------------------------------------------#
    if REVERSE_Y == True:
        ENDOG = abs(ENDOG - 1)
    
    # Missing Data
    #-------------------------------------------------------------------------#
    EXOG = EXOG.dropna(axis = 0
                       ,how = 'any')
    ENDOG = ENDOG.loc[ENDOG.index.isin(EXOG.index)]
    EXOG.reset_index(drop = True)
    ENDOG.reset_index(drop = True)
    
    # One-Hot Encoding Categorical Variables
    #-------------------------------------------------------------------------#
    iterations_log += f"{line_sep}\n"
    iterations_log += "ONE-HOT ENCODING CATEGORICAL VARIABLES\n"
    iterations_log += f"{line_sep}\n"
    iterations_log += f"Treatment for categorical variables selected: '{CLASS_TREATMENT}'\n"
    dtypes = EXOG.dtypes
    cat_cols = dtypes[(dtypes == object) | (dtypes == 'category')].index \
                                                                  .tolist()
    if CLASS_TREATMENT == 'drop' and len(cat_cols) > 0:
       EXOG = EXOG.drop(columns = dtypes[dtypes == object].index.tolist())
       iterations_log += "Categorical variables (Dropped):" \
                                               ,dtypes[dtypes == object].index \
                                               .tolist(), "\n"
    elif CLASS_TREATMENT == 'sas' and len(cat_cols) > 0:
        for i in cat_cols:
            cat_cols_labels = EXOG[i].dropna().unique().tolist()
            cat_cols_labels.sort(reverse = True)
            EXOG = pd.get_dummies(EXOG
                                  ,columns = [i]
                                  ,prefix_sep = ':'
                                  ,drop_first = False
                                  ,dummy_na = False)
            EXOG.drop(columns = [i + ':' + cat_cols_labels[0]]
                      ,inplace = True)
            iterations_log += f"Reference category for {i}: {i + ':' + cat_cols_labels[0]}\n"
            
    elif CLASS_TREATMENT == 'dummy' and len(cat_cols) > 0:
        EXOG = pd.get_dummies(EXOG
                              ,drop_first = False
                              ,dummy_na = False)
        iterations_log += "Character Variables (Dummies Generated):" \
                                                ,dtypes[dtypes == object].index \
                                                .tolist(), "\n"
    elif CLASS_TREATMENT == 'dummy_dropfirst' and len(cat_cols) > 0:
        EXOG = pd.get_dummies(EXOG
                              ,drop_first = True
                              ,dummy_na = False)
        iterations_log += "Categorical variables (Dummies Generated, First Dummies Dropped):" \
                                                ,dtypes[dtypes == object].index \
                                                .tolist(), "\n" 
    
    else:
        iterations_log += "No categorical variables were identified. One-hot encoding was not performed.\n"
    
    #-------------------------------------------------------------------------#
    # REGRESSION
    #-------------------------------------------------------------------------#
    
    # Intercept Parameter
    #-------------------------------------------------------------------------#
    EXOG = sm.add_constant(EXOG)
    EXOG.rename(columns = {'const' : 'INTERCEPT'}, inplace = True)
    cols = EXOG.columns.tolist()
    
    # List of Independent Variables
    #-------------------------------------------------------------------------#
    other_cols = cols.copy()
    other_cols.remove('INTERCEPT')
    selected_cols = ['INTERCEPT']
    
    # Stopping Criteria
    #-------------------------------------------------------------------------#
    # Hypothesis Testing
    chi2_result = False
    if MODEL_TYPE.lower() == 'logistic':
        chi2_result = True
    
    # Process
    #-------------------------------------------------------------------------#
    
    # Log
    iterations_log += f"\n{line_sep}\n"
    iterations_log += "STEPWISE REGRESSION\n"
    iterations_log += f"{line_sep}\n"
    
    # Stepwise Process
    for i in range(EXOG.shape[1]): # Maximum number of loops = nr. dep. vars.
    
        # Log - Iteration Number
        iterations_log += f"ITERATION {str(i + 1).zfill(2)}:\n"
        
        # Forward Selection Process
        #---------------------------------------------------------------------#
        if len(cat_cols) > 0:
            cat_df = pd.DataFrame(data = 0
                                  ,index = ['CHECKED','P-VALUE']
                                  ,columns = cat_cols
                                  ,dtype = 'float64')
        pvals = pd.DataFrame(columns = ['Cols','Pval'])
        
        for j in other_cols:
            
            # Is the selected variable categorical?
            selected_var_cat = False
            for m in cat_cols:
                if j.startswith(m) == True:
                    selected_var_cat = m
                    break
            
            # P-value of selected variable (non-categorical)
            if selected_var_cat == False:
                model = regressor(ENDOG, EXOG[selected_cols + [j]] * 1)
                if chi2_result == True:
                    p_value = chi2.sf(model.tvalues[j] ** 2, 1)
                else:
                    p_value = model.pvalues[j]
            
            # P-value of selected variable (categorical)
            else:
                
                # First time assessing categorical variable
                if cat_df.iloc[0][selected_var_cat] == 0:
                    
                    # Define that categorical variable was assessed
                    cat_df.loc['CHECKED', selected_var_cat] = 1
                    
                    # Group all categories of the variable
                    cat_selected_cols = []
                    for n in other_cols:
                        if n.startswith(selected_var_cat):
                            cat_selected_cols.append(n)
                            
                    # Are there more than 2 categories?
                    if len(cat_selected_cols) > 1:
                        
                        # Log-likelihood of model without categories
                        short_model = regressor(ENDOG, EXOG[selected_cols])
                        short_llf = short_model.llf
                        ind_vars = []
                        ind_vars.extend(selected_cols)
                        ind_vars.extend(cat_selected_cols)
                        
                        # Log-likelihood of model with categories
                        model = regressor(ENDOG, EXOG[ind_vars] * 1)
                        full_llf = model.llf
                        
                        # Likelihood Ratio (LR) test
                        LR_statistic = (-2) * (short_llf - full_llf)
                        p_value = chi2.sf(LR_statistic, len(cat_selected_cols))
                        cat_df.loc['P-VALUE', selected_var_cat] = p_value
                    
                    # Are there only 2 categories?
                    else:
                        model = regressor(ENDOG, EXOG[selected_cols + [j]] * 1)
                        if chi2_result == True:
                            p_value = chi2.sf(model.tvalues[j] ** 2, 1)
                        else:
                            p_value = model.pvalues[j]
                        cat_df.loc['P-VALUE', selected_var_cat] = p_value
                    
                # Categorical variable was already assessed
                else:
                    p_value = cat_df.iloc[1][selected_var_cat]

            # Store the p-value
            store_results_pvals(df = pvals
                                ,col_name = 'Cols'
                                ,col_var = 'Pval'
                                ,var_name = j
                                ,var_value = p_value)
        
        # Sort p-values and filter p-values greater than SLENTRY
        pvals = pvals.sort_values(by = ['Pval']).reset_index(drop = True)
        pvals = pvals[pvals.Pval <= SLENTRY]
        
        # All p-values are greater than SLENTRY?
        if pvals.shape[0] == 0:
            iterations_log += "Forward Selection: No variable to add.\n"
            break
        
        # Are there variables with p-value smaller or equal to SLENTRY?
        else:
            new_var = pvals['Cols'][0]
            new_var_label = new_var
            new_var_pvalue = pvals[pvals['Cols'] == new_var]['Pval'].iloc[0]
        
            # Is the new variable categorical?
            for m in cat_cols:
                if new_var.startswith(m) == True:
                    new_var = []
                    
                    # Group all variables of the same category
                    for n in other_cols:
                        if n.startswith(m):
                            new_var.append(n)
                    new_var_label = m
        
            # Remove variable from pool of potential variables
            iterations_log += f"Forward Selection: {new_var_label} (p-value: " \
                                    f"{round(new_var_pvalue, 4)}) selected.\n"
            temp_selected_cols = selected_cols.copy()
            if type(new_var) != list:
                temp_selected_cols.append(new_var)
                other_cols.remove(new_var)
            else:
                for k in new_var:
                    temp_selected_cols.append(k)
                    other_cols.remove(k)
        
            # (Additional) Stopping Criterion
            sc_check, message_log = stopping_criterion_check(ENDOG = ENDOG
                                                             ,EXOG = EXOG
                                                             ,SCRITERIA = SCRITERIA
                                                             ,old_vars = selected_cols
                                                             ,new_vars = temp_selected_cols)
            
            if sc_check == True:
                selected_cols = temp_selected_cols.copy()
                iterations_log += message_log
                iterations_log += f"Forward Selection: {new_var_label} added.\n"
            else:
                iterations_log += message_log
                iterations_log += f"Forward Selection: {new_var_label} not added.\n"
            model = regressor(ENDOG, EXOG[selected_cols] * 1)

            # Backward Elimination Process
            #-----------------------------------------------------------------#
            if len(cat_cols) > 0:
                cat_df = pd.DataFrame(data = 0
                                      ,index = ['CHECKED','P-VALUE']
                                      ,columns = cat_cols
                                      ,dtype = 'float64')
            cols_backward = EXOG[list(model.params.index[1:])].columns.tolist()
            pvals_backward = pd.DataFrame(columns = ['bw_Cols', 'bw_Pval'])
            
            for k in cols_backward: # Number dependent variables
            
                # Is the selected variable categorical?
                selected_var_cat = False
                for m in cat_cols:
                    if k.startswith(m) == True:
                        selected_var_cat = m
                        break
                    
                # P-value of selected variable (non-categorical)
                if selected_var_cat == False:
                    if chi2_result == True:
                        p_value = chi2.sf(model.tvalues[k] ** 2, 1)
                    else:
                        p_value = model.pvalues[k]
                        
                # P-value of selected variable (categorical)
                else:
                    
                    # First time assessing categorical variable
                    if cat_df.iloc[0][selected_var_cat] == 0:
                        
                        # Define that categorical variable was assessed
                        cat_df.loc['CHECKED', selected_var_cat] = 1
                        
                        # Group all categories of the variable
                        cat_selected_cols = []
                        for n in cols_backward:
                            if n.startswith(selected_var_cat):
                                cat_selected_cols.append(n)
                                
                        # Are there more than 2 categories?
                        if len(cat_selected_cols) > 1:
                            
                            # Log-likelihood of model without categories
                            short_model_vars = [x for x in list(model.params.index) \
                                                if x not in cat_selected_cols]
                            short_model = regressor(ENDOG, EXOG[short_model_vars])
                            short_llf = short_model.llf
                            
                            # Log-likelihood of model with categories
                            full_llf = model.llf
                            
                            # Likelihood Ratio (LR) test
                            LR_statistic = (-2) * (short_llf - full_llf)
                            p_value = chi2.sf(LR_statistic, len(cat_selected_cols))
                            cat_df.loc['P-VALUE', selected_var_cat] = p_value
                        
                        # Are there only 2 categories?
                        else:
                            if chi2_result == True:
                                p_value = chi2.sf(model.tvalues[k] ** 2, 1)
                            else:
                                p_value = model.pvalues[k]
                            cat_df.loc['P-VALUE', selected_var_cat] = p_value
                        
                    # Categorical variable was already assessed
                    else:
                        p_value = cat_df.iloc[1][selected_var_cat]
    
                # Store the p-value
                store_results_pvals(df = pvals_backward
                                    ,col_name = 'bw_Cols'
                                    ,col_var = 'bw_Pval'
                                    ,var_name = k
                                    ,var_value = p_value)
                    
            # Sort p-values and filter p-values lower than SLSTAY
            pvals_backward = pvals_backward.sort_values(by = ['bw_Pval']
                                                        ,ascending = False) \
                                                .reset_index(drop = True)
            pvals_backward_drop = pvals_backward[pvals_backward.bw_Pval \
                                                 >= SLSTAY].reset_index(drop = True)
                
            # All p-values are lower than SLSTAY?
            if pvals_backward_drop.shape[0] == 0:
                iterations_log += "Backward Elimination: No variable to remove.\n\n"
            
            # Are there variables with p-value greater or equal to SLSTAY?
            else:
                
                # Is the least significant selected variable categorical?
                var_drop = pvals_backward_drop['bw_Cols'][0]
                var_drop_pvalue = pvals_backward_drop['bw_Pval'][0]
                var_drop_label = var_drop
                selected_var_cat = False
                for m in cat_cols:
                    if var_drop.startswith(m) == True:
                        selected_var_cat = m
                        var_drop_label = selected_var_cat
                        break
                
                # Define list of variables to investigate
                iterations_log += f"Backward Elimination: {var_drop_label} (p-value: " \
                                        f"{round(var_drop_pvalue, 4)}) selected.\n"
                temp_selected_cols = selected_cols.copy()
                if selected_var_cat == False:
                    temp_selected_cols.remove(var_drop)
                else:
                    for l in selected_cols:
                        if l.startswith(selected_var_cat):
                            temp_selected_cols.remove(l)
            
                # (Additional) Stopping Criterion
                sc_check, message_log = stopping_criterion_check(ENDOG = ENDOG
                                                                 ,EXOG = EXOG
                                                                 ,SCRITERIA = SCRITERIA
                                                                 ,old_vars = selected_cols
                                                                 ,new_vars = temp_selected_cols)
                
                if sc_check == True and SCRITERIA.lower() not in ['aic', 'bic']:
                    selected_cols = temp_selected_cols.copy()
                    iterations_log += message_log
                    iterations_log += f"Backward Elimination: {var_drop_label} removed.\n\n"
                else:
                    iterations_log += message_log
                    iterations_log += f"Backward Elimination: {var_drop_label} not removed.\n\n"
                model = regressor(ENDOG, EXOG[selected_cols] * 1)
                
        # Log - Iteration results
        iterations_log += f"{str(model.summary())}\n"
        iterations_log += f"AIC: {str(round(model.aic, 4))}\n"
        iterations_log += f"BIC: {str(round(model.bic_llf, 4))}\n\n"                

    # Logging - End
    #-------------------------------------------------------------------------#
    iterations_log += f"\n{line_sep}\n"
    iterations_log += "OVERVIEW\n"
    iterations_log += f"{line_sep}"
    
    for m in range(len(selected_cols[1:])):
        iterations_log += f"\n{str(m+1).zfill(2)}. Final Variable: {selected_cols[1:][m]}"
    
    first_element = selected_cols[0]
    sorted_rest = sorted(selected_cols[1:])
    sorted_selected_cols = [first_element] + sorted_rest
    model = regressor(ENDOG, EXOG[sorted_selected_cols] * 1)
    iterations_log += "\n\n" + str(model.summary()) + "\nAIC: "+ str(model.aic) \
        + "\nBIC: "+ str(model.bic_llf)+"\n\n"        
    print(model.summary())
    print("AIC: " + str(round(model.aic, 4)))
    print("BIC: " + str(round(model.bic_llf, 4)))
    print("Final Variables:", selected_cols)
    
    # Final Results
    #-------------------------------------------------------------------------#
    return model, selected_cols, iterations_log
                    
# Summary of fit
#*****************************************************************************#
glm_model, selected_vars, log = StepwiseGLM(MODEL_TYPE = 'logistic'
                                            ,ENDOG = y
                                            ,EXOG = X
                                            ,REVERSE_Y = True
                                            ,CLASS_TREATMENT = 'sas'
                                            ,SCRITERIA = 'z'
                                            ,SLENTRY = 0.05
                                            ,SLSTAY = 0.01)