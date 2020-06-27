"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from EnciclaWeb import app

import os
import pandas as pd
import numpy as np
# Required for basic python plotting functionality
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import urllib.parse
import io
import base64

df = pd.read_csv("EnciclaWeb/data/inventory.csv", encoding='ISO-8859-1')
df['YYYY'] = df['Date'].str[:4]
df['MM'] = df['Date'].str[5:7]
df['DD'] = df['Date'].str[5:7]
df['TIME'] = df['Date'].str[11:16]
df['datetime'] = pd.to_datetime(df['YYYY'] + '-' + df['MM'] + '-' + df['DD'] + ' ' + df['TIME'], format='%Y-%m-%d %H:%M')
df['HOUR'] = pd.DatetimeIndex(df['datetime']).hour

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template('index.html',
        title='Home Page',
        year=datetime.now().year)

@app.route('/plotTest')
def plotTest():
    """Renders the plot test page."""
    df_temp = df[['HOUR', 'Station_name', 'Station_bikes']][df['Station_bikes'] == 0].groupby('HOUR').agg({'Station_name':'size'}).reset_index()
    df_temp.columns = ['HOUR', 'Stations_without_bikes']
    plt.plot(df_temp['HOUR'], df_temp['Stations_without_bikes'])
    img = io.BytesIO()  # create the buffer
    plt.savefig(img, format='png')  # save figure to the buffer
    img.seek(0)  # rewind your buffer
    plot_data = urllib.parse.quote(base64.b64encode(img.read()).decode()) # base64 encode & URL-escape
    return render_template('plot-test.html',
        title='Some Plots',
        inventories = df_temp.head(10).to_html(classes='table table-striped'),
        plot_url = plot_data,
        year=datetime.now().year)

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template('contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.')

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template('about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.')

