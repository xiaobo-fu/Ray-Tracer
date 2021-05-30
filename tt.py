import time
t = time.time()
for i in range(1000 * 1000 * 1000):
    a = 1 + 1
print(time.time() - t)