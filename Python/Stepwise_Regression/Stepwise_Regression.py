# Modules
#*****************************************************************************#
import pandas as pd
import statsmodels.api as sm
from scipy.stats import chi2

# Load Data
#*****************************************************************************#
df = pd.read_csv(r"C:\Users\...\example.csv")

# Define the independent and dependent variables
#*****************************************************************************#
y = df['BAD'].copy()
x_columns = list(df.loc[0, (df.columns != 'BAD')].columns
                 .values)
X = df[x_columns].copy()

# Stepwise regression
#*****************************************************************************#
def StepwiseGLM(model_type = 'logistic' #'logistic' or 'linear'
                ,endog = y
                ,reverse_y = False
                ,exog = X
                ,CLASS_TREATMENT = 'sas' #'drop', 'sas','dummy' or 'dummy_dropfirst'
                ,SCRITERIA = 'z' #'z', 'aic' or 'bic'
                ,SLENTRY = 0.05
                ,SLSTAY = 0.05):
    
    # Functions
    def regressor(y, X, model_type = model_type):
        if model_type.lower() == 'logistic':
            family = sm.families.Binomial(link = sm.families.links.Logit())
        elif model_type.lower() == 'linear':
            family = sm.families.Gaussian(link = sm.families.links.Identity())
        else:
            family = sm.families.Gaussian(link = sm.families.links.Identity())
        regressor = sm.GLM(endog = y
                           ,exog = X
                           ,missing = 'drop'
                           ,family = family).fit(method = 'IRLS'
                                                 ,tol = 1e-08
                                                 ,maxiter = 100
                                                 ,use_t = False
                                                 ,warn_convergence = True)
        return regressor
        
    def store_results_pvals(df
                            ,col_name
                            ,col_var
                            ,var_name
                            ,var_value):
        new_row = {col_name: var_name
                   ,col_var: var_value}
        df.loc[len(df.index)] = new_row
        return
    
    # Missing rows treatment
    exog = exog.dropna(axis = 0
                       ,how = 'any')
    endog = endog.loc[endog.index.isin(exog.index)]
    exog.reset_index(drop = True)
    endog.reset_index(drop = True)
    
    # Reverse Y
    if reverse_y == True:
        endog = abs(endog - 1)
    
    # One-hot Encoding Categorical Variables
    dtypes = exog.dtypes
    cat_cols = dtypes[(dtypes == object) | (dtypes == 'category')].index \
                                                                  .tolist()
    if CLASS_TREATMENT == 'drop':
       exog = exog.drop(columns = dtypes[dtypes == object].index.tolist())
       print("Character Variables (Dropped):", dtypes[dtypes == object].index \
                                                                     .tolist())
    elif CLASS_TREATMENT == 'sas':
        for i in cat_cols:
            cat_cols_labels = exog[i].dropna().unique().tolist()
            cat_cols_labels.sort(reverse = True)
            exog = pd.get_dummies(exog
                                  ,columns = [i]
                                  ,prefix_sep = '_'
                                  ,drop_first = False
                                  ,dummy_na = False)
            exog.drop(columns = [i + '_' + cat_cols_labels[0]]
                      ,inplace = True)
            
    elif CLASS_TREATMENT == 'dummy':
        exog = pd.get_dummies(exog
                              ,drop_first = False
                              ,dummy_na = False)
        print("Character Variables (Dummies Generated):"
              ,dtypes[dtypes == object].index.tolist())
    elif CLASS_TREATMENT == 'dummy_dropfirst':
        exog = pd.get_dummies(exog
                              ,drop_first = True
                              ,dummy_na = False)
        print("Character Variables (Dummies Generated, First Dummies Dropped):"
              ,dtypes[dtypes == object].index.tolist())
    else:
        exog = pd.get_dummies(exog
                              ,drop_first = True
                              ,dummy_na = False)
        print("Character Variables (Dummies Generated, First Dummies Dropped):"
              ,dtypes[dtypes == object].index.tolist())

    # Constant Parameter
    exog = sm.add_constant(exog)
    exog.rename(columns = {'const' : 'INTERCEPT'}, inplace = True)
    cols = exog.columns.tolist()
    
    # Regression Setup
    iterations_log = ''
    chi2_result = False
    if model_type.lower() == 'logistic':
        iterations_log += "Selected Model Type: " + model_type.upper()
        chi2_result = True
    elif model_type.lower() == 'linear':
        iterations_log += "Selected Model Type: " + model_type.upper()
    else:
        iterations_log += "Unknown Model Type: " + model_type.upper() + \
                          "\nReverting to linear model type."
                                                    
    # Bi-directional Stepwise Regression
    selected_cols = ['INTERCEPT']
    other_cols = cols.copy()
    other_cols.remove('INTERCEPT')
    
    # AIC or BIC Setup
    if SCRITERIA.lower() == 'aic' or SCRITERIA.lower() == 'bic':
        model = regressor(endog, exog[selected_cols])
        if SCRITERIA.lower() == 'aic':
            criteria = model.aic
        else:
            criteria = model.bic_llf
            
    # Elimination Loop - Maximum number of iterations
    for i in range(exog.shape[1]):
        cat_df = pd.DataFrame(data = 0
                              ,index = ['CHECKED','P-VALUE']
                              ,columns = cat_cols
                              ,dtype = 'float64')
        pvals = pd.DataFrame(columns = ['Cols','Pval'])
        
        ## Loop - Store p-values
        for j in other_cols:
            model = regressor(endog, exog[selected_cols + [j]] * 1)
            if chi2_result == True:
                p_value = chi2.sf(model.tvalues[j] ** 2, 1)
            else:
                p_value = model.pvalues[j]
            for m in cat_cols:
                if j.startswith(m) == True:
                    if cat_df.iloc[0][m] == 0:
                        cat_df.loc['CHECKED', m] = 1
                        cat_selected_cols = []
                        for n in other_cols:
                            if n.startswith(m):
                                cat_selected_cols.append(n)
                        if len(cat_selected_cols) > 1:
                            short_model = regressor(endog, exog[selected_cols])
                            short_llf = short_model.llf
                            ind_vars = []
                            ind_vars.extend(selected_cols)
                            ind_vars.extend(cat_selected_cols)
                            model = regressor(endog, exog[ind_vars] * 1)
                            full_llf = model.llf
                            LR_statistic = (-2) * (short_llf - full_llf)
                            p_value = chi2.sf(LR_statistic, len(cat_selected_cols))
                            cat_df.loc['P-VALUE', m] = p_value
                    else:
                        p_value = cat_df.iloc[1][m]
                    break
                    
            store_results_pvals(df = pvals
                                ,col_name = 'Cols'
                                ,col_var = 'Pval'
                                ,var_name = j
                                ,var_value = p_value)
                
        ## Select the most significant variable
        pvals = pvals.sort_values(by = ['Pval']).reset_index(drop = True)
        pvals = pvals[pvals.Pval <= SLENTRY]
        if pvals.shape[0] > 0:
            new_var = pvals['Cols'][0]
            new_var_label = pvals['Cols'][0]
            new_var_cat = 0
            for m in cat_cols:
                if new_var.startswith(m) == True:
                    new_var_cat = 1
                    new_var = []
                    for n in other_cols:
                        if n.startswith(m):
                            new_var.append(n)
                    model = regressor(endog, exog[selected_cols + new_var] * 1)
                    new_var_label = m
            if new_var_cat == 0:
                model = regressor(endog, exog[selected_cols + [new_var]] * 1)
            iterations_log += "\n" + str(i + 1) + ". iteration"
            iterations_log += str("\nEntered: " + new_var_label + "\n")    
            iterations_log += "\n\n"+str(model.summary())+"\nAIC: "+ str(model.aic) \
                + "\nBIC: "+ str(model.bic_llf)+"\n\n"

            ### Elimination Loop - General Control
            for k in range(exog[selected_cols + [pvals['Cols'][0]]].shape[1]):
                cat_df = pd.DataFrame(data = 0
                                      ,index = ['CHECKED','P-VALUE']
                                      ,columns = cat_cols
                                      ,dtype = 'float64')
                cols_backward = exog[selected_cols + [pvals['Cols'][0]]].columns.tolist()
                pvals_backward = pd.DataFrame(columns = ['bw_Cols', 'bw_Pval'])
                
                #### Loop - Store p-values
                for l in cols_backward:
                    if chi2_result == True:
                        p_value = chi2.sf(model.tvalues[l] ** 2, 1)
                    else:
                        p_value = model.pvalues[l]
                    for m in cat_cols:
                        if l.startswith(m) == True:
                            if cat_df.iloc[0][m] == 0:
                                cat_df.loc['CHECKED', m] = 1
                                cat_selected_cols = []
                                for n in other_cols:
                                    if n.startswith(m):
                                        cat_selected_cols.append(n)
                                for n in selected_cols:
                                    if n.startswith(m):
                                        cat_selected_cols.append(n)
                                if len(cat_selected_cols) > 1:
                                    if new_var != cat_selected_cols:
                                        short_list_vars = [o for o in  \
                                    selected_cols if o not in cat_selected_cols]
                                        if (type(new_var) is list) == True:
                                            short_list_vars.extend(cat_selected_cols)
                                        else:
                                            short_list_vars.append(str(new_var))
                                    elif new_var == cat_selected_cols:
                                        short_list_vars = [o for o in \
                                    selected_cols if o not in cat_selected_cols]
                                    full_list_vars = short_list_vars.copy()
                                    full_list_vars.extend(cat_selected_cols)
                                    short_model = regressor(endog, exog[short_list_vars] * 1)
                                    short_llf = short_model.llf
                                    model = regressor(endog, exog[full_list_vars] * 1)
                                    full_llf = model.llf
                                    LR_statistic = (-2) * (short_llf - full_llf)
                                    p_value = chi2.sf(LR_statistic, len(cat_selected_cols))
                                    cat_df.loc['P-VALUE', m] = p_value
                            else:
                                p_value = cat_df.iloc[1][m]
                            break
                    
                    store_results_pvals(df = pvals_backward
                                        ,col_name = 'bw_Cols'
                                        ,col_var = 'bw_Pval'
                                        ,var_name = l
                                        ,var_value = p_value)
                    
                #### Drop insignificant variables
                pvals_backward = pvals_backward.sort_values(by = ['bw_Pval']) \
                                                    .reset_index(drop = True)
                pvals_backward_drop = pvals_backward[pvals_backward.bw_Pval \
                                                     > SLSTAY].reset_index(drop = True)
                    
                if pvals_backward_drop.shape[0] > 0:
                    cat_drop_df = pd.DataFrame(data = 0
                                              ,index = ['CHECKED']
                                              ,columns = cat_cols)
                    cat_drop_var = 0
                    for m in cat_cols:
                        if pvals_backward_drop['bw_Cols'][0].startswith(m) == True:
                            cat_drop_var = 1
                            if cat_drop_df.iloc[0][m] == 0:
                                cat_drop_df.loc['CHECKED', m] = 1
                                cat_drop_cols = []
                                for n in selected_cols:
                                    if n.startswith(m):
                                        cat_drop_cols.append(n)
                                for n in other_cols:
                                    if n.startswith(m):
                                        cat_drop_cols.append(n)
                                for o in cat_drop_cols:
                                    if o in other_cols:
                                        other_cols.remove(o)
                                    if o in selected_cols:
                                        selected_cols.remove(o)
                                iterations_log += str("\nBackward Step Dropped: " \
                                                      + m + "\n")
                            else:
                                pass
                    if cat_drop_var == 0:
                        iterations_log += str("\nBackward Step Dropped: " + \
                                  pvals_backward_drop['bw_Cols'][0] + "\n")
                        if pvals_backward_drop['bw_Cols'][0] in other_cols:
                            other_cols.remove(pvals_backward_drop['bw_Cols'][0])                            
                        if pvals_backward_drop['bw_Cols'][0] in selected_cols:
                            selected_cols.remove(pvals_backward_drop['bw_Cols'][0])    

                    if (type(new_var) is list) == True:
                        model = regressor(endog, exog[selected_cols + new_var] * 1)
                    else:
                        model = regressor(endog, exog[selected_cols + [new_var]] * 1)
                    iterations_log += "\n\n"+str(model.summary())+"\nAIC: "+ \
                        str(model.aic) + "\nBIC: "+ str(model.bic_llf)+"\n\n"     
                else:
                    print("Break: No need to perform backward elimination.")
                    break
                
            if SCRITERIA.lower() == 'aic':
                new_criteria = model.aic
                if new_criteria < criteria:
                    print("Entered:"
                          ,pvals['Cols'][0]
                          ,"\tAIC:"
                          ,model.aic)
                    if (type(new_var) is list) == True:
                        for n in new_var:
                            if n not in selected_cols:
                                selected_cols.append(n)
                            if n in other_cols:
                                other_cols.remove(n)
                    else:
                        if new_var not in selected_cols:
                            selected_cols.append(str(new_var))
                        if new_var in other_cols:
                            other_cols.remove(str(new_var))
                    criteria = new_criteria
                else:
                    print("Break: AIC does not improve.")
                    break
            elif SCRITERIA.lower() == 'bic':
                new_criteria = model.bic_llf
                if new_criteria < criteria:
                    print("Entered:"
                          ,pvals['Cols'][0]
                          ,"\tBIC:"
                          ,model.bic_llf)
                    if (type(new_var) is list) == True:
                        for n in new_var:
                            if n not in selected_cols:
                                selected_cols.append(n)
                            if n in other_cols:
                                other_cols.remove(n)
                    else:
                        if new_var not in selected_cols:
                            selected_cols.append(str(new_var))
                        if new_var in other_cols:
                            other_cols.remove(str(new_var))
                    criteria = new_criteria
                else:
                    print("Break: BIC does not improve.")
                    break  
            else:
                print("Entered:"
                      ,new_var_label
                      ,"\tP-value:"
                      ,pvals['Pval'][0])
                if (type(new_var) is list) == True:
                    for n in new_var:
                        if n not in selected_cols:
                            selected_cols.append(n)
                        if n in other_cols:
                            other_cols.remove(n)
                else:
                    if new_var not in selected_cols:
                        selected_cols.append(str(new_var))
                    if new_var in other_cols:
                        other_cols.remove(str(new_var))
                
        else:
            print(f"Break: No p-value is below {SLENTRY}.")
            break
        
    model = regressor(endog, exog[selected_cols] * 1)
    if SCRITERIA.lower() == "aic":
        criteria = model.aic
    elif SCRITERIA.lower() == "bic":
        criteria = model.bic_llf
    
    print(model.summary())
    print("AIC: " + str(model.aic))
    print("BIC: " + str(model.bic_llf))
    print("Final Variables:", selected_cols)
    

    iterations_log += "\nFinal Selection and Model Statistics\n"
    
    for m in range(len(selected_cols)):
        iterations_log += "\n" + str(m+1) + str(". Final Variable :  "+ selected_cols[m]) 
           
    iterations_log += "\n\n" + str(model.summary()) + "\nAIC: "+ str(model.aic) \
        + "\nBIC: "+ str(model.bic_llf)+"\n\n"

    return model, selected_cols, iterations_log
                    
# Summary of fit
#*****************************************************************************#
glm_model, selected_vars, log = StepwiseGLM(model_type = 'logistic'
                                            ,endog = y
                                            ,reverse_y = True
                                            ,exog = X
                                            ,CLASS_TREATMENT = 'sas'
                                            ,SCRITERIA = 'z'
                                            ,SLENTRY = 0.05
                                            ,SLSTAY = 0.01)
