#!/usr/bin/python

import sqlite3
import base64

from flask import Flask, request, render_template, redirect
from math import floor
from sqlite3 import OperationalError
from urlparse import urlparse

# Setup Flask and store some base variables
app = Flask(__name__)
hostname = 'http://localhost:8000/'
str_encode = str

# These are all of the possible values for a shortened URL
base_62_values = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Use a mapping range of 28 to generate 6 character strings
mapping = range(28)
mapping.reverse()

"""
Create the database table and handle if it already exists
"""
def createTable():
    create_table = """
        CREATE TABLE URL_LINKS(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        URL TEXT NOT NULL
        );
        """
    with sqlite3.connect('url_links.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(create_table)
        except OperationalError as e:
            if e.message == "table URL_LINKS already exists":
                # The table already exists in the database, continue forward
                pass
            else:
                raise OperationalError("There was an error creating the database table")


"""
Convert a value to base 62
"""
def convertToBase62(num):
    remainder = num % 62
    result = base_62_values[remainder]
    dividend = floor(num / 62)
    while dividend:
        remainder = dividend % 62
        dividend = floor(dividend / 62)
        result = base_62_values[int(remainder)] + result
    return result


"""
Convert from a starting base back to base 10
"""
def convertToBase10(num, initialBase=62):
    limit = len(num)
    result = 0
    for i in range(limit):
        result = initialBase * result + base_62_values.find(num[i])
    return result


"""
Encode the bits by shuffling them to produce pseudo random links
"""
def encode(n):
    result = 0
    for i, b in enumerate(mapping):
        b1 = 1 << i
        b2 = 1 << mapping[i]
        if n & b1:
            result |= b2
    return result


"""
Decode the bits by unshuffling them using the same mapping
"""
def decode(n):
    result = 0
    for i, b in enumerate(mapping):
        b1 = 1 << i
        b2 = 1 << mapping[i]
        if n & b2:
            result |= b1
    return result


"""
The main link page and url shortner API
"""
@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        original_url = str_encode(request.form.get('url'))
        if urlparse(original_url).scheme == '':
            url = 'http://' + original_url
        else:
            url = original_url
        with sqlite3.connect('url_links.db') as conn:
            cursor = conn.cursor()
            res = cursor.execute(
                'INSERT INTO URL_LINKS (URL) VALUES (?)',
                [base64.urlsafe_b64encode(url)]
            )
            encoded_string = convertToBase62(encode(res.lastrowid))
        return render_template('home.html', short_url=hostname + encoded_string)
    return render_template('home.html')


"""
The redirect API
"""
@app.route('/<short_url>')
def redirect_link(short_url):
    decoded = decode(convertToBase10(short_url))
    url = hostname  # fallback if no URL is found
    with sqlite3.connect('url_links.db') as conn:
        cursor = conn.cursor()
        res = cursor.execute('SELECT URL FROM URL_LINKS WHERE ID=?', [decoded])
        try:
            base64EncodedUrl = res.fetchone()
            if base64EncodedUrl is not None:
                url = base64.urlsafe_b64decode(str(base64EncodedUrl[0]))
        except Exception as e:
            print(e)
    return redirect(url)


if __name__ == '__main__':
    createTable()
    app.run(port=8000)
