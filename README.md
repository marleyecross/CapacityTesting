# CapacityTesting
Capacity Testing Sample Code

This is a small subset of a larger script, the purpose of which is to compare measured and expected solar plant data.
The inputs to the full script are 3 excel files:
  1) a measured data file
  2) an expected data file
  3) a config file, containing key parameters for the regression including AC size and min irradiance for filtering
  
'Prepped Data Measured.xlsx' is a sample of measured data from a 3.9 MW AC solar-only system. This sample script only uses measured data and a config file.

ASTM standards for PV Capacity Testing require specific filtering of measured and expected data:

primary_filtering_m takes in a dataframe of measured data and a dataframe of config variables, and returns a dataframe with added columns of 1s and 0s indicating whether each row (timestamp) of data satisfies the filter conditions. These 1s and 0s are added for visual purposes in the final report printout.

To test primary_filtering_m, you can run it using meas_data = measured_data and config = config_filters.
 
primary_filtered_m takes in a dataframe returned from primary_filtering_m and returns a dataframe including only rows that satisfy all filtering critera.
