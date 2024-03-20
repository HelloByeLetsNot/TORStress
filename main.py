import threading
import tkinter as tk
from ttkthemes import ThemedTk
import requests
from torpy.http.requests import TorRequests

class StressTestWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title("Website Stress Test")

        self.url_label = tk.Label(self, text="Enter website URL(s) separated by commas:")
        self.url_label.pack()

        self.url_entry = tk.Entry(self)
        self.url_entry.pack()

        self.num_requests_label = tk.Label(self, text="Number of requests per URL:")
        self.num_requests_label.pack()

        self.num_requests_entry = tk.Entry(self)
        self.num_requests_entry.insert(0, "10")
        self.num_requests_entry.pack()

        self.start_button = tk.Button(self, text="Start Test", command=self.start_test)
        self.start_button.pack()

        self.status_text = tk.StringVar()
        self.status_label = tk.Label(self, textvariable=self.status_text)
        self.status_label.pack()

    def start_test(self):
        urls = self.url_entry.get().split(",")
        try:
            num_requests = int(self.num_requests_entry.get())
        except ValueError:
            self.status_text.set("Invalid number of requests. Please enter an integer.")
            return

        self.status_text.set(f"Sending {num_requests} requests to each URL...")

        def send_requests(url):
            with TorRequests() as tor_requests:
                for _ in range(num_requests):
                    try:
                        response = tor_requests.get(url)
                        if response.status_code == 200:
                            self.status_text.set(f"Request to {url} successful (status code: {response.status_code})")
                        else:
                            self.status_text.set(f"Request to {url} failed (status code: {response.status_code})")
                    except requests.exceptions.RequestException as e:
                        self.status_text.set(f"Request error for {url}: {e}")

        threads = []
        for url in urls:
            thread = threading.Thread(target=send_requests, args=(url,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        self.status_text.set("Stress test completed.")

if __name__ == "__main__":
    root = ThemedTk(theme="equilux")  # Set your desired theme here
    app = StressTestWindow(root)
    app.pack()
    root.mainloop()