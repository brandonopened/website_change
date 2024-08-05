import requests
import hashlib
import tkinter as tk
from tkinter import Text, Label
import threading
import time
import webbrowser

# URLs of the websites you want to monitor
urls = {
    "Alaska": "https://education.alaska.gov/earlylearning",
    "California": "https://www.cde.ca.gov/sp/cd/re/psfoundations.asp",
    "Florida": "https://flbt5.floridaearlylearning.com/",
    "Oregon": "https://www.oregon.gov/ode/students-and-family/Transitioning-to-Kindergarten/Documents/ODE_EarlyLearningStandards_final.pdf",
    "Texas": "https://tea.texas.gov/academics/early-childhood-education/2022-texas-pkg-comprehensive-guide.pdf"
}

# Global dictionary to store the status of the websites
site_status = {state: "No Change" for state in urls}
site_hashes = {state: None for state in urls}

def get_site_hash(url):
    response = requests.get(url)
    content_hash = hashlib.md5(response.content).hexdigest()
    return content_hash

def monitor_websites():
    global site_status, site_hashes
    while True:
        for state, url in urls.items():
            try:
                current_hash = get_site_hash(url)
                if site_hashes[state] is None:
                    site_hashes[state] = current_hash
                elif current_hash != site_hashes[state]:
                    site_status[state] = "Changed"
                    status_labels[state].config(bg="red")
                    site_hashes[state] = current_hash
                else:
                    site_status[state] = "No Change"
                    status_labels[state].config(bg="green")
            except Exception as e:
                site_status[state] = f"Error: {str(e)}"
        time.sleep(86400)  # Check every 24 hours

def open_url(event):
    url = event.widget.cget("text")
    webbrowser.open_new(url)

# Set up the UI
root = tk.Tk()
root.title("Website Change Monitor")

status_labels = {}

for state in urls:
    url_label = Label(root, text=f"{state} URL to Monitor:")
    url_label.pack()

    url_value = Text(root, height=1, width=80, fg="blue", cursor="hand2", bd=0)
    url_value.insert(tk.END, urls[state])
    url_value.pack()
    url_value.bind("<Button-1>", open_url)
    url_value.config(state=tk.DISABLED)

    status_label = Label(root, text="   ", bg="green", width=2)
    status_label.pack()
    status_labels[state] = status_label

# Start the monitoring in a separate thread
threading.Thread(target=monitor_websites, daemon=True).start()

root.mainloop()
