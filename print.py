import urllib.request
import os
import time
url = "http://www.printaya.com/queue.txt"
while True:
    text = urllib.request.urlopen(url).read()
    clean = bytes.decode(text)
    if clean == "print":
        print("Printing...")
        os.startfile("printaya.pdf", "print")
        time.sleep(5)
