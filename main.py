import tkinter as tk
from tkinter import messagebox

# Datele noastre
catalog_filme = [
    {"id": 1, "titlu": "Inception", "genuri": ["Sci-Fi", "Acțiune", "Thriller"]},
    {"id": 2, "titlu": "The Godfather", "genuri": ["Crimă", "Dramă"]},
    {"id": 3, "titlu": "Interstellar", "genuri": ["Sci-Fi", "Aventură", "Dramă"]},
    {"id": 4, "titlu": "The Matrix", "genuri": ["Sci-Fi", "Acțiune"]},
    {"id": 5, "titlu": "Dune", "genuri": ["Sci-Fi", "Aventură"]},
    {"id": 6, "titlu": "Gladiator", "genuri": ["Acțiune", "Dramă"]}
]

lista_favorite = []

# --- FUNCȚIA DE ADĂUGARE ---
def adauga_la_favorite():
    selectie = lista_vizuala_catalog.curselection()
    
    if not selectie:
        messagebox.showwarning("Atenție", "Te rog să selectezi un film din catalog făcând click pe el!")
        return
    
    index_selectat = selectie[0]
    film_ales = catalog_filme[index_selectat]
    
    if film_ales['id'] not in lista_favorite:
        lista_favorite.append(film_ales['id'])
        # Adăugăm un emoji steluță în fața titlului pentru un aspect mai frumos
        lista_vizuala_favorite.insert(tk.END, f"⭐ {film_ales['titlu']}")
    else:
        messagebox.showinfo("Info", "Acest film este deja în lista ta de favorite.")

# --- CONSTRUIREA INTERFEȚEI RESPONSIVE ---
fereastra = tk.Tk()
fereastra.title("Aplicație Filme - UI Responsiv")
fereastra.geometry("500x550")
fereastra.minsize(400, 400) # Fereastra nu va putea fi făcută mai mică de atât

# SECRETUL RESPONSIVITĂȚII: Configurăm grila să se extindă (weight=1)
fereastra.columnconfigure(0, weight=1) # Coloana principală se lățește la maxim
fereastra.rowconfigure(1, weight=1)    # Rândul cu lista de catalog se întinde pe verticală
fereastra.rowconfigure(4, weight=1)    # Rândul cu lista de favorite se întinde pe verticală

# 1. Titlu Catalog
tk.Label(fereastra, text="🍿 Catalog de Filme:", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, pady=(15, 5), padx=20, sticky="w")

# 2. Container pentru Lista Catalog + Bară de scroll
frame_catalog = tk.Frame(fereastra)
frame_catalog.grid(row=1, column=0, sticky="nsew", padx=20)
frame_catalog.columnconfigure(0, weight=1)
frame_catalog.rowconfigure(0, weight=1)

lista_vizuala_catalog = tk.Listbox(frame_catalog, font=("Segoe UI", 11), activestyle="none", relief="groove")
lista_vizuala_catalog.grid(row=0, column=0, sticky="nsew")

scroll_catalog = tk.Scrollbar(frame_catalog, orient="vertical", command=lista_vizuala_catalog.yview)
scroll_catalog.grid(row=0, column=1, sticky="ns")
lista_vizuala_catalog.config(yscrollcommand=scroll_catalog.set)

# Populăm lista de catalog cu filme
for film in catalog_filme:
    lista_vizuala_catalog.insert(tk.END, f"  {film['titlu']}  |  Genuri: {', '.join(film['genuri'])}")
    
buton_adauga = tk.Button(fereastra, text="➕ ADAUGĂ LA FAVORITE", font=("Segoe UI", 10, "bold"), bg="#4CAF50", fg="white", cursor="hand2", relief="raised", command=adauga_la_favorite)
buton_adauga.grid(row=2, column=0, pady=15, padx=20, sticky="ew")

# 4. Titlu Favorite
tk.Label(fereastra, text="⭐ Filmele tale favorite:", font=("Segoe UI", 12, "bold")).grid(row=3, column=0, pady=(0, 5), padx=20, sticky="w")

# 5. Container pentru Lista Favorite + Bară de scroll
frame_favorite = tk.Frame(fereastra)
frame_favorite.grid(row=4, column=0, sticky="nsew", padx=20, pady=(0, 20))
frame_favorite.columnconfigure(0, weight=1)
frame_favorite.rowconfigure(0, weight=1)

lista_vizuala_favorite = tk.Listbox(frame_favorite, font=("Segoe UI", 11), bg="#f8f9fa", activestyle="none", relief="groove")
lista_vizuala_favorite.grid(row=0, column=0, sticky="nsew")

scroll_fav = tk.Scrollbar(frame_favorite, orient="vertical", command=lista_vizuala_favorite.yview)
scroll_fav.grid(row=0, column=1, sticky="ns")
lista_vizuala_favorite.config(yscrollcommand=scroll_fav.set)

fereastra.mainloop()