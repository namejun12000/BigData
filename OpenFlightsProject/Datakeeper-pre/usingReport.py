import load
import driver
import time
import solve
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 100)

# driver to be used throughout entire application
driver = driver.driver()

# loader used for loading and resetting data
loader = load.Load(driver.driver)

# runs the queries for questions
task = solve.Solution(driver.driver)

def P1():
    # print("*"*50)
    # print("Problem 1")
    # print("*"*50)
    # p1 = input("Enter the Country Name (ex: Iceland, Canada, United State): ")
    # start_time = time.time()
    task.problem1("United States")
    # end_time = time.time()
    # timeTest = end_time - start_time
    # print("Total time:", end_time - start_time, "seconds\n")

def P7():
    # print("*"*50)
    # print("Problem 7")
    # print("*"*50)
    # p7City = input("Enter the first City: ")
    # p7City1 = input("Enter the second City: ")
    # start_time = time.time()
    size = task.problem7("San Francisco", "New York")
    # print(a)
    # end_time = time.time()
    # print("Total time:", end_time - start_time, "seconds\n")
    return len(size)

def P80():
    # print("*"*50)
    # print("Problem 8")
    # print("*"*50)
    # p8City = input("Enter the first City: ")
    # p8City1 = input("Enter the second City: ")
    # p8Stop = int(input("Enter the Stops (find all route less than entered Stops): "))
    # start_time = time.time()
    size = task.problem8("Seattle", "New York", 0)
    # size2 = None
    # end_time = time.time()
    # print("Total time:", end_time - start_time, "seconds\n")
    return len(size)

def P81():
    # print("*"*50)
    # print("Problem 8")
    # print("*"*50)
    # p8City = input("Enter the first City: ")
    # p8City1 = input("Enter the second City: ")
    # p8Stop = int(input("Enter the Stops (find all route less than entered Stops): "))
    # start_time = time.time()
    size = task.problem8("Seattle", "New York", 1)
    # size2 = None
    # end_time = time.time()
    # print("Total time:", end_time - start_time, "seconds\n")
    return len(size)

def P82():
    # print("*"*50)
    # print("Problem 8")
    # print("*"*50)
    # p8City = input("Enter the first City: ")
    # p8City1 = input("Enter the second City: ")
    # p8Stop = int(input("Enter the Stops (find all route less than entered Stops): "))
    # start_time = time.time()
    size = task.problem8("Seattle", "New York", 1)
    # size2 = None
    # end_time = time.time()
    # print("Total time:", end_time - start_time, "seconds\n")
    return len(size)

def stop():
    driver.close()
    return


def main():
    # Question 1
    # print("*"*50)
    # print("Question 1 (Country Name: United States)")
    # print("*"*50)
    # i = 0
    # lst = list()
    # for i in range(10):
    #     start_time = time.time()
    #     P1()
    #     end_time = time.time()
    #     timeTest = end_time - start_time
    #     print(f"Test {i+1}: {timeTest}")
    #     i += 1
    #     lst.append(timeTest)
    # mean = sum(lst) / len(lst)
    # print(f"Average execution times for running 10 times: {mean}")

    # # Question 7
    # print("*"*50)
    # print("Question 7\nDeparture City: San Francisco\nArrival City: New York")
    # print("*"*50)
    # start_time = time.time()
    # record = P7()
    # end_time = time.time()
    # timeTest = end_time - start_time
    # print(f"Execution Time: {timeTest}")
    # print(f"Size of Record: {record}")

    # Question 8
    print("*"*50)
    print("Question 8\nDeparture City: Seattle\nArrival City: New York\nStops: 0, 1, 2")
    print("*"*50)
    # stop 0
    start_time = time.time()
    size0 = P80()
    end_time = time.time()
    timeTest = end_time - start_time
    # stop 1
    start_time1 = time.time()
    size1 = P81()
    end_time1 = time.time()
    timeTest1 = end_time1 - start_time1
    # stop 2
    start_time1 = time.time()
    size2 = P82()
    end_time1 = time.time()
    timeTest2 = end_time1 - start_time1
    # results
    print("Stops 0:")
    print(f"Execution Time: {timeTest}")
    print(f"Size of Record: {size0}")

    print("\nStops 1:")
    print(f"Execution Time: {timeTest1}")
    print(f"Size of Record: {size1}")

    print("\nStops 2:")
    print(f"Execution Time: {timeTest2}")
    print(f"Size of Record: {size2}")

    # exit program
    stop()


if __name__ == '__main__':
    main()

# problems = [stop, P1, P7, P8]
# choice = 1
# while choice:
#     choice = int(input("Enter problem number: "))
#     problems[choice]()
#     stop()
# print(P1())