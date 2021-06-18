#Import Libs
import pandas as pd

# Inputs
#col_name = input('What is the name of the column to convert to columns?: ')
#keyz = input('what are the names of the columns that uniquely identify a row? (seperate these with pipes "|"):')
#keyz.split('|')
file_dir = r'data.xlsx'
output_dir = r'data-out.xlsx'
list_key_cols = ['Person - Medical Record Number', 'CE-Verified DT/TM']
# This is the column that you want to return the unique items and make those the unique iterms the headings for new columns
split_col = 'Clinical Event'
# Use this data to fill in the new columns
filler_col = 'Clinical Event Result'

# Create Dataframe
df = pd.read_excel(
    file_dir
    )

#convert to strings
df = df.applymap(str)
# Make the primary key
series_primary_key = df[list_key_cols].sum(1)
df['primary-key']=series_primary_key
# new base dataframe
dfa = df.drop(
    [split_col, filler_col],
    axis='columns'
    )
# drop duplicates
dfa.drop_duplicates(
    keep='first',
    inplace=True,
)

dfa.set_index(keys='primary-key', inplace=True)

# new columns
new_cols = pd.unique(df[split_col])
for item in new_cols:
    dfa[item]=''

# Iterate and fill in dfa
for a_key in series_primary_key:
    for col_name in new_cols:
        df_temp = df.loc[df['primary-key'] == a_key]
        df_temp = df_temp.loc[df_temp[split_col] == col_name]
        df_temp.reset_index(inplace=True)
        try:
            cell_text = df_temp.at[0, filler_col]
            dfa.at[a_key, col_name] = cell_text
        except:
            print('1')

# Export dataframe
dfa.to_excel(output_dir, index = False)