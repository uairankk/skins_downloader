import sqlite3

# Conectar ao banco de dados (ou criar um novo se não existir)
conn = sqlite3.connect('skins.db')
cursor = conn.cursor()

# Criar a tabela de skins
cursor.execute('''
CREATE TABLE IF NOT EXISTS skins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_name TEXT NOT NULL,
    skin_name TEXT NOT NULL,
    icon_path TEXT NOT NULL,
    download_link TEXT NOT NULL
)
''')

# Adicionar skins de exemplo ao banco de dados
skins_data = [
    ('Jax', 'Divine Staff', 'skins/jax_icon.png', 'https://github.com/uairankk/skins_downloader/raw/main/skins/Jax%20Divine%20Staff.fantome'),
    ('Yasuo', 'NightBringer', 'skins/yasuo_icon.png', 'https://github.com/uairankk/skins_downloader/raw/main/skins/Yasuo%20NightBringer.fantome')
]

cursor.executemany('''
INSERT INTO skins (character_name, skin_name, icon_path, download_link)
VALUES (?, ?, ?, ?)
''', skins_data)

# Salvar e fechar a conexão
conn.commit()
conn.close()
