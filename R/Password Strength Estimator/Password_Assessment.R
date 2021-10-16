#/***********************************************************************************************/#
#/ ZXCVBN: REALISTIC PASSWORD STRENGTH ESTIMATION
#/***********************************************************************************************/#

#/ FUNCTIONS
#/***********************************************************************************************/#
#INSTALL PACKAGE(S)
list.of.packages <- c("V8")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages) > 0){
  install.packages(new.packages, dependencies = TRUE)
}
if(length(new.packages)) install.packages(new.packages)

#LOADING PACKAGE(S)
library("V8")

#INITIATE JAVA ENGINE
ct <- v8(global = "window")
JavaLibrary <- file.choose()
ct$source(JavaLibrary)
#ORIGINAL JAVA LIBRARY: https://github.com/dropbox/zxcvbn/blob/master/dist/zxcvbn.js

#PASSWORD EVALUATION
#EXAMPLE: df$SCORE <- sapply(df$password, password_score)
password_score <- function(password){
  res <- ct$call("zxcvbn", password)
  if(res$score == 0){
    return("Very Weak")
  }else if(res$score == 1){
    return("Weak")
  }else if(res$score == 2){
    return("Moderate")
  }else if(res$score == 3){
    return("Strong")
  }else{
    return("Very Strong")
  }
}

#PASSWORD FEEDBACK
#EXAMPLE: df$FEEDBACK <- sapply(df$password, password_suggestion)
password_suggestion <- function(password){
  res <- ct$call("zxcvbn", password)
  return(res$feedback[[2]][1])
}

#REUSED PASSWORDS
#EXAMPLE: df$DUPLICATE <- sapply(df$password, detect_duplicates, PasswordColumn = df$password)
detect_duplicates <- function(password, PasswordColumn){
  if(sum(PasswordColumn == password) > 1){
    return(1)
  }else{
    return(0)
  }
}

#EMPTY PASSWORDS
#EXAMPLE: df$FEEDBACK <- sapply(df$password, detect_empty)
detect_empty <- function(password){
  if(password == "" || is.na(password)){
    return(1)
  }else{
    return(0)
  }
}

#UNSECURED WEBSITES
#EXAMPLE: df$HTTP <- sapply(df$hyperlink, detect_empty)
HTTP_Protocol <- function(hyperlink){
  if(grepl("http:", hyperlink) > 0){
    return(1)
  }else{
    return(0)
  }
}