catalog_filme = [
    {"id": 1, "titlu": "Inception", "genuri": ["Sci-Fi", "Acțiune", "Thriller"]},
    {"id": 2, "titlu": "The Godfather", "genuri": ["Crimă", "Dramă"]},
    {"id": 3, "titlu": "Interstellar", "genuri": ["Sci-Fi", "Aventură", "Dramă"]},
    {"id": 4, "titlu": "The Matrix", "genuri": ["Sci-Fi", "Acțiune"]}
]

lista_favorite = []

# Funcția 1: Afișează catalogul de filme
def afiseaza_catalog(filme):
    print("\n=== CATALOG DE FILME ===")
    for index, film in enumerate(filme):
        print(f"{index + 1}. {film['titlu']} - Genuri: {', '.join(film['genuri'])}")
    print("\n")

# Funcția 2: Gestionează alegerea utilizatorului
def alege_film_preferat(filme, favorite):
    while True:
        raspuns = input("Introdu numărul filmului tău preferat (sau 'q' pentru a ieși): ")
        
        if raspuns.lower() == 'q':
            print("Ai ieșit din program.")
            break
            
        try:
            alegere_numar = int(raspuns)
            
            # Validăm dacă numărul ales este în lista de filme
            if 1 <= alegere_numar <= len(filme):
                film_ales = filme[alegere_numar - 1]
                
                # Verificăm să nu adăugăm duplicate în favorite
                if film_ales['id'] not in favorite:
                    favorite.append(film_ales['id'])
                
                print(f"\n✅ Ai ales cu succes filmul: {film_ales['titlu']}!")
                print(f"Lista ta de favorite conține acum ID-urile: {favorite}")
                break 
                
            else:
                print(f"❌ Te rog să alegi un număr valid între 1 și {len(filme)}.\n")
                
        except ValueError:
            print("❌ EROARE: Te rog să introduci doar o CIFRĂ (ex: 1, 2, 3).\n")
# Apelăm prima funcție pentru a afișa lista
afiseaza_catalog(catalog_filme)

# Apelăm a doua funcție pentru a prelua opțiunea utilizatorului
alege_film_preferat(catalog_filme, lista_favorite)