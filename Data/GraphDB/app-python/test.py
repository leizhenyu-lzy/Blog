import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()


NEO4J_URI=os.getenv('NEO4J_URI')
NEO4J_USERNAME=os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD=os.getenv('NEO4J_PASSWORD')


print(NEO4J_URI)

