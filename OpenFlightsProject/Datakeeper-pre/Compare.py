import load
import driver
import time
import pandas as pd
pd.set_option('display.max_columns', None)
import matplotlib.pyplot as plt
import seaborn as sns
import solve

class Compare:
    def __init__(self, driver):
        self.driver = driver

    def close(self):
        self.driver.close()

    # For compare execute time (Problem 7)
    def problem7_BFS(self, City1, City2):
        with self.driver.session() as session:
            result = session.run('''
                MATCH (start:Airport{City:$City1}), (end:Airport{City:$City2})
                CALL apoc.path.expandConfig(start, {
                    labelFilter:'-Airline', relationshipFilter:'BEGIN_ROUTE>|END_ROUTE>', terminatorNodes:[end], maxLevel:4}) 
                    YIELD path 
                RETURN nodes(path) as Route
            ''', City1=City1, City2=City2).to_df()
            result["Route"] = result["Route"].apply(lambda x: solve.Solution.MapRoutes(self,x))
            result = result.drop_duplicates(subset=['Route'])
            return result

    # For compare execute time (Problem 9)
    # BFS Short (duplicates)
    def problem9_1(self, City, Stops):
        Stops = (Stops + 1) * 2
        with self.driver.session() as session:
            result = session.run('''
                MATCH (airport:Airport) WHERE airport.City = $City
                CALL apoc.path.expandConfig(airport, 
                {maxLevel:$Stops, labelFilter:'>Airport|-Airline',relationshipFilter:'BEGIN_ROUTE>|END_ROUTE>',uniqueness:'NODE_PATH'}) YIELD path
                RETURN last(nodes(path)).City as City, length(path) as Stops
                ''', City=City, Stops=Stops).to_df().drop_duplicates(subset=['City'])
            result["Stops"] = result["Stops"].astype(int)
            result["Stops"] = result["Stops"].apply(lambda x: (x / 2) - 1)
            return result

    # BFS Long (contains duplicates)
    def problem9_2(self, City, Stops):
        Stops = (Stops + 1) * 2
        with self.driver.session() as session:
            result = session.run('''
                MATCH (airport:Airport) WHERE airport.City = $City
                CALL apoc.path.expandConfig(airport, 
                {maxLevel: $Stops, labelFilter:'/Airport|'}) YIELD path
                RETURN last(nodes(path)).City as City, length(path) as Stops
                ''', City=City, Stops=Stops).to_df().drop_duplicates(subset=['City'])
            result["Stops"] = result["Stops"].astype(int)
            result["Stops"] = result["Stops"].apply(lambda x: (x / 2) - 1)
            return result

    # DFS
    def problem9_3(self, City1, City2, Stops):
        Stops = (Stops + 1) * 2
        with self.driver.session() as session:
            result = session.run('''
                MATCH (start:Airport{City:$City1}), (end:Airport{City:$City2})
                CALL apoc.path.expandConfig(start, {
                    labelFilter:'-Airline', relationshipFilter:'BEGIN_ROUTE>|END_ROUTE>', terminatorNodes:[end], maxLevel:$Stops}) 
                    YIELD path 
                RETURN nodes(path) as Route, length(path) as Stops
            ''', City1=City1, City2=City2, Stops=Stops).to_df()
            result["Route"] = result["Route"].apply(lambda x: self.MapRoutes(x))
            result = result.drop_duplicates(subset=['Route'])
            result["Stops"] = result["Stops"].astype(int)
            result["Stops"] = result["Stops"].apply(lambda x: (x / 2) - 1)
            return result

# load driver
driver = driver.driver()

# loader used for loading and resetting data
loader = load.Load(driver.driver)

mainTask = solve.Solution(driver.driver)
task = Compare(driver.driver)

### Compare Problem 7 ###
# input cities
print("Compare Problem 7 Algoritm time complexity\n")
c = input("Enter the first City: ")
c1 = input("Enter the second City: ")
# first
print("Algoritm 1")
start_time = time.time()
mainTask.problem7(c, c1)
end_time = time.time()
first7 = (end_time - start_time)
print("Total time:", end_time - start_time, "seconds\n")
# second
print("Algoritm 2")
start_time = time.time()
task.problem7_BFS(c, c1)
end_time = time.time()
second7 = (end_time - start_time)
print("Total time:", end_time - start_time, "seconds\n")
timeP7 = list()
timeP7.append(first7)
timeP7.append(second7)
algoP7 = ['allShortestPaths', 'apoc.path.expandConfig']
# show graph
plt.figure(figsize=(8,5))
sns.barplot(x=algoP7, y=timeP7)
plt.title("Problem 7\nCompare Algorithm Time Complexity",
          fontdict={'fontweight': 'bold'})
plt.xlabel("Algorithm")
plt.ylabel("Time (sec)")
plt.savefig('Problem7.png')
print("png file created\n")

### Compare Problem 9 ###
# input city
print("Compare Problem 9 Algoritm time complexity\n")
c2 = input("Enter the City: ")
s1 = int(input("Enter the Stops (1 recommended): "))
# first
print("Algoritm 1")
start_time = time.time()
mainTask.problem9(c2, s1)
end_time = time.time()
first9 = (end_time - start_time)
print("Total time:", end_time - start_time, "seconds\n")
# second
print("Algoritm 2")
start_time = time.time()
task.problem9_1(c2, s1)
end_time = time.time()
second9 = (end_time - start_time)
print("Total time:", end_time - start_time, "seconds\n")
# third
print("Algoritm 3")
start_time = time.time()
task.problem9_2(c2, s1)
end_time = time.time()
third9 = (end_time - start_time)
print("Total time:", end_time - start_time, "seconds\n")
timeP9 = list()
timeP9.append(first9)
timeP9.append(second9)
timeP9.append(third9)
algoP9 = ['Config parameters 1', 'Config parameters 2', 'Config parameters 3']
# show graph
plt.figure(figsize=(8,5))
sns.barplot(x=algoP9, y=timeP9)
plt.title("Problem 9\nCompare Algorithm Time Complexity",
          fontdict={'fontweight': 'bold'})
plt.xlabel("Algorithm (apoc.path.expandConfig)")
plt.ylabel("Time (sec)")
plt.savefig('Problem9.png')
print("png file created")
Compare.close(driver)

