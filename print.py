import urllib.request
import os
import time
url = "http://www.printaya.com/queue.txt"
while True:
    text = urllib.request.urlopen(url).read()
    clean = bytes.decode(text)
    if clean != "stop":
        file = "http://www.printaya.com/media/" + clean
        print("Printing " + clean)
        urllib.request.urlretrieve(file, clean)
        os.startfile(clean, "print")
        time.sleep(5)
