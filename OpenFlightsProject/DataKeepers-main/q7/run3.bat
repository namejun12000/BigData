javac -cp $(hadoop classpath) QSeven3.java QSevenMapper3.java QSevenReducer3.java
jar cvf QSeven3.jar QSeven3.class QSevenMapper3.class QSevenReducer3.class
hadoop jar QSeven3.jar QSeven3 "3726 3577" "8123 7767 7729 3993 3797 3697"