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





SQL = """SELECT -- user_id,
                created_dt as x,
                -- id,
                followers,
                followees,
                posts
FROM bots
WHERE user_id = 1"""


engine = create_engine('sqlite:///data.db')

df = pd.read_sql_query(SQL, engine)



print(plt.style.available)


plt.style.use('fivethirtyeight')

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Ubuntu'
plt.rcParams['font.monospace'] = 'Ubuntu Mono'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titlesize'] = 10
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 12



fig = plt.figure(figsize=(10,5), dpi=72)




plt.xlabel('Age (days)')
plt.ylabel('Closed sales')
ax2.set_title('Opportunities age', fontstyle='italic')





plt.savefig('books_read.png')


# Verify that result of SQL query is stored in the dataframe
print(df.head())
