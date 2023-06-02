javac -cp $(hadoop classpath) QSeven1.java QSevenMapper1.java QSevenReducer1.java
jar cvf QSeven1.jar QSeven1.class QSevenMapper1.class QSevenReducer1.class
hadoop jar QSeven1.jar QSeven1