import load
import driver
import time
import solve
import pandas as pd
pd.set_option('display.max_columns', None)

# driver to be used throughout entire application
driver = driver.driver()

# loader used for loading and resetting data
loader = load.Load(driver.driver)
if (int(input("Enter 1 to load data 0 to continue: "))):
    start_time = time.time()
    loader.clean_data()
    loader.create_airports()
    loader.create_airlines()
    loader.create_routes()
    loader.create_relations()
    loader.create_indexes()
    end_time = time.time()
    print("Total time:", end_time - start_time, "seconds")

# runs the queries for questions
task = solve.Solution(driver.driver)

def P1():
    print("*"*50)
    print("Problem 1")
    print("*"*50)
    p1 = input("Enter the Country Name (ex: Iceland, Canada, United State): ")
    start_time = time.time()
    a1 = task.problem1(p1)
    print(len(a1))
    end_time = time.time()
    print(a1)
    print("Total time:", end_time - start_time, "seconds\n")

def P2():
    print("*"*50)
    print("Problem 2")
    print("*"*50)
    p2 = int(input("Enter the number of Stops (0 or 1): "))
    start_time = time.time()
    a2 = task.problem2(p2)
    end_time = time.time()
    print(a2)
    print("Total time:", end_time - start_time, "seconds\n")

def P3():
    print("*"*50)
    print("Problem 3")
    print("*"*50)
    p3 = input("Enter the Codeshare (Y or N): ")
    start_time = time.time()
    a3 = task.problem3(p3)
    end_time = time.time()
    print(a3)
    print("Total time:", end_time - start_time, "seconds\n")

def P4():
    print("*"*50)
    print("Problem 4")
    print("*"*50)
    p4 = input("Enter the Activate (Y or N): ")
    start_time = time.time()
    a4 = task.problem4(p4)
    end_time = time.time()
    print(a4)
    print("Total time:", end_time - start_time, "seconds\n")

def P5():
    print("*"*50)
    print("Problem 5")
    print("*"*50)
    start_time = time.time()
    a5 = task.problem5()
    end_time = time.time()
    print(a5)
    print("Total time:", end_time - start_time, "seconds\n")

def P6():
    print("*"*50)
    print("Problem 6")
    print("*"*50)
    start_time = time.time()
    a6 = task.problem6()
    end_time = time.time()
    print(a6)
    print("Total time:", end_time - start_time, "seconds\n")

def P7():
    print("*"*50)
    print("Problem 7")
    print("*"*50)
    p7City = input("Enter the first City: ")
    p7City1 = input("Enter the second City: ")
    start_time = time.time()
    print(len(task.problem7(p7City,p7City1)))
    end_time = time.time()
    print("Total time:", end_time - start_time, "seconds\n")

def P8():
    print("*"*50)
    print("Problem 8")
    print("*"*50)
    p8City = input("Enter the first City: ")
    p8City1 = input("Enter the second City: ")
    p8Stop = int(input("Enter the Stops (find all route less than entered Stops): "))
    start_time = time.time()
    task.problem8(p8City, p8City1, p8Stop)
    end_time = time.time()
    print("Total time:", end_time - start_time, "seconds\n")

def P9():
    print("*"*50)
    print("Problem 9")
    print("*"*50)
    p9City = input("Enter the City: ")
    p9Stop = int(input("Enter number of Stops: "))
    start_time = time.time()
    print(len(task.problem9(p9City, p9Stop)))
    end_time = time.time()
    print("Total time:", end_time - start_time, "seconds\n")

def P10():
    print("*"*50)
    print("Problem 10")
    print("*"*50)
    p10City = input("Enter the City: ")
    start_time = time.time()
    a10 = task.problem10(p10City)
    end_time = time.time()
    print(len(a10))
    print("Total time:", end_time - start_time, "seconds\n")

def stop():
    driver.close()
    return

#           0     1   2   3   4   5   6   7   8   9   10
problems = [stop, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10]
choice = 1
while choice:
    choice = int(input("Enter problem number: "))
    problems[choice]()
