from db_utils import create_collection
from utils import check_inserted_documents

check_inserted_documents(create_collection("Command"))