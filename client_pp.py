from utils.db_utils import create_sqlite
from opcua_client_gd import read_tags_from_gd

read_tags_from_gd(sqlite='PickAndPlace.db',mongodb="PPTest", mongocol="pp",opc="opc.tcp://localhost:4841")