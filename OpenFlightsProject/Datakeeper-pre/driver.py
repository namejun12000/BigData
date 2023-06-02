from neo4j import GraphDatabase

import os
from dotenv import load_dotenv


class driver:

    def __init__(self):
        self.driver = None

        load_dotenv()

        NEO4J_URI = os.getenv("NEO4J_URI", "neo4j+s://9dde27bd.databases.neo4j.io")
        NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
        NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "FEEpR0H7vNUNb5ovse6876F-iKE0Aysh_ser0pXiHX4")

        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
        # self.driver.verify_connectivity()

    def close(self):
        self.driver.close()
        self.driver = None