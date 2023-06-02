javac -cp $(hadoop classpath) QOne.java QOneMapper.java QOneReducer.java
jar cvf QOne.jar QOne.class QOneMapper.class QOneReducer.class
hadoop jar QOne.jar QOne airports.csv output "United States"