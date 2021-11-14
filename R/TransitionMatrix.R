#/******************************************************************/#
#/ TRANSITION MATRIX - DEFINITION
#/******************************************************************/#
MissingConversion <- function(x){
  if(is.na(x)){
    return('Other') #Another classification may be assigned to NAs
  }else{
    return(x)
  }
}

TransitionMatrix <- function(db, start_var, end_var, convertNA = TRUE){
  #Define Matrix Labels
  db <- db[!is.na(db[[start_var]]), ]
  db[[start_var]] <- as.character(db[[start_var]])
  if(convertNA == TRUE){
    db[[end_var]] <- as.character(sapply(db[[end_var]], MissingConversion))
  }else{
    db[[end_var]] <- as.character(db[[end_var]])
  }
  
  start <- sort(unique(db[[start_var]]))
  end <- sort(unique(db[[end_var]]))
  
  #Create Empty Matrix
  transition.matrix <- matrix(nrow = length(start),
                              ncol = length(end),
                              dimnames = list(start, end))
  
  #Fill Matrix
  for(b in start){  #Rows
    for(c in end){  #Columns
      transition.matrix[b, c] <- sum(db[[start_var]] == b & db[[end_var]] == c)
    }
  }
  return(transition.matrix <<- transition.matrix)
}

#/******************************************************************/#
#/ TRANSITION MATRIX - DEPICTION
#/******************************************************************/#
#Variables indicating the observation's segment/status in each point in time
#(Sorted in an increasing order - from oldest to latest)
segments <- c('segment_Y1',
              'segment_Y2',
              'segment_Y3',
              'segment_Y4',
              'segment_Y5',
              'segment_Y6')

#Run the function for each day/month/year defined above
for(a in 1:(length(segments) - 1)){
  #Create a matrix for each day/month/year
  TransitionMatrix(df, start_var = segments[a], end_var = segments[a+1])
  
  #Export each matrix to a .csv file
  name <- paste('TransitionMatrix', a, sep = '_')
  name <- paste(name, 'csv', sep = '.')
  write.csv(x = transition.matrix,
            file = name)
}