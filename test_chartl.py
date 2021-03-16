from utils import send_mail
import sys, json
from email_theme import body_html
import pandas as pd
from sqlalchemy import create_engine
from pretty_html_table import build_table
import sys
import os
from datetime import datetime
import emoji



import sqlite3
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns





SQL = """SELECT user_id,
                created_dt,
                id,
                followers,
                followees,
                posts
FROM bots
WHERE user_id = 1"""

# Read sqlite query results into a pandas DataFrame
# con = sqlite3.connect("data.db")

engine = create_engine('sqlite:///data.db')

df = pd.read_sql_query(SQL, engine)









plt.figure() # Push new figure on stack
fig = plt.gcf()


# Change seaborn plot size
fig.set_size_inches(12, 8)


# create plot

sns_plot = sns.barplot(x = "created_dt", y = "followers", palette = 'magma', data = df)

fig.savefig('example.png')







# Verify that result of SQL query is stored in the dataframe
print(df.head())
