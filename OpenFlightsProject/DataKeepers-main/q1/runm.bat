javac -cp $(hadoop classpath) QOneM.java QOneMapperM.java QOneReducerM.java
jar cvf QOneM.jar QOneM.class QOneMapperM.class QOneReducerM.class
hadoop jar QOneM.jar QOneM airports.csv output "United States"