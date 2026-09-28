import time
start = time.time()

# Code being measured
time.sleep(2)

end = time.time()
print("Time taken:", end - start, "seconds")