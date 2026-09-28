import time

start = time.perf_counter()

total = 0
for i in range(1_000_000):
    total += i

end = time.perf_counter()

print("Total:", total)
print("Time taken:", end - start, "seconds")