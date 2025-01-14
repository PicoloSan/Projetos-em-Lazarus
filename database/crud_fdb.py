import os
import fdb

pasta = os.path.dirname(os.path.abspath(__file__))
pasta = pasta.replace("\\", "/")
firebird = pasta + "/fbembed.dll"

# Defina o caminho para o diretório onde o fbembed.dll ou libfbembed.so está localizado
fdb.load_api(firebird)

# Configurações do banco de dados
db_path = '' + pasta + '/BANCO.FDB'  # Sube para o caminho real do seu banco de dados

# Conexão com o banco de dados
def connect():
    conn = fdb.connect(dsn=db_path, user='SYSDBA', password='masterkey', charset='UTF8',
                       fb_library_name=firebird)
    return conn

# Create - Inserir um novo registro
def create(nome, idade):
    conn = connect()
    cur = conn.cursor()
    
    # Use RETURNING para obter o ID do registro recém-inserido
    cur.execute("INSERT INTO pessoas (nome, idade) VALUES (?, ?) RETURNING id", (nome, idade))
    
    # Captura o ID retornado
    novo_id = cur.fetchone()[0]
    
    conn.commit()
    cur.close()
    conn.close()
    
    print("Registro inserido com sucesso. ID gerado:", novo_id)
    return novo_id  # Retornar o ID gerado, se desejado

# Read - Ler registros
def read():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM pessoas")
    rows = cur.fetchall()
    for row in rows:
        print(f"ID: {row[0]} - Nome: {row[1]} - Idade: {row[2]}")
    cur.close()
    conn.close()

# Update - Atualizar um registro
def update(id, nome, idade):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE pessoas SET nome = ?, idade = ? WHERE id = ?", (nome, idade, id))
    conn.commit()
    cur.close()
    conn.close()
    print("Registro atualizado com sucesso.")

# Delete - Deletar um registro
def delete(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM pessoas WHERE id = ?", (id,))
    conn.commit()
    cur.close()
    conn.close()
    print("Registro deletado com sucesso.")

# Exemplo de uso das funções
create('Maria', 28)  # Criar um novo registro
read()                # Ler registros existentes
update(1, 'João', 35) # Atualizar registro com ID 1
# delete(1)            # Deletar registro com ID 1