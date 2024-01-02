from datetime import datetime, timedelta
import random
import pandas as pd

from test_sqlite.test5_sqlite import converter_segundos, get_cursor_and_conn

def convert_to_plant_simulation_date_format(date):
    formato = "%Y/%m/%d %H:%M:%S.%f"
    return date.strftime(formato)[:-2]

def convert_to_plant_simulation_time_format(date):
    formato = "%H:%M:%S.%f"
    return date.strftime(formato)[:-2]

now = datetime.now()
times = []
MU = []
number = []
Name = []
Attributes = []
attr = []

properties = {"peca_vermelha_tampada": [
        {"Cor":"Vermelha"},
        {"RFID_OK":True},
        {"Metalica":False},
        {"Tampa":True}
    ],
    "peca_metalica_tampada": [
        {"Cor":""},
        {"RFID_OK":True},
        {"Metalica":True},
        {"Tampa":True}
    ],
    "peca_preta_tampada": [
        {"Cor":"Preta"},
        {"RFID_OK":True},
        {"Metalica":False},
        {"Tampa":True}
    ],
    "peca_sem_tampa": [
        {"Cor":""},
        {"RFID_OK":False},
        {"Metalica":False},
        {"Tampa":False}
    ]
}
'''_map = Cor-> 0 = indefinida, -1 = preta, 1 = vermelha
        RFID = Metalica = Tampa -> 0 = nao, 1 = sim

 '''

peca_sem_tampa = {}
peca_sem_tampa["NameofAttribute"] = ["Cor", "RFID", "Metalica", "Tampa", "DistProcTime","PPProcTime","SortProcTime"]
peca_sem_tampa["Value"] = [0, 0, 0, 0, random.randint(0,5), 0, 0]
# peca_sem_tampa["String"] = ["","","",""]

peca_preta_tampada = {}
peca_preta_tampada["NameofAttribute"] = ["Cor", "RFID", "Metalica", "Tampa", "DistProcTime","PPProcTime","SortProcTime"]
peca_preta_tampada["Value"] = [-1, 1, 0, 1,random.randint(0,5),random.randint(0,5),random.randint(0,5) ]
# peca_preta_tampada["String"] = ["Preta","","",""]

peca_metalica_tampada = {}
peca_metalica_tampada["NameofAttribute"] = ["Cor", "RFID", "Metalica", "Tampa","DistProcTime","PPProcTime","SortProcTime"]
peca_metalica_tampada["Value"] = [0, 1,1,1,random.randint(0,5),random.randint(0,5),random.randint(0,5)]
# peca_metalica_tampada["String"] = ["","","",""]

peca_vermelha_tampada = {}
peca_vermelha_tampada["NameofAttribute"] = ["Cor", "RFID", "Metalica", "Tampa","DistProcTime","PPProcTime","SortProcTime"]
peca_vermelha_tampada["Value"] = [1,1,0,1,random.randint(0,5),random.randint(0,5),random.randint(0,5)]
# peca_vermelha_tampada["String"] = ["Vermelha","","",""]

props = []
props.append(peca_metalica_tampada)
props.append(peca_preta_tampada)
props.append(peca_vermelha_tampada)
props.append(peca_sem_tampa)

cursor, conn = get_cursor_and_conn("Teste.db")

def set_df(df, string):
    return df.to_sql(string, conn, if_exists='replace', index=False,
                    dtype={"NameofAttribute": "STRING", "Value": "INTEGER"})
for i in props:
    print(i)
    df = pd.DataFrame(i)
    if i["Value"][1] == 0:
        set_df(df, "propertiesSemTampa")

    elif i["Value"][0] == -1:
        set_df(df,"propertiesPreta")

    elif i["Value"][0] == 1:
        set_df(df, "propertiesVermelha")

    elif i["Value"][2] == 1:
        set_df(df, "propertiesMetalica")

    else:
        print("Erro")   




for i in range(1000):
    peca = random.choice(["peca_vermelha_tampada", "peca_preta_tampada", "peca_sem_tampa","peca_metalica_tampada"])
    # times.append(convert_to_plant_simulation_time_format(now + timedelta(seconds=3*i)))
    times.append( converter_segundos(3*i))
    MU.append(".UserObjects.Peca_Re")
    number.append(1)
    Name.append(peca)
    attr.append('properties')
    Attributes.append(properties[peca])

data_dict = {}
data_dict["DeliveryTime"] = times
data_dict["MU"] = MU
data_dict["Number"] = number
data_dict["Name"] = Name
data_dict["Attributes"] = attr

df = pd.DataFrame(data_dict)
df.to_sql('Teste', conn, if_exists='replace', index=False,dtype={"DeliveryTime": "TIME"})


properties_format = {}
properties_format['attr'] = Attributes
test = {}
cor = []
rfid = []
metalica = []
tampa = []
for i in properties_format["attr"]:
    cor.append(i[0]["Cor"])
    rfid.append(i[1]["RFID_OK"])
    metalica.append(i[2]["Metalica"])
    tampa.append(i[3]["Tampa"])

test["Cor"] = cor
test["RFID"] = rfid
test["Metalica"] = metalica
test["Tampa"] = tampa

dp = pd.DataFrame(test)
dp.to_sql('properties', conn, if_exists='replace', index=False,dtype={"RFID": "BOOLEAN", "Metalica": "BOOLEAN", "Tampa": "BOOLEAN"})
print(dp.head())