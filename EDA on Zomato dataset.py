#!/usr/bin/env python
# coding: utf-8

# # EDA on Zomato Dataset

# ### Importing important libraries

# In[256]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
matplotlib.rcParams['figure.figsize'] = (12, 6)


# **Dataset is taken from Kaggle in json format, coverted to 2 files: Zomato.csv and Country-code.excel**

# In[257]:


df = pd.read_csv('zomato.csv', encoding='latin-1')


# In[258]:


df.head()


# In[259]:


df.shape


# In[260]:


df.columns


# In[261]:


df.info()


# In[262]:


df.describe()


# ### Data analysis include:
# **1. Missing values**
# **2. Explore about numberical variable**
# **3. Explore about catagorical variable**
# **4. finding relationship b/n features**

# ### How i can find missing values
# **1. Using isnull func**
# **2. Using query**
# **3. Using heatmap**

# In[263]:


# using isnull func
df.isnull().sum()


# **In cusines, there are 9 missing values. 

# In[264]:


#using query
features = []
for col in df.columns:
    if df[col].isnull().sum()>0:
        features.append(col)
        
        
print(features)


# In[265]:


#using heatmap
sns.heatmap(df.isnull())


# There are only 9 missing values, for that reason it is not visible

# # Importing Country Code data

# In[266]:


df_country = pd.read_excel('Country-Code.xlsx')


# In[267]:


df_country.head()


# In[268]:


df['Country Code'].value_counts()


# ### Merging 2 table: Zomato.csv and Country code.xlsx

# In[269]:


final_df = pd.merge(df, df_country, on="Country Code", how="left")


# In[270]:


final_df.head()


# ### Exploring Features in final_df

# In[271]:


final_df.info()


# In[272]:


final_df.Country.value_counts()


# In[273]:


final_df.Country.value_counts().index


# ### Which country has maximum number of orders?
# **1. Using pandas**
# **2. Using pie chart**

# In[274]:


country_names = final_df.Country.value_counts().index
country_names


# In[275]:


country_names_counts = final_df.Country.value_counts().values
country_names_counts


# In[276]:


plt.pie(country_names_counts, labels=country_names)


# **The above pie chart is bit messy so we are finding top 3 countries that has maximum orders**

# In[277]:


plt.pie(country_names_counts[:3], labels=country_names[:3], autopct="%1.3f%%")


# **Observation
# India has maximum number of orders, then USA, then United Kingdom**

# ### Numberical Variables

# In[278]:


final_df.head()


# In[279]:


final_df["Aggregate rating"].value_counts()


# In[280]:


final_df["Rating color"].value_counts()


# In[281]:


final_df["Rating text"].value_counts()


# In[282]:


ratings = final_df.groupby(['Aggregate rating', 'Rating color', 'Rating text']).size().reset_index().rename(columns={0:"Rating Count"})
ratings


# ## Observation
# 1. 2148 users has not given rating ---> We need to work on it. 
# 2. When rating is between 4.5 to 4.9 --> Excellent
# 3. When rating is between 4 to 4.4 --> Very good
# 4. When rating is between 3.5 to 3.9 -->  good
# 5. When rating is between 2.5 to 3.4 --> average
# 6. When rating is between 1.8 to 2.4 --> poor
# 7. No customer rated 5.
# 
# 

# In[283]:


# Using bar to visulize
sns.barplot(x="Aggregate rating", y="Rating Count", hue="Rating color", data=ratings, palette=['White', 'Red', 'Orange', 'Yellow', 'Green', 'Green'])


# Observation: Maximum rating is between 2.5 to 3.9

# ### Ques: How many users has given 0.0 rating? which country they belong?

# In[284]:


# Method 1
res = final_df['Country'][final_df['Aggregate rating'] == 0.0]
res.count()


# 2148 users has given 0.0 rating.

# In[285]:


#Method 2
ct = final_df[final_df['Aggregate rating'] == 0.0]
ct.count()


# In[286]:


#Method 3
x = final_df[final_df['Rating color'] == 'White'].groupby("Country").size().reset_index()
x


# In[287]:


#Method 4
final_df.groupby(['Aggregate rating', 'Country']).size().reset_index().rename(columns={0:"Counts"})


# ### Observation
# Maximum number of 0 rating are from Indian customers
# 

# ### Ques: Which currency is used by which country?
# 

# In[288]:


final_df.head(50)


# In[289]:


final_df.columns


# In[290]:


final_df.groupby(["Currency", "Country"]).size().reset_index()


# ### Ques: Which countries has online delivery option?

# In[291]:


final_df.head(40)


# In[292]:


final_df["Has Online delivery"].value_counts()


# In[293]:


y = final_df[final_df["Has Online delivery"]=="Yes"].groupby(["Country" , "Has Online delivery"]).size().reset_index().rename(columns={0:"Total yes Counts"})
y


# In[294]:


n = final_df[final_df["Has Online delivery"]=="No"].groupby(["Country" , "Has Online delivery"]).size().reset_index().rename(columns={0:"Total No counts"})
n


# ### Observation: Out of 16 countries, only India and UAE has Opted for Online Delivery.

# ### Ques: Draw a pie chart for City Distribution

# In[295]:


city_names = final_df["City"].value_counts().index
city_names


# In[296]:


city_names_count = final_df["City"].value_counts().values
city_names_count


# In[297]:


plt.pie(city_names_count[:5], labels=city_names[:5],autopct="%.2f%%")


# ### Observation:
# New Delhi has maximum number of orders followed by gurgaon and noida.

# ### Ques: Top 10 Cusines

# In[298]:


#Method 1
final_df["Cuisines"].value_counts().head(10)


# In[299]:


cuisine = final_df["Cuisines"].value_counts().index
cuisine
cuisine_count = final_df["Cuisines"].value_counts().values
cuisine_count


# In[300]:


#plt.pie(city_names_count[:5], labels=city_names[:5],autopct="%.2f%%")
plt.pie(cuisine_count[:5], labels=cuisine[:5], autopct="%.2f%%")


# ### Observation:
# North Indian was the most ordered Cuisine.
