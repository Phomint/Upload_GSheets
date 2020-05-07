import sys

user = sys.argv[1]
pw = sys.argv[2]
host = sys.argv[3]
port = sys.argv[4]
db = sys.argv[5]

with open('../Credentials/credentials.txt', 'w') as file:
    file.write(user+':'+pw+'@'+host+':'+port+'/'+db)

print('Sucesso ao Salvar')