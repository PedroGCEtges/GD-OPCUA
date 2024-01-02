from datetime import datetime
import time
from time_normalizer import get_cursor_and_conn, get_first_time_in_interval_from_station_tables, get_first_value_in_interval, get_tables, normalize_timestamps, remove_repeatead_timestamps
from working_cycle import check_piece_status, create_df_for_every_table, filter_rows, generate_intervals_table, set_station_cycle
from delete_tables import delete_tables
from create_tag_tables import create_tag_tables

class StationPiece:
    def __init__(self, cursor, conn, start_date, end_date, piece_status, sensor_entrada, sensor_saida, carac):
        self.sensor_entrada = sensor_entrada
        self.sensor_saida = sensor_saida
        self.conn = conn
        self.cursor = cursor
        self.piece_status = piece_status
        self.start_date = start_date
        self.end_date = end_date
        self.carac = carac
        
    def create_tag_tables_from_db(self):
        create_tag_tables(self.cursor, self.conn)

    def get_tables_created(self):
        return get_tables(self.cursor)
    
    def remove_repeated_timestamps_inner(self):
        tables = self.get_tables_created()
        remove_repeatead_timestamps(tables, self.cursor, self.conn)

    def get_first_time_in_interval_from_station_tables_inner(self, tables):
        return get_first_time_in_interval_from_station_tables(tables, self.cursor, self.start_date, self.end_date)
    
    def get_first_value_in_interval_inner(self, first_time):
        return get_first_value_in_interval(first_time)
    
    def normalize_timestamps_inner(self,tables, first_value):
        normalize_timestamps(tables, self.cursor, self.conn, first_value, self.start_date, self.end_date)

    def set_station_cycle_inner(self):
        return set_station_cycle(self.conn, self.sensor_entrada, self.sensor_saida)

    def create_df_for_every_table_inner(self):
        return create_df_for_every_table(self.cursor, self.conn)
    
    def filter_rows_inner(self,dfs,df):
        return filter_rows(dfs, df)
    
    def generate_intervals_table_inner(self, df):
        generate_intervals_table(df, self.conn)
    
    def check_piece_status_inner(self,df):
        if isinstance(self.piece_status, list):
            sorting = {}
            list_of_piece_status = []
            for i in range(len(self.piece_status)):
                piece = check_piece_status(self.piece_status[i], self.conn, df, self.carac[i])
                list_of_piece_status.append(piece)
            sorting['PecaStatus'] = list_of_piece_status
            return sorting
        else:
            return check_piece_status(self.piece_status, self.conn, df, caracteristica=self.carac)
    
    def run_reprise(self):
        delete_tables(self.cursor)
        self.create_tag_tables_from_db()
        tables = self.get_tables_created()
        self.remove_repeated_timestamps_inner()
        first_time_in_interval = self.get_first_time_in_interval_from_station_tables_inner(tables)
        first_value = self.get_first_value_in_interval_inner(first_time=first_time_in_interval)
        self.normalize_timestamps_inner(tables=tables,first_value=first_value)
        dfs = self.set_station_cycle_inner()
        df = self.create_df_for_every_table_inner()
        filter_df = self.filter_rows_inner(df, dfs)
        self.generate_intervals_table_inner(filter_df)
        return self.check_piece_status_inner(dfs)
    
distPiece = StationPiece(*get_cursor_and_conn("Distribution.db"),'2024-01-01', '2024-12-02', ['G1BG1','G1KF1-1TRAS'], 'B_I5', 'G1MB1', ['Aprovada', 'Rejeitada'])
ppPiece = StationPiece(*get_cursor_and_conn("PickAndPlace.db"),'2023-12-31', '2024-12-01', 'G2BG1', 'G1BG1', 'G2MG1','Tampada')
sortPiece = StationPiece(*get_cursor_and_conn("Sorting.db"),'2023-12-31', '2024-12-01', ['C2GB1','C2GB2','C2GB3'], 'G1BG1', 'C1',['Vermelha','Preta','Metalica'])

# rfid = distPiece.run_reprise()
# tampa = ppPiece.run_reprise()
tipo = sortPiece.run_reprise()

print(tipo)

def calculate_proc_time(d):
    '''Para pickandplace d = tampa['Tampada']'''
    l = []
    for i in d:
        proc_time = (datetime.strptime(i['time_out'], "%H:%M:%S.%f") - datetime.strptime(i['time_in'], "%H:%M:%S.%f")).total_seconds()
        l.append(round(proc_time))
    return l

def create_delivery_time():
    x = []
    l = []
    '''Os time_in de aprovada e rejeitada são os mesmos, pois é o sensor de peça no
        magazine'''
    for i in rfid['Operations'][0]['Aprovada']:
        x.append(datetime.strptime(i['time_in'][2:], '%H:%M:%S.%f'))

    x = sorted(x,key=lambda y: y)

    for i in x:
        l.append(datetime.strftime(i,'%H:%M:%S.%f'))
    return l


