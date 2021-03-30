import sqlalchemy as sql


class MySQL():
    def __init__(self):
        self.credential = None

    def get_credential(self, url='Credentials/credentials.txt'):
        print('[MySQL | MariaDB] Procurando autorização')
        with open(url, 'r', encoding='utf-8') as f:
            self.credential = f.read()

    def con(self):
        print('[MySQL | MariaDB] Conectando')
        db = sql.create_engine('mysql+pymysql://' + self.credential)
        return db
