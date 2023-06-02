import driver
import pandas

class Load:
    def __init__(self, driver):
        self.driver = driver

    def clean_data(self):
        # clean airport
        airport = pandas.read_csv('./dirty/airports.csv', header = None)
        airport.columns = ['AirportID', 'Name', 'City','Country', 'IATA','ICAO', 'Latitude','Longitude','Altitude','Timezone', 'DST','TzDatabase','Type','Source']

        # drop unnecessary columns
        cols_airports = ["Altitude", "Source", "Timezone", "Type", "TzDatabase", "DST"]
        airport = airport.drop(cols_airports, axis=1)

        # fill dirty fields
        airport = airport.fillna("N/A")
        airport = airport.replace("-", "N/A")
        airport = airport.replace("\\N", "N/A")
        airport = airport.replace("NAN", "N/A")
        airport = airport.replace("", "N/A")
        airport.to_csv('./clean/airports.csv', index=None)

        # clean airline
        airline = pandas.read_csv('./dirty/airlines.csv', header = None)
        airline.columns = ['AirlineID', 'Name', 'Alias', 'IATA','ICAO',
                    'Callsign','Country','Active']

        # drop unnecessary columns 
        cols_airlines = ("Alias")
        airline = airline.drop(cols_airlines, axis=1)

        # fill dirty fields
        airline = airline.fillna("N/A")
        airline = airline.replace("-", "N/A")
        airline = airline.replace("\\N", "N/A")
        airline = airline.replace("NAN", "N/A")
        airline = airline.replace("", "N/A")
        airline = airline.replace("Unknown", "N/A")
        airline = airline.drop(index=airline.loc[airline.AirlineID == -1].index) # first record is not useful
        airline.to_csv('./clean/airlines.csv', index=None)

        # clean route
        route = pandas.read_csv('./dirty/routes.csv', header = None)
        route.columns = ['Airline','AirlineID','SourceAirport','SourceAirportID',
                        'DestinationAirport','DestinationAirportID',
                        'Codeshare','Stops','Equipment']
        # drop unnecessary columns
        cols_routes = ("Equipment") 
        route = route.drop(cols_routes, axis=1)

        # fill dirty fields
        route = route.fillna("N/A")
        route = route.replace("-", "N/A")
        route = route.replace("\\N", "N/A")
        route = route.replace("NAN", "N/A")
        route = route.replace("", "N/A")
        route['Codeshare'] = route['Codeshare'].replace("N/A","N") # assume invalid codeshare values are 'N'
        route.to_csv('./clean/routes.csv', index=None)

    def create_airports(self):
        with self.driver.session() as session:
            session.run(''' 
                LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MortalNemesis/Flight-Navigator/main/clean/airports.csv' AS line
                CREATE (a:Airport)
                SET a = line
                SET a.AirportID = toInteger(line.AirportID),
                a.Latitude = toFloat(line.Latitude),
                a.Longitude = toFloat(line.Longitude)
            ''')

    def create_airlines(self):
        with self.driver.session() as session:
            session.run(''' 
                LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MortalNemesis/Flight-Navigator/main/clean/airlines.csv' AS line
                CREATE (a:Airline)
                SET a = line
                SET a.AirlineID = toInteger(line.AirlineID)
            ''')

    def create_routes(self):
        with self.driver.session() as session:
            session.run('''
                LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MortalNemesis/Flight-Navigator/main/clean/routes.csv' AS line
                CREATE (r:Route)
                SET r = line
                SET r.AirlineID = toInteger(line.AirlineID),
                r.SourceAirportID = toInteger(line.SourceAirportID),
                r.DestinationAirportID = toInteger(line.DestinationAirportID),
                r.Stops = toInteger(line.Stops)
            ''')

    def create_relations(self):
        with self.driver.session() as session:
            session.run(''' 
                MATCH (r:Route)
                MATCH (a:Airport)
                WHERE a.AirportID = r.SourceAirportID
                MERGE (a)-[:BEGIN_ROUTE]->(r)
            ''')

            session.run('''
                MATCH (r:Route)
                MATCH (a:Airport)
                WHERE a.AirportID = r.DestinationAirportID
                MERGE (r)-[:END_ROUTE]->(a)
            ''')

            session.run('''
                MATCH (r:Route)
                MATCH (a:Airline)
                WHERE a.AirlineID = r.AirlineID
                MERGE (r)-[:FLOWN_BY]->(a)
            ''')

    def create_indexes(self):
        with self.driver.session() as session:
            session.run('''
                CREATE INDEX ap_id
                IF NOT EXISTS 
                FOR (a:Airport) ON (a.AirportID)
            ''')

            session.run('''
                CREATE INDEX al_id 
                IF NOT EXISTS
                FOR (a:Airline) ON (a.AirlineID)
            ''')

            session.run('''
                CREATE INDEX rt_id 
                IF NOT EXISTS
                FOR (r:Route) 
                ON (r.SourceAirportID, 
                    r.DestinationAirportID,
                    r.AirlineID)
            ''')

    # returns unique airport countries
    def get_countries(self):
        with self.driver.session() as session:
            return session.run('''
                    MATCH (a:Airport)
                    RETURN a.Country
                    ORDER BY a.Country ASC
                ''').to_df().drop_duplicates()
    
    # returns unqiue airport cities
    def get_cities(self):
        with self.driver.session() as session:
            return session.run('''
                    MATCH (a:Airport)
                    RETURN a.City
                    ORDER BY a.City ASC
                ''').to_df().drop_duplicates()
