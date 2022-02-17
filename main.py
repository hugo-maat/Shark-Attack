import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
Assignment: Shark Attacks
for Winc Academy
Hugo Maat, 17/2/2022
"""

df = pd.read_csv('C:\Users\hugom\OneDrive\Documents\Winc\Python\shark attack\attacks.csv') #, encoding = "ISO-8859-1")
# changed encoding based on advice on StackOverflow, utf-8 gave error.

# dropping columns (although it might be better to indicate which ones not to drop)

df2 = df.drop(columns=[
      'Case Number', 'Date', 'Year', 'Country', 'Area', 'Location', 'Name', 'Sex ',
      'Time', 'Investigator or Source','pdf', 'href', 'href formula', 'Case Number.1', 
      'Case Number.2', 'Unnamed: 22','Unnamed: 23', 'original order'])

# dropping rows that only contain null values

df3 = df2.dropna(how='all').copy()
new_columns = ['type','activity','age','injury','was_fatal','species']
df3.columns = new_columns

# Checked for distribution in years

test_df1 = df.dropna(how='all').copy()
test_df1.loc[test_df1['Year'] > 1900,['Year']].value_counts()
records_since_1900 = len(test_df1.loc[test_df1['Year'] > 1900,['Year']])
relative = records_since_1900 / len(test_df1)
relative # = 0.64

# Less than two-thirds of the reports with a year are from after 1900. 

#####################################################################

# Preparation: changing values

# First: Going to use the non-standard null value filter from the 
# Questionnaire excercises

def searching_non_standard_nulls(df, column):
  current_column = df.loc[:,column]
  print("Tactic 1: unique values \n")
  unique_limit = 50
  unique_values = current_column.unique()
  if len(unique_values) == len(df):
    print(f"{column} is all unique values!")
  elif len(unique_values) > 10:
    print(f"There are more than ten unique values: \n {unique_values[:11]}")
  else:
    print("There are fewer than ten unique values:", unique_values, "\n")
  print("Tactic 2: heads and tails \n")
  heads = current_column.head()
  tails = current_column.tail()
  print(heads, "\n", tails, "\n")
  print("Tactic 3: casting to type\n")
  for dtype in ['integer','float','string','bool']:
    try:
      current_column.astype(dtype)
      print(f'Can be cast to {dtype}')
    except:
      print(f'Could not be cast to {dtype}')
  try:
    sorted = current_column.dropna().sort_values()
    print("Data can be sorted:\n", sorted)
  except:
    print("Data could not be sorted\n")
  print("Tactic 4: checking frequency\n", current_column.value_counts(dropna=False))

# Column 'type'
# searching_non_standard_nulls(df3, 'type')

# Column 'type' contains value 'Invalid' and nan which whould be None.
# Also has 'Boating', 'Boat', and 'Boatomg'. Going to merge those three.

def change_values(df, column, old_value, new_value):
    new_df = df[column].replace({old_value: new_value}, inplace=True)
    return new_df

change_values(df3, 'type', 'Invalid', None)
change_values(df3, 'type', np.nan, None)
change_values(df3, 'type', 'Boat', 'Boating')
change_values(df3, 'type', 'Boatomg', 'Boating')

# Column 'activity'

change_values(df3, 'activity', np.nan, None)

# searching_non_standard_nulls(df3, 'activity')

# Column 'age'

# searching_non_standard_nulls(df3, 'age')
change_values(df3, 'age', ' ', np.nan)
change_values(df3, 'age', '', np.nan)

# Column 'injury'

change_values(df3, 'injury', 'unknown', None)
# searching_non_standard_nulls(df3, 'injury')

# Column 'was_fatal'

change_values(df3, 'was_fatal', 'y', True)
change_values(df3, 'was_fatal', 'Y', True)
change_values(df3, 'was_fatal', 'N', False)
change_values(df3, 'was_fatal', np.nan, None)
change_values(df3, 'was_fatal', 'UNKNOWN', None)
change_values(df3, 'was_fatal', 'M', False)
change_values(df3, 'was_fatal', '2017', None)
change_values(df3, 'was_fatal', ' N', False)
change_values(df3, 'was_fatal', 'N  ', False)
change_values(df3, 'was_fatal', 'N ', False)

# searching_non_standard_nulls(df3, 'was_fatal')

# Column 'species'

change_values(df3, 'species', 'Invalid', None)
change_values(df3, 'species', np.nan, None)
change_values(df3, 'species', '', None)
# searching_non_standard_nulls(df3, 'species')

#####################################################################

# Question 1: What are the most dangerous types of sharks to humans?
df3['species'].unique().size
# There are 1466 different values in this set.

# No value for species is significant missing data for this question.
question1df = df3.dropna(subset=['species']).copy()

def only_shark_name(col):
    index = col.find('shark')
    space_index = col.rfind(' ',0,index-1)
    if space_index == -1:
        return col[:index+5]
    else:
        return col[space_index+1:index+5]

question1df.loc[:,'species'] = question1df.transform({'species':only_shark_name})
question1df.loc[:,'species'] = question1df.transform({'species':str.lower})

# this transformation normalizes the names of sharks so we don't have to deal with
# "5 foot bull shark" or similar variants. This makes the idenfiable shark species
# countable. 

# It did introduce a few new empty strings.
change_values(question1df, 'species', '', None)
question1df = question1df.dropna(subset=['species']).copy()

question1df['species'].value_counts()[:20]

# Let's focus on the top 3, the white shark, tiger shark, and bull shark.
# But: what does "most dangerous to humans" mean? This is only the number of
# recorded attacks. Let's check the fatality rate as well.

def fatality_rate_per_species(df, species):
    fatality_rate = df.loc[df['species'] == species,['was_fatal']].mean()
    attacks = len(df.loc[df['species'] == species])
    percentage = round(fatality_rate[0]*100,2)
    of_total = round(attacks / len(question1df) * 100,2)
    print(f"The fatality rate of a {species} attack is {percentage}%.\
    \nBased on {attacks} attacks. That's {of_total}% of the sample.\n")
    
for species in question1df['species'].value_counts()[:3].index:
    fatality_rate_per_species(question1df,species)

"""
The fatality rate of a white shark attack is 23.06%.    
Based on 633 attacks. That's 21.46% of the sample.

The fatality rate of a tiger shark attack is 27.45%.    
Based on 259 attacks. That's 8.78% of the sample.

The fatality rate of a bull shark attack is 21.51%.    
Based on 173 attacks. That's 5.86% of the sample.
"""

# Fatal attacks seem somewhat evenly distributed amongst the top three species. 
# My conclusion is that with 21% of identifiable cases of attacks, 
# white sharks appear to be the most dangerous species of shark for humans.

# However: there is a chance for bias in the reporting. "White shark" could
# simply describe the color rather than the actual species. Maybe the white
# shark is easier to recognize, being one of the most well-known species.

#####################################################################

# Question 2: Are children more likely to be attacked by sharks?

# Since this DataFrame is a collection of shark attacks, we only need the
# 'age' column for this question. 

df3.loc[:,'age'].isna().mean()

# That column is 45% missing values. There don't appear to be any other columns
# containing data covariant with age. And since the measurements are arbitrary
# there are no reliable methods to impute the age of the attack victim.

df3['age'].unique()

# Which of these values should be considered 'a child'? Numeric values below 17.
# Certainly any age measureable in months, and anything 'young' or 'teen' as well.

df3.loc[df3['age'].str.contains('month', na=False),'age'] = 1
df3.loc[df3['age'].str.contains('een', na=False),'age'] = 16
df3.loc[df3['age'].str.contains('young', na=False),'age'] = 16

def make_number(str):
    try:
      leftmost = str[:3].strip()
      numeric = int(leftmost)
      return numeric
    except:
      try:
        leftmost = str[:2].strip()
        numeric = int(leftmost)
        return numeric
      except:
        return np.nan

question2df = df3.copy()

for index, row in question2df.iterrows():
    old = question2df.loc[index,'age']
    question2df.loc[index,'age'] = make_number(old)

question2df.loc[:,'age'].isna().sum() - df3.loc[:,'age'].isna().sum()

# This removes 40 objects from the 'age' column, the remainder is now in integer.
# Now to visualize the distribution:

age_median = question2df.loc[:,'age'].value_counts().median()
question2df['age'].value_counts().sort_index().plot\
(kind='bar', xticks=range(0,80,10), xlabel='Age', ylabel='Attacks', \
title='Recorded attacks by victim age', figsize=(15,10))
plt.axvline(17.5, color='r') # line indicating the age of 18
plt.axvline(age_median, color='g') # median

# This looks like a result. The answer to question 2 would be:
# "There are numerous shark attacks where the victim was below the 
# age of 18. However, median human age in 2015 was 29.6 
# (https://ourworldindata.org/) # and most of these records are older
# than that. Are children more likely to be attacked by sharks? Hard
# to say. The data does # not appear to diverge significantly from 
# human age distribution. Also, the # dataset is biased because it 
# only records shark attacks, not 'no shark attacks.'

#####################################################################

# Question 3: Are shark attacks where sharks were provoked more or less dangerous?

# How do we measure danger? The easiest indicator is the fatality rate. That means
# we need two columns: one that indicates whether or not the attack was provoked,
# and one indicating whether or not the attack was fatal for the victim.

df3['type'].value_counts() # seems clean enough to work with
df3['was_fatal'].value_counts() 

question3df = df3.dropna(subset=['type','was_fatal']).loc[:,['type','was_fatal']]
# this removes about 10% of rows. 

# I only need to know whether an attack was provoked or not, so:

question3df.loc[question3df['type'] != 'Provoked','type'] = 'Unprovoked'

# Now to calculate the rate of fatal outcome for provoked and unprovoked:

provoked_fatal = question3df.loc[question3df['type'] == 'Provoked','was_fatal'].mean()
unprovoked_fatal = question3df.loc[question3df['type'] == 'Unprovoked','was_fatal'].mean()
print(f"Provoked attacks had a fatal outcome in {round(provoked_fatal*100,2)}% \
of recorded cases, and unprovoked attacks had a fatal outcome in {round(unprovoked_fatal*100,2)}% \
of recorded cases.")

# It seems attacks where the sharks were provoked were less dangerous.

#####################################################################

# Question 4: Are certain activities more likely to result in a shark attack?

# This is a tricky question to answer statistically. Let's take for instance
# the activity 'swimming'. From this dataset we can find out how many shark attacks
# happened while people were swimming. We cannot, however, find out if swimming
# is likely to result in a shark attack, because we don't have data on people
# who were swimming and were not attacked by sharks. As far as the dataset is
# concerned, swimming results in a shark attack in 100% of recorded cases.

# I would presume that "making a documentary about sharks" results in a higher
# risk of a shark attack, but I don't think I could find statistical evidence
# for this. I would need records of shark documentaries without shark attacks,
# and a control sample (like data on swimmers NOT attacked by sharks).

# Because I don't want to hand in this assignment with a question simply left
# blank, I will try to make an analysis based on the activities noted in the 
# shark attacks dataset.

df3.loc[:,'activity'].value_counts()[-10:]
len(df3['activity'].unique()) / len(df3['activity'])
df3['activity'].isna().mean()

question4df = df3.dropna(subset=['activity']).loc[:,['activity']]
len(question4df['activity'].unique())

# There are 1532 unique values for activity. Looks like there are several 
# values that are rather long strings. I'll reuse some code from question 1, 
# to try and bring out the gerund verbs (words that end in '-ing').

def only_activity_verb(col):
    index = col.find('ing')
    space_index = col.rfind(' ',0,index)
    if index == -1:
        return None
    elif space_index == -1:
        return col[:index+3].lower().strip(' "')
    else:
        return col[space_index+1:index+3].lower().strip(' "')

question4df.loc[:,'activity'] = question4df.transform({'activity':only_activity_verb})

len(question4df['activity'].unique()) # down to 206 unique values
len(question4df['activity']) / len(df3['activity']) # lost about 9% of rows

question4df['activity'].value_counts()[:11].plot.bar(rot=45, figsize=(15,10), xlabel='Activities',ylabel='Recorded attacks')

# The graph shows that most shark attacks happened when the victim was swimming
# or surfing. It is reasonable to assume that the total number of people
# swimming is greater than the total number of people surfing, which would make
# surfing the more dangerous activity. I have not been able to find a dataset
# of for instance how many people go swimming in Florida waters per year, so it
# is difficult to make a proper assessment of these risks.