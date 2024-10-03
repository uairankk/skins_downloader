import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk
import requests
import os

# Função para baixar a skin
def download_skin(download_link):
    try:
        response = requests.get(download_link)
        response.raise_for_status()  # Verifica se houve um erro na requisição

        # Salva a skin com o nome correto
        skin_name = download_link.split("/")[-1]
        with open(skin_name, 'wb') as f:
            f.write(response.content)
        
        messagebox.showinfo("Download Completo", f"A skin foi baixada: {skin_name}")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Função para carregar as skins do banco de dados e criar a interface
def create_gui():
    # Conectar ao banco de dados
    conn = sqlite3.connect('skins.db')
    cursor = conn.cursor()

    # Criar a janela principal
    root = tk.Tk()
    root.title("Skin Downloader")

    # Criar uma árvore para exibir as skins
    tree = ttk.Treeview(root, columns=('Character', 'Skin'), show='headings')
    tree.heading('Character', text='Personagem')
    tree.heading('Skin', text='Skin')
    tree.pack(fill='both', expand=True)

    # Carregar as skins do banco de dados
    cursor.execute("SELECT * FROM skins")
    skins = cursor.fetchall()

    for skin in skins:
        character_name, skin_name, icon_path, download_link = skin[1:]
        
        # Verifica se o ícone existe
        if os.path.exists(icon_path):
            img = Image.open(icon_path)
            img.thumbnail((50, 50))  # Reduz o tamanho da imagem
            img = ImageTk.PhotoImage(img)

            # Insere a imagem e os dados na árvore
            tree.insert('', 'end', values=(character_name, skin_name))
            tree.image = img  # Manter a referência da imagem
        else:
            messagebox.showwarning("Imagem Não Encontrada", f"Ícone não encontrado: {icon_path}")

    # Adiciona botão de download
    download_button = tk.Button(root, text="Baixar Skin", command=lambda: download_skin(skins[tree.selection()[0]][4]))
    download_button.pack()

    # Inicia o loop da interface gráfica
    root.mainloop()

    # Fecha a conexão
    conn.close()

# Chama a função para criar a interface
if __name__ == "__main__":
    create_gui()
