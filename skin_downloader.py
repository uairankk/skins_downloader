import tkinter as tk
from tkinter import messagebox
import sqlite3
import requests
import os

def download_skin(download_link, skin_name):
    response = requests.get(download_link)
    if response.status_code == 200:
        with open(skin_name + '.zip', 'wb') as f:
            f.write(response.content)
        messagebox.showinfo("Sucesso", f"Skin '{skin_name}' baixada com sucesso!")
    else:
        messagebox.showerror("Erro", "Falha ao baixar a skin.")

def get_skins():
    conn = sqlite3.connect('skins.db')
    cursor = conn.cursor()
    cursor.execute("SELECT character_name, skin_name, icon_path, download_link FROM skins")
    return cursor.fetchall()

def on_skin_click(character_name, skin_name, download_link):
    download_skin(download_link, skin_name)

def create_skin_buttons(root):
    skins = get_skins()
    for character_name, skin_name, icon_path, download_link in skins:
        frame = tk.Frame(root)
        frame.pack(pady=10)

        icon = tk.PhotoImage(file=icon_path)  # Carregar o ícone
        icon_label = tk.Label(frame, image=icon)
        icon_label.image = icon  # Manter uma referência
        icon_label.pack(side=tk.LEFT)

        skin_button = tk.Button(frame, text=f"{character_name} - {skin_name}",
                                command=lambda cn=character_name, sn=skin_name, dl=download_link: on_skin_click(cn, sn, dl))
        skin_button.pack(side=tk.LEFT)

def main():
    root = tk.Tk()
    root.title("Skin Downloader")
    create_skin_buttons(root)
    root.mainloop()

if __name__ == "__main__":
    main()
