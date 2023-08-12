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
# chart.show()

# [5] type conversion for the installations & price data
# [5.1] apps with over 1 billion installs and apps with 1 install
df_apps.Installs = df_apps.Installs.astype(str).str.replace(',', '')
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
df_apps.Price = df_apps.Price.astype(str).str.replace('$', '')
df_apps.Price = pd.to_numeric(df_apps.Price)
# >>> print(df_apps.sort_values('Price', ascending=False).head(20))
# [5.3] remove apps more expensive than 250$ and create a revenue projection column
df_apps = df_apps[df_apps['Price'] < 250]
# >>> print(df_apps.sort_values('Price', ascending=False).head(5)[['App', 'Price']])
# # 2281  Vargo Anesthesia Mega App  79.99
# # 1407               LTC AS Legal  39.99
# # 2629           I am Rich Person  37.99
df_apps['Revenue_Estimate'] = df_apps.Installs.mul(df_apps.Price)
# >>> print(df_apps.sort_values('Revenue_Estimate', ascending=False)[:10][['App', 'Revenue_Estimate']])
# # 9220                      Minecraft        69900000.0
# # 8825                  Hitman Sniper         9900000.0
# # 7151  Grand Theft Auto: San Andreas         6990000.0

# [6] Analyze different app categories
# >>> print(df_apps.Category.nunique())
# # 33
# [6.1] top 10 categories
top_10_category = df_apps.Category.value_counts()[:10]
# >>> print(top_10_category)
# # FAMILY             1606
# # GAME                910
# # TOOLS               719
# # ...
bar = px.bar(x=top_10_category.index, y=top_10_category.values)
# bar.show()
# [6.2] group apps by category and sum the number of installations
category_installs = df_apps.groupby('Category').agg({'Installs': pd.Series.sum})
category_installs.sort_values('Installs', ascending=False, inplace=True)
# >>> print(category_installs)
h_bar = px.bar(x=category_installs.Installs,
               y=category_installs.index,
               orientation='h',
               title='Category Popularity',)

h_bar.update_layout(xaxis_title='Number of Downloads',
                    yaxis_title='Category')

# h_bar.show()

# [6.3] create a scatter plot to show number of apps and number of installs for different categories
cat_number = df_apps.groupby('Category').agg({'App': pd.Series.count})
cat_merged_df = pd.merge(cat_number, category_installs, on='Category', how='inner')
cat_merged_df.sort_values('Installs', ascending=False)

scatter = px.scatter(cat_merged_df,
                     x='App',
                     y='Installs',
                     title='Category Concentration',
                     size='App',
                     hover_name=cat_merged_df.index,
                     color='Installs')

scatter.update_layout(xaxis_title='Number of Apps (Lower=More Concentrated)',
                      yaxis_title='Installs',
                      yaxis=dict(type='log'))

scatter.show()







