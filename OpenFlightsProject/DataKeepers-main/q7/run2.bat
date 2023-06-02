javac -cp $(hadoop classpath) QSeven2.java QSevenMapper2.java QSevenReducer2.java
jar cvf QSeven2.jar QSeven2.class QSevenMapper2.class QSevenReducer2.class
hadoop jar QSeven2.jar QSeven2 1 "3726 3577" "8123 7767 7729 3993 3797 3697"