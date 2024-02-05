from utils.db_utils import create_sqlite
from opcua_client_gd import read_tags_from_gd


read_tags_from_gd('Sorting.db',opc="opc.tcp://localhost:4842",mongodb="SortTest", mongocol="sort")