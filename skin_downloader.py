import sqlite3
from tkinter import *
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import os

# Função para criar o banco de dados
def create_db():
    conn = sqlite3.connect('skins.db')
    cursor = conn.cursor()
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
        ('Jax', 'Divine Staff', 'skins/jax_icon.png', 'skins/Jax Divine Staff.fantome'),
        ('Yasuo', 'NightBringer', 'skins/yasuo_icon.png', 'skins/Yasuo NightBringer.fantome')
    ]
    
    cursor.executemany('''
    INSERT INTO skins (character_name, skin_name, icon_path, download_link)
    VALUES (?, ?, ?, ?)
    ''', skins_data)

    conn.commit()
    conn.close()

# Função para baixar a skin
def download_skin(download_link):
    try:
        response = requests.get(download_link)
        response.raise_for_status()  # Verifica se ocorreu um erro na requisição
        with open('skin_downloaded.fantome', 'wb') as file:
            file.write(response.content)
        messagebox.showinfo("Sucesso", "Skin baixada com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao baixar a skin: {e}")

# Função para criar a interface gráfica
def create_gui():
    root = Tk()
    root.title("Skin Downloader")

    conn = sqlite3.connect('skins.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM skins")
    skins = cursor.fetchall()

    for skin in skins:
        character_name = skin[1]
        skin_name = skin[2]
        icon_path = skin[3]
        download_link = skin[4]

        # Adicionando o ícone
        img = Image.open(icon_path)
        img = img.resize((50, 50), Image.ANTIALIAS)  # Redimensiona a imagem
        icon = ImageTk.PhotoImage(img)

        panel = Frame(root)
        panel.pack(side=TOP, fill=X)

        label_icon = Label(panel, image=icon)
        label_icon.image = icon  # Mantém uma referência à imagem
        label_icon.pack(side=LEFT)

        label_text = Label(panel, text=f"{character_name} - {skin_name}")
        label_text.pack(side=LEFT)

        download_button = Button(panel, text="Baixar", command=lambda link=download_link: download_skin(link))
        download_button.pack(side=RIGHT)

    conn.close()
    root.mainloop()

# Cria o banco de dados e a interface gráfica
create_db()
create_gui()
