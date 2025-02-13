import time

myTime = int(input("Enter the amount of seconds here: "))

for x in range(myTime, 0, -1):  
    print(x)
    time.sleep(1)  

print("Time is up!")