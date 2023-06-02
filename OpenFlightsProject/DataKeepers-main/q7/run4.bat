javac -cp $(hadoop classpath) QSeven4.java QSevenMapper4.java QSevenReducer4.java
jar cvf QSeven4.jar QSeven4.class QSevenMapper4.class QSevenReducer4.class
hadoop jar QSeven4.jar QSeven4 2