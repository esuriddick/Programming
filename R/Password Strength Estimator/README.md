# What is zxcvbn?
As presented in the original repository (<a href="https://github.com/dropbox/zxcvbn">HERE</a>):

"<code>zxcvbn</code> is a password strength estimator inspired by password crackers. Through pattern matching and conservative estimation, it recognizes and weighs 30k common passwords, common names and surnames according to US census data, popular English words from Wikipedia and US television and movies, and other common patterns like dates, repeats (<code>aaa</code>), sequences (<code>abcd</code>), keyboard patterns (<code>qwertyuiop</code>), and l33t speak."

# Who is the original creator?
<code>Dropbox Inc.</code> created and made available the underlying code as a low-budget password strength estimator. If you are curious on how it was developed, the underlying
paper and presentation were made available at the 25th USENIX Security Symposium (available 
<a href="https://www.usenix.org/conference/usenixsecurity16/technical-sessions/presentation/wheeler">HERE</a>).

# Purpose of this program
Password managers, which usually have incorporated a password generator, are getting increasingly popular. However, if you would like additional services, such as assessing the strength of your current passwords, you are requested to pay extra. This program allows you to export your passwords and through the functions available identify any weak password that you might have stored.

In addition, in case you have thought of a password of your own, you can use these functions to determine whether it is deemed as safe or not.

# Dependencies
<code>V8</code>: Google's open source JavaScript Engine for R.

# Functions
<code>password_score</code>: evaluates a given password and classifies it from "Very Weak" to "Very Strong".
