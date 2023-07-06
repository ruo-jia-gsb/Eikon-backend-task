from datetime import datetime as dt
from glob import glob 
import pandas as pd

USER_ID_COL = 'user_id'
EXPERIMENTS_FILE_NAME = 'user_experiments.csv'
COMPOUNDS_FILE_NAME = 'compounds.csv'
USERS_FILE_NAME = 'users.csv'
DATA_FILES = glob('data/*csv')

# Return name of data file if it exists....
def find_data_file(file_name, data_files = DATA_FILES):

    try:
        return [x for x in data_files if file_name in x][0]
    except:
        return False

# Read csv and do a bit of cleaning on text formats 
def extract_data_from_csv(file_name, data_files = DATA_FILES):

    # Allow for a little flexibility on spelling and file formatting
    df = pd.read_csv(find_data_file(file_name, data_files), sep = ",")

    # Remove the extra tabs on the columns' names
    df.columns = [col.strip() for col in df.columns]
    
    # Remove the excess tabs from the columns that have string/object values 
    for col in df.select_dtypes(include=[object]).columns:
        df[col] = df[col].apply(lambda x: str(x).strip())

    return df 

# Calculate the average experiment times, using groupby and mean
def get_avg_experiments_time(experiments_df = extract_data_from_csv(EXPERIMENTS_FILE_NAME),
                               run_time_col = 'experiment_run_time',
                               user_id_col = USER_ID_COL):
    
    avg_run_time = experiments_df[[user_id_col, run_time_col]].groupby(user_id_col).mean().reset_index()
    avg_run_time = avg_run_time.rename(columns = {'experiment_run_time': 'avg_experiment_run_time'})
    return avg_run_time

# Calculate the total experiments run, using groupby and count 
def get_total_experiments(experiments_df = extract_data_from_csv(EXPERIMENTS_FILE_NAME),
                               experiment_id_col = 'experiment_id',
                               user_id_col = USER_ID_COL):
    
    total_experiments = experiments_df[[user_id_col, experiment_id_col]].groupby(user_id_col).count().reset_index()
    total_experiments = total_experiments.rename(columns = {'experiment_id': 'total_experiments_run'})
    return total_experiments
    
# Multi-step process due to complexity, explode, rank, and re-combine results 
def get_most_popular_compounds(experiments_df = extract_data_from_csv(EXPERIMENTS_FILE_NAME), 
                              compounds_df = extract_data_from_csv(COMPOUNDS_FILE_NAME),
                              user_id_col = USER_ID_COL, 
                              compounds_id_col = 'compound_id',
                              experiments_compounds_col = 'experiment_compound_ids'):

    # Convert compounds_id_col to be string, since it will merge on column 'compound_id' that's also string
    compounds_df[compounds_id_col] = compounds_df[compounds_id_col].apply(str)

    # Explode the experiment_compound_ids column so each compound is represented by its own row
    compounds_usage = experiments_df[[user_id_col, experiments_compounds_col]].copy()
    compounds_usage[compounds_id_col] = compounds_usage.pop(experiments_compounds_col).apply(lambda x: x.split(';'))
    compounds_usage = compounds_usage.explode(compounds_id_col)

    # Now count the frequency of each user-compound combination, and rank them by this count in descending order
    compounds_usage['count'] = True
    compounds_usage = compounds_usage.groupby([user_id_col, compounds_id_col])['count'].count().reset_index()
    compounds_usage['popularity'] = compounds_usage.groupby(user_id_col)['count'].rank(method = 'dense', ascending=False).astype(int)

    # Keep the user-compound rows with rank = 1, i.e most popular
    compounds_usage = compounds_usage[compounds_usage.popularity == 1]

    # Combine results to get the names and structures of these compounds
    compounds_usage = compounds_usage.merge(compounds_df, how = 'left', on = compounds_id_col)

    # Since multiple compounds be equally popular for a given user, combine them and separate by ;
    most_popular_compounds = pd.DataFrame(compounds_usage.groupby(['user_id'])[compounds_id_col].apply(lambda x: ';'.join(x)))
    most_popular_compounds['most_popular_compound_names'] = compounds_usage.groupby([user_id_col])['compound_name'].apply(lambda x: ';'.join(x))
    most_popular_compounds['most_popular_compound_structures'] = compounds_usage.groupby([user_id_col])['compound_structure'].apply(lambda x: ';'.join(x))
    most_popular_compounds = most_popular_compounds.reset_index().rename(columns = {compounds_id_col: 'most_popular_compound_ids'})

    return most_popular_compounds

# Combine the preceding 3 processes into one, and combine their results with the users dim data
def generate_data_features():

    experiments_df = extract_data_from_csv(EXPERIMENTS_FILE_NAME)
    compounds_df = extract_data_from_csv(COMPOUNDS_FILE_NAME)
    user_df = extract_data_from_csv(USERS_FILE_NAME)

    most_popular_compounds = get_most_popular_compounds(experiments_df = experiments_df, compounds_df = compounds_df)
    avg_run_time = get_avg_experiments_time(experiments_df=experiments_df)
    total_experiments = get_total_experiments(experiments_df = experiments_df)

    user_df['time_created'] = dt.now()
    user_df['time_updated'] = None

    return  user_df.merge(total_experiments, on = USER_ID_COL).\
                    merge(avg_run_time, on = USER_ID_COL).\
                    merge(most_popular_compounds, on = USER_ID_COL)

# Uploading data can be potentially time consuming so use async 
async def upload_df_to_table(df: pd.DataFrame, table_name: str, connection):

    with connection as connection:
        df.to_sql(
            name=table_name,
            con=connection,
            if_exists="append",
            chunksize=10_000, #Optimal speed for medium sized loads
            index=False
        )