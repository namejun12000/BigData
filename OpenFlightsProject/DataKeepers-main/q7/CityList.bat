javac -cp $(hadoop classpath) CityList.java CityListMapper.java CityListReducer.java
jar cvf CityList.jar CityList.class CityListMapper.class CityListReducer.class
hadoop jar CityList.jar CityList Seattle "New York" 