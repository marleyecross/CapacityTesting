import statsmodels.api as sm
import pandas as pd
import numpy as np

# Data import and formatting:

measured_data = pd.read_excel('Prepped Data Measured.xlsx')
measured_data.head()
measured_data.columns = ['date', 'irradiance', 'tamb', 'combined', 'wind']

config_data = pd.read_excel('Config.xlsx')
config_data.head()

config_filters = config_data.filter(['Lower Bound RC', 'Upper Bound RC', 'Lower Bound Unstable Sky', 'Upper Bound Unstable Sky', 'Min Irradiance', 'SE Filtering'])
config_filters['AC Clipping'] = config_data['Project AC Size']*.98
config_filters.head()


# Helper Function for Irradiance Filtering:

def unstable_irr (irr_data):
    """
    takes in a column of irr data and returns a new column of 0s and 1s
    indicating data points that meet and exceed unstable irr filter criteria
    """
    unstable_irr = list()
    for index, value in irr_data.items():
        if index == 0:
            unstable_irr.append(0)
        elif (value > irr_data[index - 1]*config_filters['Lower Bound Unstable Sky'][0]) and (value < irr_data[index-1]*config_filters['Upper Bound Unstable Sky'][0]):
            unstable_irr.append(1)
        else:
            unstable_irr.append(0)
    return unstable_irr

# Primary Data Filtering:

def primary_filtering_m(meas_data, config):
    """
    takes in a pandas dataframe of measured data
    adds columns with 1s and 0s for primary filtering
    """
    pri_filtering_df = meas_data
    pri_filtering_df['Min Irradiance'] = np.where(pri_filtering_df['irradiance'] > config['Min Irradiance'][0], 1,0 )
    pri_filtering_df['Site Clipping'] = np.where(pri_filtering_df['combined'] < config['AC Clipping'][0], 1, 0)
    pri_filtering_df['Missing Data'] = np.where(pd.isnull(pri_filtering_df['irradiance']) | pd.isnull(pri_filtering_df['tamb']) | pd.isnull(pri_filtering_df['combined']) | pd.isnull(pri_filtering_df['wind']), 0, 1)
    pri_filtering_df['Unstable_Irradiance'] = unstable_irr(pri_filtering_df['irradiance'])
    return pri_filtering_df

def primary_filtered_m(pri_filtering):
    """
    takes in a primary filtering dataframe and returns a dataframe with only timestamps that meet all filtering criteria
    """
    primary_filtered_df = pri_filtering.loc[np.where((pri_filtering['Min Irradiance']==1) & (pri_filtering['Site Clipping']==1) & (pri_filtering['Missing Data']==1)
    & (pri_filtering['Unstable_Irradiance']==1) & (pri_filtering['Min Irradiance']==1))]
    return primary_filtered_df


