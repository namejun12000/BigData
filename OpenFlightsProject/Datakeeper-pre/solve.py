import driver


class Solution:
    def __init__(self, driver):
        self.driver = driver

    def close(self):
        self.driver.close()

    # Given a country X, provide a list of airports operating in country X.
    def problem1(self, Country):
        with self.driver.session() as session:
            result = session.run('''
                MATCH (p:Airport) 
                WHERE p.Country = $Country
                RETURN p.AirportID, p.Name, p.City, p.Country
            ''', Country=Country).to_df
        print(result)
        # return result

    # Given a number of stops X, provide a list of airlines having X stops.
    def problem2(self, Stops):
        with self.driver.session() as session:
            result = session.run('''
                MATCH (o:Route)-[r:FLOWN_BY]->(l:Airline)
                WHERE o.AirlineID = l.AirlineID AND
	                o.Stops = $Stops
                RETURN DISTINCT l.AirlineID, l.Name, o.Stops
                ORDER BY l.AirlineID
            ''', Stops=Stops).to_df()
        return result

    # Given a code share X for airlines, provide a list of airlines operating with code share X.
    def problem3(self, Codeshare):
        with self.driver.session() as session:
            result = session.run('''
                MATCH (o:Route)-[r:FLOWN_BY]->(l:Airline)
                WHERE o.AirlineID = l.AirlineID AND o.Codeshare = $Codeshare
                RETURN DISTINCT l.AirlineID, l.Name, o.Codeshare
            ''', Codeshare=Codeshare).to_df()
        return result

    # Given the option to display active airlines, provide a list of active airlines if selected.
    def problem4(self, Active):
        with self.driver.session() as session:
            result = session.run('''
                MATCH (l:Airline)
                WHERE l.Active = $Active
                RETURN DISTINCT l.AirlineID, l.Name, l.Active
            ''', Active=Active).to_df()
        return result

    # Given the option to display the country or territory with the highest number of airports, provide the country or territory with the highest number of airports if
    # selected.
    def problem5(self):
        with self.driver.session() as session:
            result = session.run('''
                MATCH (p:Airport)
                RETURN p.Country, COUNT(*) as Count
                ORDER BY Count DESC
                LIMIT 10
            ''').to_df()
        return result

    # Given a number of cities X, provide the top X cities with the most incoming and outgoing airlines.
    def problem6(self, limit: int):
        with self.driver.session() as session:
            result = session.run('''
                MATCH ()-[incoming]->(n)-[outgoing]->() 
                WITH n, incoming, outgoing
                WHERE n.City IS NOT NULL
                RETURN n.City, 
                    COUNT(DISTINCT incoming) AS Incoming, 
                    COUNT(DISTINCT outgoing) as Outgoing, 
                    COUNT(DISTINCT incoming) + COUNT(DISTINCT outgoing) as Total
                ORDER BY Total desc
                LIMIT $limit
            ''', limit=limit).to_df()
        return result

    # Given two cities X and Y, provide a list of routes connecting cities X and Y.
    def problem7(self, City1, City2):
        with self.driver.session() as session:
            result = session.run('''
                    MATCH PATH=allShortestPaths((p:Airport{City: $City1})-[*..4]->
                    (p1:Airport{City: $City2}))
                    RETURN nodes(PATH) as Route
                ''', City1=City1, City2=City2).to_df()
            result["Route"] = result["Route"].apply(lambda x: self.MapRoutes(x))
            result = result.drop_duplicates(subset=['Route'])
        return result
        # return result

    # Given two cities X and Y and a number of stops Z, provide a list of routes connecting cities X and Y with less than Z stops.
    def problem8(self, City1, City2, Stops):
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

    def MapRoutes(self, route):
        result = ""
        for node in route:
            n = dict(node)
            if "SourceAirportID" in n:
                # we've found a route
                temp = n['Airline'] + ': ' + n['SourceAirport'] + ' ' + str(n['SourceAirportID']) + ' -> ' + n[
                    'DestinationAirport'] + ' ' + str(n['DestinationAirportID']) + ' '
                result = result + temp
        return result

    # Given a city X and number of stops Y, provide a list of cities that can be reached from X within Y stops.
    def problem9(self, City, Stops):
        Stops = (Stops + 1) * 2
        with self.driver.session() as session:
            result = session.run('''
                    MATCH (airport:Airport) WHERE airport.City = $City
                    CALL apoc.path.expandConfig(airport, 
                        {maxLevel: $Stops, labelFilter:'>Airport|-Airline',relationshipFilter:'BEGIN_ROUTE>|END_ROUTE>',uniqueness:'NODE_LEVEL'}) YIELD path
                    RETURN last(nodes(path)).City as City, length(path) as Stops;
                ''', City=City, Stops=Stops).to_df().drop_duplicates(subset=['City'])
            result["Stops"] = result["Stops"].astype(int)
            result["Stops"] = result["Stops"].apply(lambda x: (x / 2) - 1)
            return result

    # Given all routes, provide the transitive closure of the graph of all routes.
    def problem10(self, City):
        with self.driver.session() as session:
            result = session.run('''
                MATCH PATH=(p:Airport)-[:BEGIN_ROUTE]->(o:Route)-[:END_ROUTE]->(p1:Airport)
                WITH *, point({ longitude: p.Longitude, latitude: p.Latitude }) AS source,
                 point({ longitude: p1.Longitude, latitude: p1.Latitude }) AS destination
                WHERE o.AirlineID IS NOT NULL AND p.City = $City
                RETURN round(point.distance(source, destination))/1000 AS travelDistance, p.City, p.Name,
                 p1.City, p1.Name, o.AirlineID
                ORDER BY travelDistance ASC 
            ''', City=City).to_df()
            return result