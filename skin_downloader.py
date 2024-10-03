import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import webbrowser
import os

def fetch_skins():
    conn = sqlite3.connect('skins.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM skins")
    skins = cursor.fetchall()
    conn.close()
    return skins

def download_skin(url):
    webbrowser.open(url)

def create_gui():
    skins = fetch_skins()

    root = tk.Tk()
    root.title("Skin Downloader")
    root.geometry("400x300")
    root.resizable(False, False)

    style = ttk.Style()
    style.configure("Treeview", font=("Helvetica", 10))
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
    style.configure("TButton", font=("Helvetica", 10))

    frame = ttk.Frame(root, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)

    # Adicionando um Treeview com imagens
    tree = ttk.Treeview(frame, columns=("Character", "Skin"), show='headings', height=10)
    tree.heading("Character", text="Character")
    tree.heading("Skin", text="Skin")

    # Carregar ícones
    icons = {}
    for skin in skins:
        # Corrigir o caminho do ícone
        icon_filename = os.path.basename(skin[3])  # Pega o nome do arquivo da URL
        icon_path = os.path.join("skins", icon_filename)  # Construindo o caminho corretamente
        
        # Verificar se o arquivo existe
        if os.path.exists(icon_path):
            img = Image.open(icon_path)
            img = img.resize((32, 32), Image.ANTIALIAS)  # Redimensionar a imagem
            icons[skin[1]] = ImageTk.PhotoImage(img)  # Armazenar a imagem
            
            # Inserir os dados e a imagem no Treeview
            tree.insert("", "end", values=(skin[1], skin[2]), tags=(skin[4],))
        else:
            print(f"Ícone não encontrado: {icon_path}")

    # Adicionando a imagem ao Treeview
    for i, skin in enumerate(skins):
        tree.item(i + 1, image=icons[skin[1]])  # Atualizar o item com a imagem

    def on_tree_select(event):
        item = tree.selection()[0]
        url = tree.item(item, "tags")[0]
     
