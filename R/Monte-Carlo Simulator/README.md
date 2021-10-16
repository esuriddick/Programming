# What is Monte-Carlo simulation?
As presented in Investopedia (<a href="https://www.investopedia.com/terms/m/montecarlosimulation.asp">HERE</a>):

"Monte Carlo simulations are used to model the probability of different outcomes in a process that cannot easily be predicted due to the intervention of random variables. It is a technique used to understand the impact of risk and uncertainty in prediction and forecasting models.

A Monte Carlo simulation can be used to tackle a range of problems in virtually every field such as finance, engineering, supply chain, and science. It is also referred to as a multiple probability simulation."

# Who is the original creator?
<code>Dropbox Inc.</code> created and made available the underlying code as a low-budget password strength estimator. If you are curious on how it was developed, the underlying
paper and presentation were made available at the 25th USENIX Security Symposium (available 
<a href="https://www.usenix.org/conference/usenixsecurity16/technical-sessions/presentation/wheeler">HERE</a>).

# Purpose of this program
Password managers, which usually have incorporated a password generator, are getting increasingly popular. However, if you would like additional services, such as assessing the strength of your current passwords, you are requested to pay extra. This program allows you to import into R your passwords (e.g., through <code>.csv</code>) and then the functions available identify any weak password that you might have stored (examples of how to run the functions are provided in the program).

In addition, in case you have thought of a password of your own, you can use these functions to determine whether it is deemed as safe or not.

# Dependencies
<code>V8</code>: Google's open source JavaScript and WebAssembly engine for R. The information on this package can be found in: https://cran.r-project.org/web/packages/V8/index.html

# Functions
<code>password_score</code>: evaluates a given password and classifies it from "Very Weak" to "Very Strong".

<code>password_suggestion</code>: attempts to provide a comment in how to improve the password.

<code>detect_duplicates</code>: identifies duplicated.

<code>detect_empty</code>: identifies empty passwords.

<code>HTTP_Protocol</code>: identifies whether the website associated with the password uses the "HTTP" or "HTTPS" protocols.

# Additional information
Want to check if any of your e-mails have been compromised? Check out this page: https://haveibeenpwned.com/

Want to check if any of your passwords have been compromised? Check out this page: https://haveibeenpwned.com/Passwords
