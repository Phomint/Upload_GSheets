import pandas as pd
import os.path
import shutil


class Query():
    def __init__(self, query_path):
        '''
        Query is an object that contains a dataframe created by a sql file
        Args:
            query_path (str): the path where is storage a sql file.

        Attributes:
            dataframe (DataFrame): is based on pandas lib
            folder_temp (str): name default to a temporary folder
        '''
        self.dataframe = pd.DataFrame()
        self.query_path = query_path
        self.folder_temp = 'temp'
        self.file = None

    def build_dataframe(self, con):
        '''
        It's a method that acquires a dataframe, connecting to database, executing the query.
        Args:
            con (sqlalchemy.engine): connection with the database
        Raises:
            dataframe (Dataframe): receive the whole file
        '''
        with open(self.query_path, 'r', encoding='utf-8') as line:
            query = line.read()
        print('[MySQL | MariaDB] (Executando) query ' + self.query_path.split('\\')[1])
        self.dataframe = pd.read_sql_query(query, con)

    def to_gdrive(self, sep='\t', extension='.tsv'):
        self.file = self.query_path.split('\\')[1][:-4] + extension
        print('[Master] Criando arquivo temporário')
        if not os.path.exists(self.folder_temp):
            os.makedirs(self.folder_temp)
        print('[Master] (Criando) ' + self.folder_temp + '/' + self.file)
        self.dataframe.to_csv(self.folder_temp + '/' + self.file, sep=sep, index=False)

    def remove_temp(self):
        print('[Master] Excluindo diretório temporário')
        shutil.rmtree(self.folder_temp)

