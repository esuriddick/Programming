# Purpose of this program
Assign a ranking to any killer in the video game Dead By Daylight according to the criteria created by a streamer in the channel **not Otzdarva**.
The criteria defined by this streamer are the following:
* Skill ceiling: potential to snowball (e.g., slugging), control the map/generators, chase potential, etc.
* Add-ons: strength of the add-ons on the killer's general performance.
* Map dependency: influence of different map layouts in the killer's general performance.
* Unhook scenarios: potential to deal with different unhooking scenarios (e.g., several survivors rushing the hook).
It should be noted that there is no explicit definition for each of these criterion, so the definitions provided are my own interpretation.

# Dependencies
You need an input file with the score assigned to each of the criterion necessary to assess a killer's ranking. The Excel file provided is based on the review performed as of **20th August 2022** in the channel **not Otzdarva**.

# Additional information
The PDF provided is just a printable version of the Jupyter Notebook code provided, while the file _killer_rank_model.joblib_ contains the parameters of the best model identified during our process, namely a Random Forest classifier.
