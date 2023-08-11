import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.express as px

df_apps = pd.read_csv('apps.csv')

# [1] describe the dataframes
# >>> print(df_apps.describe())
# >>> print(df_apps.shape)
# (10841, 12)
# [1.1] take a random sample of 5 rows
# >>> print(df_apps.sample(5))

# [2] drop unnecessary columns
df_apps.drop(columns=['Last_Updated', 'Android_Ver'], axis=1, inplace=True)
# [2.1] clean from NaN values
df_apps.dropna(inplace=True)
# (9767, 10)
# [2.2] drop duplicates - subset defines the criteria for two entries being a duplicate
df_apps.drop_duplicates(subset=['App', 'Type', 'Price'], inplace=True)
# (8199, 10)

# [3] preliminary exploration
# [3.1] app with the highest ratings
highest_rating_apps = df_apps[df_apps['Rating'] == df_apps['Rating'].max()]
# >>> print(highest_rating_apps.shape)
# (271, 10)
# [3.2] apps with the largest file size
largest_apps = df_apps[df_apps['Size_MBs'] == df_apps['Size_MBs'].max()]
# >>> print(largest_apps.shape)
# (14, 10)
# [3.3] 50 most reviewed apps
most_reviewed = df_apps.nlargest(50, 'Reviews')
# print(most_reviewed[['App', 'Reviews']])
most_reviewed_paid = most_reviewed[most_reviewed['Type'] == 'Paid']
# >>> print(most_reviewed_paid.shape)
# (0, 10)
# top 50 most reviewed apps are free

# [4] visualize Ratings values in a pie-chart
ratings = df_apps.Content_Rating.value_counts()
chart = px.pie(labels=ratings.index,
               values=ratings.values,
               title='Content Rating',
               names=ratings.index,
               hole=0.6)
# ^ hole argument turns the pie chart into a donut chart
chart.update_traces(textposition='inside', textfont_size=15, textinfo='percent')
# ^ alternative: textinfo='label+percent'; textposition='outside'
chart.show()

# [5] type conversion for the installations & price data
# [5.1] apps with over 1 billion installs and apps with 1 install
df_apps.Installs = df_apps.Installs.astype(str).str.replace(',', "")
df_apps.Installs = pd.to_numeric(df_apps.Installs)
bln_installs = df_apps[df_apps.Installs >= 1000000000]
# >>> print(bln_installs[['App', 'Installs']])
# >>> print(bln_installs.shape)
# (20, 10)
one_install = df_apps[df_apps.Installs == 1]
# >>> print(one_install[['App', 'Installs']])
# >>> print(one_install.shape)
# (3, 10)
# [5.2] top 20 most expensive apps








