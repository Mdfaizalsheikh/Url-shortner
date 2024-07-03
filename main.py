import tkinter as tk
from tkinter import messagebox
import sqlite3
import string
import random

conn = sqlite3.connect('urls.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS urls
             (id INTEGER PRIMARY KEY, long_url TEXT, short_url TEXT)''')
conn.commit()

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    c.execute("SELECT short_url FROM urls WHERE short_url = ?", (short_url,))
    if c.fetchone():
        return generate_short_url()
    return short_url

def shorten_url():
    long_url = long_url_entry.get()
    if not long_url:
        messagebox.showwarning("Input Error", "Please enter a URL")
        return

    c.execute("SELECT short_url FROM urls WHERE long_url = ?", (long_url,))
    result = c.fetchone()
    if result:
        short_url = result[0]
    else:
        short_url = generate_short_url()
        c.execute("INSERT INTO urls (long_url, short_url) VALUES (?, ?)", (long_url, short_url))
        conn.commit()

    short_url_display.config(text="Short URL: " + short_url)


app = tk.Tk()
app.title("URL Shortener")

tk.Label(app, text="Enter URL:").grid(row=0, column=0, padx=10, pady=10)

long_url_entry = tk.Entry(app, width=50)
long_url_entry.grid(row=0, column=1, padx=10, pady=10)

shorten_button = tk.Button(app, text="Shorten URL", command=shorten_url)
shorten_button.grid(row=1, column=0, columnspan=2, pady=10)

short_url_display = tk.Label(app, text="")
short_url_display.grid(row=2, column=0, columnspan=2, pady=10)

app.mainloop()


conn.close()
