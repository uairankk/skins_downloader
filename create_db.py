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
    ('Jax', 'Divine Staff', 'https://github.com/seu_usuario/skins_downloader/raw/main/skins/jax_icon.png', 'https://github.com/seu_usuario/skins_downloader/raw/main/skins/Jax Divine Staff.fantome'),
    ('Yasuo', 'NightBringer', 'https://github.com/seu_usuario/skins_downloader/raw/main/skins/yasuo_icon.png', 'https://github.com/seu_usuario/skins_downloader/raw/main/skins/Yasuo NightBringer.fantome')
]

cursor.executemany('''
INSERT INTO skins (character_name, skin_name, icon_path, download_link)
VALUES (?, ?, ?, ?)
''', skins_data)

# Salvar e fechar a conexão
conn.commit()
conn.close()
