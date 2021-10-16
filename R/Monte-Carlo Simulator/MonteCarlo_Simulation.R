#/***********************************************************************************************/#
#/ MONTE-CARLO SIMULATOR 
#/***********************************************************************************************/#

#/ FUNCTIONS
#/***********************************************************************************************/#
generate.path <- function(initial_value, average = 0, std = 1, timesteps, cumulative = "PRODUCT"){
  #Errors
  if(initial_value == "" || !is.numeric(initial_value)){
    stop("Starting point is not valid.")
  }
  if(timesteps == "" || !is.numeric(timesteps)){
    stop("Timesteps is not valid.")
  }
  if(!is.numeric(average)){
    stop("Average indicated is not valid.")
  }
  if(!is.numeric(std) || std <= 0){
    stop("Standard deviation indicated is not valid.")
  }
  if(!(cumulative %in% c("PRODUCT", "SUM"))){
    stop("Unknown cumulative process selected.")
  }
  
  #Simulation (https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Distributions.html)
  changes <- rnorm(n = timesteps, mean = average, sd = std)
  if(cumulative == "PRODUCT"){
    sample.path <- cumprod(c(initial_value, changes))
  }else if(cumulative == "SUM"){
    sample.path <- cumsum(c(initial_value, changes))
  }
  final_value <- sample.path[timesteps + 1]
  
  #Result
  return(final_value)
}

generate.values <- function(average = 0, std = 1, timesteps){
  #Errors
  if(!is.numeric(average)){
    stop("Average indicated is not valid.")
  }
  if(!is.numeric(std) || std <= 0){
    stop("Standard deviation indicated is not valid.")
  }
  if(timesteps == "" || !is.numeric(timesteps)){
    stop("Timesteps is not valid.")
  }
  
  #Simulation (https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Distributions.html)
  final_values <- rnorm(n = timesteps, mean = average, sd = std)
  
  #Result
  return(final_values)
}

#/ ASSET VALUATION (NORMAL DISTRIBUTION)
#/***********************************************************************************************/#
#Options
runs <- 100               #Number of simulations
initial_value <- 50       #Starting point
ObservedMean <- 1.001     #Mean for the Normal Distribution
ObservedSTD <- 0.005      #Standard deviation for the Normal Distribution
timesteps <- 20           #Number of results per simulation

#Results
set.seed(101)
simulations <- replicate(runs,
                         generate.path(initial_value,
                                       average = ObservedMean,
                                       std = ObservedSTD,
                                       timesteps))
PathsResult <- data.frame("SIMULATION" = seq(1, runs),
                          "FINAL_VALUE" = simulations)

#/ AREA UNDER THE CURVE OF A NORMAL DISTRIBUTION (INTEGRATION)
#/***********************************************************************************************/#
#Options
ObservedMean <- 1         #Mean for the Normal Distribution
ObservedSTD <- 3          #Standard deviation for the Normal Distribution
timesteps <- 10000000     #Number of results in the simulation

#Results
set.seed(101)
simulations <- generate.values(average = ObservedMean,
                               std = ObservedSTD,
                               timesteps)
AUC <- round(sum(simulations>=3 & simulations<=6) / timesteps, 6) #Value: 0.204698
#Real AUC of a normal distribution with mean 1 and std 3 between 3 and 6 is roughly 0.204792

#/ METRICS
#/***********************************************************************************************/#
#Statistics
Mean <- mean(simulations)
Median <- median(simulations)
Quantile_05 <- quantile(simulations, 0.05)
Quantile_95 <- quantile(simulations, 0.95)

#Visualizations
hist(simulations,
     main = "Histogram",
     xlab = "Simulations",
     ylab = "Frequency")
