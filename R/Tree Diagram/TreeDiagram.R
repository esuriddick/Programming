#/***********************************************************************************************/#
#/ SETUP
#/***********************************************************************************************/#
#Load library (to install, write in console: install.packages('data.tree', dependencies = TRUE))
library('data.tree')

#Create empty dataframe
data <- data.frame(matrix(ncol = 7, nrow = 0))
colnames(data) <- c('pathString',
                    'prob',
                    'tree_level',
                    'tree_group',
                    'node_type',
                    'overall_prob',
                    'prob_rank')

#/***********************************************************************************************/#
#/ TREE DIAGRAM - FUNCTIONS
#/***********************************************************************************************/#
AddNode <- function(parentnode = NA, 
                   name,
                   prob = NA,
                   tree_level,
                   node_type,
                   overall_prob = FALSE,
                   prob_rank = NA){
  
  #Rules to fill in the dataframe
  if(!is.na(parentnode)){
    name <- paste(parentnode, name, sep = '/')
  }
  if(overall_prob == TRUE){
    if(tree_level <= 1){
      overall_prob <- prob
    }else{
      term_for_search <- paste('^', parentnode, '$', sep = '')
      past_overall_prob <- data[grep(term_for_search, data$pathString), 6]
      overall_prob <- past_overall_prob * prob
    }
  }else{
    if(node_type == 'terminal'){
      term_for_search <- paste('^', parentnode, '$', sep = '')
      past_overall_prob <- data[grep(term_for_search, data$pathString), 6]
      overall_prob <- past_overall_prob
    }else{
      overall_prob <- prob
    }
  }
  
  #Add new row to the dataframe
  new_row <- c(name, prob, tree_level, parentnode, node_type, overall_prob, NA)
  data <<- rbind(data, new_row)
  
  #Ensure proper formatting of the dataframe
  colnames(data) <<- c('pathString',
                      'prob',
                      'tree_level',
                      'tree_group',
                      'node_type',
                      'overall_prob',
                      'prob_rank')
  data$prob <<- as.numeric(data$prob)
  data$tree_level <<- as.numeric(data$tree_level)
  data$overall_prob <<- as.numeric(data$overall_prob)
  data$prob_rank <<- as.numeric(data$prob_rank)
}

MakeTree <- function(df, display_level = NULL, show_rank = FALSE, direction = 'LR'){
  #Direction can be: i) left to right ('LR'); ii) right to left ('RL'); or iii) top to bottom ('TB')
  
  #Clean variable 'overall_prob' from nodes that are not terminal
  df[df$node_type != 'terminal', 6] <- NA
  
  #Calculate the ranks for terminal nodes
  ranked_overall_probs <- sort(unique(df[df$node_type == 'terminal', 6]), decreasing = TRUE)
  determine_rank <- function(x){
    term_for_search <- paste('^', x, '$', sep = '')
    return(grep(term_for_search, ranked_overall_probs))
  }
  df[df$node_type == 'terminal', 7] <- sapply(df[df$node_type == 'terminal', 6], determine_rank)
  
  #Transfer the adjustments to the dataframe
  data <<- df
  
  #Determine maximum tree level to display
  if(!is.null(display_level)) {
    df <- subset(df, tree_level <= display_level)
  }
  
  #Create a Tree object
  mytree <- as.Node(df) 
  
  #Tree configuration
  GetEdgeLabel <- function(node) switch(node$node_type, node$prob)
  GetNodeShape <- function(node) switch(node$node_type, start = "box", decision_node = "circle", terminal = "none")
  GetNodeLabel <- function(node) switch(node$node_type, 
                                        terminal = ifelse(show_rank  == TRUE, paste0("Prob: ", node$overall_prob,"\nRank: ", node$prob_rank),
                                                          paste0("Prob: ", node$overall_prob)),
                                        node$node_name)
  
  SetEdgeStyle(mytree, fontname = 'helvetica', label = GetEdgeLabel)
  SetNodeStyle(mytree, fontname = 'helvetica', label = GetNodeLabel, shape = GetNodeShape)
  SetGraphStyle(mytree, rankdir = direction) 
  
  #Tree plot
  plot(mytree)
}

#/***********************************************************************************************/#
#/ TREE DIAGRAM - DEFINITION
#/***********************************************************************************************/#
#Define Master Node
#/***********************************************************************************************/#
AddNode(name = 'weather',
        tree_level = 0,
        node_type = 'start')

#Define level 1
#/***********************************************************************************************/#
AddNode(parentnode = 'weather',
        name = 'rain',
        prob = 0.28,
        tree_level = 1,
        node_type = 'decision_node',
        overall_prob = TRUE)

AddNode(parentnode = 'weather',
        name = 'no rain',
        prob = 0.72,
        tree_level = 1,
        node_type = 'decision_node',
        overall_prob = TRUE)

#Define level 2
#/***********************************************************************************************/#
AddNode(parentnode = 'weather/no rain',
        name = '95º F',
        prob = 0.25,
        tree_level = 2,
        node_type = 'decision_node',
        overall_prob = TRUE)

AddNode(parentnode = 'weather/no rain',
        name = '85º F',
        prob = 0.55,
        tree_level = 2,
        node_type = 'decision_node',
        overall_prob = TRUE)

AddNode(parentnode = 'weather/no rain',
        name = '75º F',
        prob = 0.15,
        tree_level = 2,
        node_type = 'decision_node',
        overall_prob = TRUE)

AddNode(parentnode = 'weather/no rain',
        name = '65º F',
        prob = 0.05,
        tree_level = 2,
        node_type = 'decision_node',
        overall_prob = TRUE)

AddNode(parentnode = 'weather/rain',
        name = '95º F',
        prob = 0.05,
        tree_level = 2,
        node_type = 'decision_node',
        overall_prob = TRUE)

AddNode(parentnode = 'weather/rain',
        name = '85º F',
        prob = 0.25,
        tree_level = 2,
        node_type = 'decision_node',
        overall_prob = TRUE,
        prob_rank = NA)

AddNode(parentnode = 'weather/rain',
        name = '75º F',
        prob = 0.35,
        tree_level = 2,
        node_type = 'decision_node',
        overall_prob = TRUE)

AddNode(parentnode = 'weather/rain',
        name = '65º F',
        prob = 0.35,
        tree_level = 2,
        node_type = 'decision_node',
        overall_prob = TRUE)

#Define level 3
#/***********************************************************************************************/#
AddNode(parentnode = 'weather/no rain/95º F',
        name = 'overall',
        tree_level = 3,
        node_type = 'terminal')

AddNode(parentnode = 'weather/no rain/85º F',
        name = 'overall',
        tree_level = 3,
        node_type = 'terminal')

AddNode(parentnode = 'weather/no rain/75º F',
        name = 'overall',
        tree_level = 3,
        node_type = 'terminal')

AddNode(parentnode = 'weather/no rain/65º F',
        name = 'overall',
        tree_level = 3,
        node_type = 'terminal')

AddNode(parentnode = 'weather/rain/95º F',
        name = 'overall',
        tree_level = 3,
        node_type = 'terminal')

AddNode(parentnode = 'weather/rain/85º F',
        name = 'overall',
        tree_level = 3,
        node_type = 'terminal',
        prob_rank = NA)

AddNode(parentnode = 'weather/rain/75º F',
        name = 'overall',
        tree_level = 3,
        node_type = 'terminal')

AddNode(parentnode = 'weather/rain/65º F',
        name = 'overall',
        tree_level = 3,
        node_type = 'terminal')

#/***********************************************************************************************/#
#/ TREE DIAGRAM - PLOT
#/***********************************************************************************************/#
MakeTree(df = data, display_level = max(data$tree_level), show_rank = FALSE, direction = 'LR')
