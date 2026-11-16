import sys
import json
import hashlib
import os
import math
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QStackedWidget, 
                             QMessageBox, QScrollArea, QFrame, QTabWidget, 
                             QComboBox, QGridLayout)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

USERS_FILE = 'users.json'
MOVIES_FILE = 'movies.json'

# ==========================================
# 1. GESTIUNEA UTILIZATORILOR
# ==========================================
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    users = load_users()
    if username in users:
        return False  
    
    users[username] = {
        "password": hash_password(password),
        "favorites": [],
        "unfavorites": []
    }
    save_users(users)
    return True

def verify_user(username, password):
    users = load_users()
    if username in users and users[username]["password"] == hash_password(password):
        return username
    return None

def get_user_preferences(username):
    users = load_users()
    if username in users:
        return users[username].get("favorites", []), users[username].get("unfavorites", [])
    return [], []

def add_preference(username, movie_id, status):
    users = load_users()
    if username in users:
        if movie_id in users[username].get("favorites", []):
            users[username]["favorites"].remove(movie_id)
        if movie_id in users[username].get("unfavorites", []):
            users[username]["unfavorites"].remove(movie_id)
        
        if status == 'favorite':
            users[username].setdefault("favorites", []).append(movie_id)
        elif status == 'unfavorite':
            users[username].setdefault("unfavorites", []).append(movie_id)
        
        save_users(users)

# ==========================================
# 2. GESTIUNEA CATALOGULUI DE FILME
# ==========================================
def load_movies():
    existing_movies = []
    if os.path.exists(MOVIES_FILE):
        with open(MOVIES_FILE, 'r', encoding='utf-8') as f:
            try:
                existing_movies = json.load(f)
            except:
                pass
                
    # Verificăm dacă avem deja un catalog extins (peste 100 de filme)
    if len(existing_movies) > 100:
        return existing_movies

    # Generarea unui catalog extins (150+ filme) dacă nu există
    raw_movie_data = [
        # Acțiune & Aventură
        ("The Dark Knight", "Acțiune", 2008), ("Inception", "Acțiune", 2010), ("The Matrix", "Acțiune", 1999), 
        ("Gladiator", "Acțiune", 2000), ("Mad Max: Fury Road", "Acțiune", 2015), ("John Wick", "Acțiune", 2014), 
        ("Die Hard", "Acțiune", 1988), ("Terminator 2: Judgment Day", "Acțiune", 1991), ("Avengers: Endgame", "Acțiune", 2019),
        ("Jurassic Park", "Aventură", 1993), ("Indiana Jones and the Raiders of the Lost Ark", "Aventură", 1981), 
        ("Pirates of the Caribbean: The Curse of the Black Pearl", "Aventură", 2003), ("Back to the Future", "Aventură", 1985),
        ("The Lord of the Rings: The Fellowship of the Ring", "Aventură", 2001), ("The Lord of the Rings: The Two Towers", "Aventură", 2002),
        ("The Lord of the Rings: The Return of the King", "Aventură", 2003), ("Spider-Man: No Way Home", "Acțiune", 2021),
        ("Léon: The Professional", "Acțiune", 1994), ("V for Vendetta", "Acțiune", 2005), ("Kill Bill: Vol. 1", "Acțiune", 2003),
        ("Kill Bill: Vol. 2", "Acțiune", 2004), ("Casino Royale", "Acțiune", 2006), ("Mission: Impossible - Fallout", "Acțiune", 2018),
        ("Logan", "Acțiune", 2017), ("Batman Begins", "Acțiune", 2005), ("The Dark Knight Rises", "Acțiune", 2012),
        
        # Science-Fiction & Fantasy
        ("Interstellar", "Science-Fiction", 2014), ("Avatar", "Science-Fiction", 2009), ("Blade Runner 2049", "Science-Fiction", 2017),
        ("Dune", "Science-Fiction", 2021), ("Alien", "Science-Fiction", 1979), ("Aliens", "Science-Fiction", 1986),
        ("The Terminator", "Science-Fiction", 1984), ("Arrival", "Science-Fiction", 2016), ("The Martian", "Science-Fiction", 2015),
        ("Ex Machina", "Science-Fiction", 2014), ("Star Wars: Episode IV - A New Hope", "Science-Fiction", 1977),
        ("Star Wars: Episode V - The Empire Strikes Back", "Science-Fiction", 1980), ("Gravity", "Science-Fiction", 2013),
        ("Harry Potter and the Sorcerer's Stone", "Fantasy", 2001), ("Harry Potter and the Deathly Hallows: Part 2", "Fantasy", 2011),
        ("Pan's Labyrinth", "Fantasy", 2006), ("The Hobbit: An Unexpected Journey", "Fantasy", 2012), ("Avatar: The Way of Water", "Science-Fiction", 2022),
        
        # Dramă
        ("The Shawshank Redemption", "Dramă", 1994), ("Forrest Gump", "Dramă", 1994), ("Fight Club", "Dramă", 1999),
        ("The Godfather", "Dramă", 1972), ("The Godfather: Part II", "Dramă", 1974), ("Schindler's List", "Dramă", 1993),
        ("Joker", "Dramă", 2019), ("The Green Mile", "Dramă", 1999), ("12 Angry Men", "Dramă", 1957),
        ("Good Will Hunting", "Dramă", 1997), ("Requiem for a Dream", "Dramă", 2000), ("American Beauty", "Dramă", 1999),
        ("A Beautiful Mind", "Dramă", 2001), ("The Pursuit of Happyness", "Dramă", 2006), ("There Will Be Blood", "Dramă", 2007),
        ("No Country for Old Men", "Dramă", 2007), ("Gran Torino", "Dramă", 2008), ("Dead Poets Society", "Dramă", 1989),
        ("Catch Me If You Can", "Dramă", 2002), ("The Truman Show", "Dramă", 1998), ("Rocky", "Dramă", 1976),
        ("Braveheart", "Dramă", 1995), ("Million Dollar Baby", "Dramă", 2004), ("Slumdog Millionaire", "Dramă", 2008),
        
        # Thriller, Mister & Crimă
        ("Pulp Fiction", "Crimă", 1994), ("Se7en", "Thriller", 1995), ("The Silence of the Lambs", "Thriller", 1991),
        ("The Prestige", "Mister", 2006), ("Shutter Island", "Mister", 2010), ("Gone Girl", "Mister", 2014),
        ("Knives Out", "Mister", 2019), ("Parasite", "Thriller", 2019), ("Prisoners", "Thriller", 2013),
        ("Zodiac", "Mister", 2007), ("The Departed", "Crimă", 2006), ("Goodfellas", "Crimă", 1990),
        ("The Usual Suspects", "Mister", 1995), ("Memento", "Mister", 2000), ("Scarface", "Crimă", 1983),
        ("Reservoir Dogs", "Crimă", 1992), ("Fargo", "Crimă", 1996), ("Nightcrawler", "Thriller", 2014),
        ("Snatch", "Crimă", 2000), ("Heat", "Crimă", 1995), ("L.A. Confidential", "Mister", 1997),
        ("Sicario", "Thriller", 2015), ("The Sixth Sense", "Mister", 1999), ("Mystic River", "Mister", 2003),
        
        # Horror & Psihologic
        ("The Shining", "Horror", 1980), ("Psycho", "Horror", 1960), ("The Conjuring", "Horror", 2013),
        ("The Exorcist", "Horror", 1973), ("Halloween", "Horror", 1978), ("A Nightmare on Elm Street", "Horror", 1984),
        ("Hereditary", "Horror", 2018), ("Get Out", "Psihologic", 2017), ("Black Swan", "Psihologic", 2010),
        ("Split", "Psihologic", 2016), ("Donnie Darko", "Psihologic", 2001), ("A Clockwork Orange", "Psihologic", 1971),
        ("The Thing", "Horror", 1982), ("It", "Horror", 2017), ("Scream", "Horror", 1996),
        ("Saw", "Horror", 2004), ("The Ring", "Horror", 2002), ("Sinister", "Horror", 2012),
        
        # Comedie & Romantic
        ("The Hangover", "Comedie", 2009), ("Superbad", "Comedie", 2007), ("Dumb and Dumber", "Comedie", 1994),
        ("Groundhog Day", "Comedie", 1993), ("Step Brothers", "Comedie", 2008), ("Titanic", "Romantic", 1997),
        ("Pride & Prejudice", "Romantic", 2005), ("La La Land", "Romantic", 2016), ("The Notebook", "Romantic", 2004),
        ("Casablanca", "Romantic", 1942), ("Crazy, Stupid, Love.", "Romantic", 2011), ("Silver Linings Playbook", "Romantic", 2012),
        ("500 Days of Summer", "Romantic", 2009), ("Amélie", "Romantic", 2001), ("Before Sunrise", "Romantic", 1995),
        ("The Grand Budapest Hotel", "Comedie", 2014), ("Tropic Thunder", "Comedie", 2008), ("Anchorman", "Comedie", 2004),
        ("Borat", "Comedie", 2006), ("Shaun of the Dead", "Comedie", 2004), ("Hot Fuzz", "Comedie", 2007),
        
        # Animație
        ("The Lion King", "Animație", 1994), ("Spider-Man: Into the Spider-Verse", "Animație", 2018), 
        ("Spirited Away", "Animație", 2001), ("Toy Story", "Animație", 1995), ("WALL-E", "Animație", 2008),
        ("Coco", "Animație", 2017), ("Inside Out", "Animație", 2015), ("Up", "Animație", 2009),
        ("Finding Nemo", "Animație", 2003), ("Shrek", "Animație", 2001), ("How to Train Your Dragon", "Animație", 2010),
        ("Ratatouille", "Animație", 2007), ("The Incredibles", "Animație", 2004), ("Monsters, Inc.", "Animație", 2001),
        ("Princess Mononoke", "Animație", 1997), ("My Neighbor Totoro", "Animație", 1988),
        
        # Istoric & Biografic
        ("The Wolf of Wall Street", "Biografic", 2013), ("Oppenheimer", "Biografic", 2023), 
        ("The Social Network", "Biografic", 2010), ("Bohemian Rhapsody", "Biografic", 2018), 
        ("Axe Hacksaw Ridge", "Istoric", 2016), ("1917", "Istoric", 2019), ("Dunkirk", "Istoric", 2017),
        ("The Pianist", "Istoric", 2002), ("Apollo 13", "Biografic", 1995), ("The Imitation Game", "Biografic", 2014),
        ("The Theory of Everything", "Biografic", 2014), ("Lincoln", "Istoric", 2012), ("The King's Speech", "Istoric", 2010)
    ]
    
    extended_movies = []
    for i, (title, genre, year) in enumerate(raw_movie_data, start=1):
        extended_movies.append({
            "id": i,
            "title": title,
            "genre": genre,
            "year": year
        })
        
    with open(MOVIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(extended_movies, f, indent=4, ensure_ascii=False)
    
    return extended_movies

# ==========================================
# 3. ALGORITMI RECOMANDARE ȘI TOP
# ==========================================
def get_user_similarities(target_username, users, movie_ids):
    target_data = users.get(target_username, {})
    target_favs = set(target_data.get("favorites", []))
    target_unfavs = set(target_data.get("unfavorites", []))
    
    if not target_favs and not target_unfavs:
        return {}, []

    def build_vector(username):
        vec = []
        u_favs = set(users[username].get("favorites", []))
        u_unfavs = set(users[username].get("unfavorites", []))
        for mid in movie_ids:
            if mid in u_favs:
                vec.append(1)
            elif mid in u_unfavs:
                vec.append(-1)
            else:
                vec.append(0)
        return vec

    target_vec = build_vector(target_username)
    
    def cosine_similarity(v1, v2):
        dot_product = sum(x * y for x, y in zip(v1, v2))
        norm1 = math.sqrt(sum(x * x for x in v1))
        norm2 = math.sqrt(sum(x * x for x in v2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot_product / (norm1 * norm2)

    similarities = {}
    ranked_users = []
    
    for user, data in users.items():
        if user == target_username:
            continue
        user_vec = build_vector(user)
        sim = cosine_similarity(target_vec, user_vec)
        if sim != 0:
            similarities[user] = sim
            ranked_users.append({"username": user, "similarity": round(sim * 100, 2)})
            
    ranked_users.sort(key=lambda x: x["similarity"], reverse=True)
    return similarities, ranked_users

def get_collaborative_recommendations(target_username):
    users = load_users()
    movies = load_movies()
    movie_ids = [m["id"] for m in movies]
    movie_dict = {m["id"]: m for m in movies}
    
    similarities, ranked_users = get_user_similarities(target_username, users, movie_ids)
    
    target_data = users.get(target_username, {})
    target_evaluated = set(target_data.get("favorites", [])) | set(target_data.get("unfavorites", []))
    
    recommendations_scores = []
    
    if similarities:
        for mid in movie_ids:
            if mid in target_evaluated:
                continue
                
            score_numerator = 0.0
            score_denominator = 0.0
            
            for user, sim in similarities.items():
                u_favs = set(users[user].get("favorites", []))
                u_unfavs = set(users[user].get("unfavorites", []))
                
                if mid in u_favs:
                    score_numerator += sim * 1
                    score_denominator += abs(sim)
                elif mid in u_unfavs:
                    score_numerator += sim * (-1)
                    score_denominator += abs(sim)
                    
            if score_denominator > 0 and score_numerator > 0:
                predicted_score = score_numerator / score_denominator
                recommendations_scores.append({
                    "movie": movie_dict[mid],
                    "score": round(predicted_score * 100, 2),
                    "reason": "Recomandat deoarece utilizatorii cu preferințe asemănătoare au apreciat acest film."
                })
                
    recommendations_scores.sort(key=lambda x: x["score"], reverse=True)
    return recommendations_scores[:20], ranked_users

def get_global_top():
    users = load_users()
    movies = load_movies()
    
    top_list = []
    for m in movies:
        mid = m["id"]
        favs = sum(1 for u in users.values() if mid in u.get("favorites", []))
        unfavs = sum(1 for u in users.values() if mid in u.get("unfavorites", []))
        total_votes = favs + unfavs
        
        if total_votes > 0:
            appreciation_pct = (favs / total_votes) * 100
            if favs > 0:
                top_list.append({
                    "movie": m,
                    "favs": favs,
                    "unfavs": unfavs,
                    "pct": round(appreciation_pct, 1)
                })
                
    # Sortăm descrescător după numărul de aprecieri, apoi după procent
    top_list.sort(key=lambda x: (x["favs"], x["pct"]), reverse=True)
    return top_list


# ==========================================
# 4. INTERFAȚA GRAFICĂ (GUI)
# ==========================================
class MovieApp(QWidget):
    def __init__(self):
        super().__init__()
        self.current_user = None
        
        # Dicționar pentru stocarea referințelor butoanelor, evitând recrearea lor la fiecare click
        self.movie_card_buttons = {} 
        self.all_movies_data = []
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Recomandări Filme PRO")
        self.resize(1000, 850)
        self.setStyleSheet("background-color: #1e1e2e; color: #cdd6f4; font-family: 'Segoe UI', Arial;")
        
        self.layout = QVBoxLayout()
        self.stacked_widget = QStackedWidget()
        
        self.login_widget = self.create_login_ui()
        self.main_widget = self.create_main_ui()
        
        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.main_widget)
        
        self.layout.addWidget(self.stacked_widget)
        self.setLayout(self.layout)
        
    def create_login_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel("🎬 Autentificare")
        title.setFont(QFont("Arial", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nume utilizator")
        self.username_input.setStyleSheet("padding: 12px; border-radius: 6px; background: #313244; border: 1px solid #45475a; font-size: 14px;")
        self.username_input.setFixedWidth(320)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Parolă")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 12px; border-radius: 6px; background: #313244; border: 1px solid #45475a; font-size: 14px;")
        self.password_input.setFixedWidth(320)
        
        login_btn = QPushButton("Intră în cont")
        login_btn.setFixedWidth(320)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet("padding: 12px; background-color: #89b4fa; color: #11111b; font-weight: bold; border-radius: 6px; font-size: 14px;")
        login_btn.clicked.connect(self.handle_login)
        
        signup_btn = QPushButton("Creează cont")
        signup_btn.setFixedWidth(320)
        signup_btn.setCursor(Qt.PointingHandCursor)
        signup_btn.setStyleSheet("padding: 12px; background-color: #a6e3a1; color: #11111b; font-weight: bold; border-radius: 6px; font-size: 14px;")
        signup_btn.clicked.connect(self.handle_signup)
        
        layout.addWidget(title)
        layout.addSpacing(40)
        layout.addWidget(self.username_input, alignment=Qt.AlignCenter)
        layout.addSpacing(15)
        layout.addWidget(self.password_input, alignment=Qt.AlignCenter)
        layout.addSpacing(25)
        layout.addWidget(login_btn, alignment=Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(signup_btn, alignment=Qt.AlignCenter)
        
        widget.setLayout(layout)
        return widget
        
    def create_main_ui(self):
        widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        
        # HEADER
        header_layout = QHBoxLayout()
        self.welcome_label = QLabel("Salut!")
        self.welcome_label.setFont(QFont("Arial", 18, QFont.Bold))
        
        logout_btn = QPushButton("Deconectare")
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.setStyleSheet("padding: 8px 16px; background-color: #f38ba8; color: #11111b; border-radius: 6px; font-weight: bold;")
        logout_btn.clicked.connect(self.handle_logout)
        
        header_layout.addWidget(self.welcome_label)
        header_layout.addStretch()
        header_layout.addWidget(logout_btn)
        
        self.main_layout.addLayout(header_layout)
        self.main_layout.addSpacing(10)
        
        # TABURI
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab { background: #313244; color: #cdd6f4; padding: 12px 25px; border-top-left-radius: 6px; border-top-right-radius: 6px; font-weight: bold; font-size: 14px;}
            QTabBar::tab:selected { background: #89b4fa; color: #11111b; }
            QTabWidget::pane { border: 2px solid #45475a; border-radius: 6px; border-top-left-radius: 0; background: #1e1e2e;}
        """)
        self.tabs.currentChanged.connect(self.on_tab_changed)
        
        # TAB 1: CATALOG FILME
        self.tab_catalog = QWidget()
        self.setup_catalog_tab()
        
        # TAB 2: RECOMANDĂRI
        self.tab_recommendations = QWidget()
        self.setup_recommendations_tab()
        
        # TAB 3: TOP GLOBAL
        self.tab_top = QWidget()
        self.setup_top_tab()
        
        self.tabs.addTab(self.tab_catalog, "📚 Catalog Filme")
        self.tabs.addTab(self.tab_recommendations, "✨ Recomandări pentru Tine")
        self.tabs.addTab(self.tab_top, "🏆 Top Global")
        
        self.main_layout.addWidget(self.tabs)
        widget.setLayout(self.main_layout)
        return widget

    def setup_catalog_tab(self):
        layout = QVBoxLayout()
        
        # Bara de unelte pentru căutare și filtrare
        toolbar = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Caută după titlu...")
        self.search_input.setStyleSheet("padding: 8px; border-radius: 4px; background: #313244; border: 1px solid #45475a;")
        self.search_input.textChanged.connect(self.filter_catalog)
        
        self.genre_combo = QComboBox()
        self.genre_combo.setStyleSheet("padding: 8px; border-radius: 4px; background: #313244; border: 1px solid #45475a;")
        self.genre_combo.currentIndexChanged.connect(self.filter_catalog)
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Implicit", "A-Z", "Z-A", "An (Nou-Vechi)", "An (Vechi-Nou)"])
        self.sort_combo.setStyleSheet("padding: 8px; border-radius: 4px; background: #313244; border: 1px solid #45475a;")
        self.sort_combo.currentIndexChanged.connect(self.filter_catalog)
        
        self.view_combo = QComboBox()
        self.view_combo.addItems(["Toate filmele", "Filme Favorite ❤️", "Filme Neplăcute 👎", "Neevaluate"])
        self.view_combo.setStyleSheet("padding: 8px; border-radius: 4px; background: #313244; border: 1px solid #45475a;")
        self.view_combo.currentIndexChanged.connect(self.filter_catalog)
        
        toolbar.addWidget(self.search_input, 2)
        toolbar.addWidget(self.genre_combo, 1)
        toolbar.addWidget(self.sort_combo, 1)
        toolbar.addWidget(self.view_combo, 1)
        
        layout.addLayout(toolbar)
        
        # Scroll Area pentru filme
        self.scroll_catalog = QScrollArea()
        self.scroll_catalog.setWidgetResizable(True)
        self.scroll_catalog.setStyleSheet("border: none; background-color: transparent;")
        
        self.catalog_container = QWidget()
        # Folosim grid pentru a pune cardurile pe mai multe coloane
        self.catalog_layout = QGridLayout()
        self.catalog_layout.setSpacing(15)
        self.catalog_layout.setAlignment(Qt.AlignTop)
        
        self.catalog_container.setLayout(self.catalog_layout)
        self.scroll_catalog.setWidget(self.catalog_container)
        
        layout.addWidget(self.scroll_catalog)
        self.tab_catalog.setLayout(layout)

    def setup_recommendations_tab(self):
        layout = QVBoxLayout()
        self.scroll_rec = QScrollArea()
        self.scroll_rec.setWidgetResizable(True)
        self.scroll_rec.setStyleSheet("border: none; background-color: transparent;")
        
        self.recs_container = QWidget()
        self.recs_layout = QVBoxLayout()
        self.recs_container.setLayout(self.recs_layout)
        self.scroll_rec.setWidget(self.recs_container)
        layout.addWidget(self.scroll_rec)
        self.tab_recommendations.setLayout(layout)

    def setup_top_tab(self):
        layout = QVBoxLayout()
        self.scroll_top = QScrollArea()
        self.scroll_top.setWidgetResizable(True)
        self.scroll_top.setStyleSheet("border: none; background-color: transparent;")
        
        self.top_container = QWidget()
        self.top_layout = QVBoxLayout()
        self.top_container.setLayout(self.top_layout)
        self.scroll_top.setWidget(self.top_container)
        layout.addWidget(self.scroll_top)
        self.tab_top.setLayout(layout)

    # ==========================================
    # LOGICĂ APLICAȚIE & EVENIMENTE
    # ==========================================
    def handle_login(self):
        user = self.username_input.text().strip()
        pwd = self.password_input.text().strip()
        if verify_user(user, pwd):
            self.current_user = user
            self.load_initial_data()
            self.stacked_widget.setCurrentIndex(1)
        else:
            QMessageBox.warning(self, "Eroare", "Credențiale incorecte!")

    def handle_signup(self):
        user = self.username_input.text().strip()
        pwd = self.password_input.text().strip()
        if not user or not pwd:
            QMessageBox.warning(self, "Eroare", "Completează toate câmpurile!")
            return
        if create_user(user, pwd):
            QMessageBox.information(self, "Succes", "Cont creat! Acum te poți autentifica.")
        else:
            QMessageBox.warning(self, "Eroare", "Numele de utilizator există deja.")

    def handle_logout(self):
        self.current_user = None
        self.username_input.clear()
        self.password_input.clear()
        self.stacked_widget.setCurrentIndex(0)

    def load_initial_data(self):
        self.welcome_label.setText(f"Salut, {self.current_user}! 🍿")
        self.all_movies_data = load_movies()
        
        # Populează combobox-ul cu genuri unice
        genres = sorted(list(set(m["genre"] for m in self.all_movies_data)))
        self.genre_combo.blockSignals(True)
        self.genre_combo.clear()
        self.genre_combo.addItem("Toate genurile")
        self.genre_combo.addItems(genres)
        self.genre_combo.blockSignals(False)
        
        self.filter_catalog() # Aceasta va randa catalogul inițial
        
        # Restul tab-urilor vor fi încărcate on-demand când utilizatorul dă click pe ele
        self.clear_layout(self.recs_layout)
        self.clear_layout(self.top_layout)

    def on_tab_changed(self, index):
        # 1 = Recomandări, 2 = Top
        if index == 1:
            self.load_recommendations()
        elif index == 2:
            self.load_top_global()

    # ==========================================
    # ACTUALIZARE ÎN TIMP REAL (FĂRĂ SCROLL JUMP)
    # ==========================================
    def set_preference(self, movie_id, status):
        add_preference(self.current_user, movie_id, status)
        favs, unfavs = get_user_preferences(self.current_user)
        
        # Actualizăm CULORILE butoanelor doar pentru filmul vizat, pe loc
        if movie_id in self.movie_card_buttons:
            for btns in self.movie_card_buttons[movie_id]:
                fav_btn = btns['fav']
                unfav_btn = btns['unfav']
                
                if movie_id in favs:
                    fav_btn.setStyleSheet("background-color: #a6e3a1; color: #11111b; padding: 6px; border-radius: 5px; font-weight: bold;")
                else:
                    fav_btn.setStyleSheet("background-color: #45475a; padding: 6px; border-radius: 5px; color: #cdd6f4;")
                    
                if movie_id in unfavs:
                    unfav_btn.setStyleSheet("background-color: #f38ba8; color: #11111b; padding: 6px; border-radius: 5px; font-weight: bold;")
                else:
                    unfav_btn.setStyleSheet("background-color: #45475a; padding: 6px; border-radius: 5px; color: #cdd6f4;")
                    
        # Dacă suntem pe filtrul de "Favorite" sau "Neplăcute", ar trebui logic să ascundem cardul dacă a fost debifat
        # Pentru a nu deranja brusc scroll-ul, lăsăm cardul vizibil până la următoarea filtrare manuală.

    # ==========================================
    # RENDERING TAB 1: CATALOG
    # ==========================================
    def filter_catalog(self):
        # Salvează valoarea curentă a scrollbar-ului pentru a preveni salturile la scriere (dacă era deja generat)
        scroll_val = self.scroll_catalog.verticalScrollBar().value()
        
        query = self.search_input.text().lower()
        genre_filter = self.genre_combo.currentText()
        sort_mode = self.sort_combo.currentText()
        view_mode = self.view_combo.currentText()
        
        favs, unfavs = get_user_preferences(self.current_user)
        
        filtered = []
        for m in self.all_movies_data:
            if query and query not in m["title"].lower():
                continue
            if genre_filter != "Toate genurile" and m["genre"] != genre_filter:
                continue
                
            if view_mode == "Filme Favorite ❤️" and m["id"] not in favs:
                continue
            if view_mode == "Filme Neplăcute 👎" and m["id"] not in unfavs:
                continue
            if view_mode == "Neevaluate" and (m["id"] in favs or m["id"] in unfavs):
                continue
                
            filtered.append(m)
            
        if sort_mode == "A-Z":
            filtered.sort(key=lambda x: x["title"])
        elif sort_mode == "Z-A":
            filtered.sort(key=lambda x: x["title"], reverse=True)
        elif sort_mode == "An (Nou-Vechi)":
            filtered.sort(key=lambda x: x["year"], reverse=True)
        elif sort_mode == "An (Vechi-Nou)":
            filtered.sort(key=lambda x: x["year"])
            
        self.render_catalog_cards(filtered, favs, unfavs)
        
        # Restaurare poziție scroll (pentru finețe maximă)
        QTimer.singleShot(10, lambda: self.scroll_catalog.verticalScrollBar().setValue(scroll_val))

    def render_catalog_cards(self, movies_list, favs, unfavs):
        self.clear_layout(self.catalog_layout)
        self.movie_card_buttons.clear() # Resetăm referințele vechi
        
        col, row = 0, 0
        max_cols = 2 # Punem 2 carduri pe rând pentru a folosi spațiul mai bine
        
        for m in movies_list:
            card = self.create_movie_card(m, favs, unfavs)
            self.catalog_layout.addWidget(card, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def create_movie_card(self, movie, favs, unfavs):
        card = QFrame()
        card.setStyleSheet("background-color: #313244; border-radius: 8px; border: 1px solid #45475a;")
        card.setMinimumHeight(130)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        
        title_lbl = QLabel(f"<b>{movie['title']}</b> ({movie['year']})")
        title_lbl.setFont(QFont("Segoe UI", 12))
        title_lbl.setStyleSheet("border: none; color: #cdd6f4;")
        title_lbl.setWordWrap(True)
        
        genre_lbl = QLabel(f"Gen: {movie['genre']}")
        genre_lbl.setStyleSheet("border: none; color: #a6adc8; font-size: 12px;")
        
        btn_layout = QHBoxLayout()
        fav_btn = QPushButton("❤️ Fav")
        unfav_btn = QPushButton("👎 Nu")
        fav_btn.setCursor(Qt.PointingHandCursor)
        unfav_btn.setCursor(Qt.PointingHandCursor)
        
        # Setare stil inițial
        if movie['id'] in favs:
            fav_btn.setStyleSheet("background-color: #a6e3a1; color: #11111b; padding: 6px; border-radius: 5px; font-weight: bold;")
        else:
            fav_btn.setStyleSheet("background-color: #45475a; padding: 6px; border-radius: 5px; border: none; color: #cdd6f4;")
            
        if movie['id'] in unfavs:
            unfav_btn.setStyleSheet("background-color: #f38ba8; color: #11111b; padding: 6px; border-radius: 5px; font-weight: bold;")
        else:
            unfav_btn.setStyleSheet("background-color: #45475a; padding: 6px; border-radius: 5px; border: none; color: #cdd6f4;")
            
        fav_btn.clicked.connect(lambda checked, m_id=movie['id']: self.set_preference(m_id, 'favorite'))
        unfav_btn.clicked.connect(lambda checked, m_id=movie['id']: self.set_preference(m_id, 'unfavorite'))
        
        btn_layout.addWidget(fav_btn)
        btn_layout.addWidget(unfav_btn)
        
        # Salvăm referințele butoanelor pentru update fără reload
        if movie['id'] not in self.movie_card_buttons:
            self.movie_card_buttons[movie['id']] = []
        self.movie_card_buttons[movie['id']].append({'fav': fav_btn, 'unfav': unfav_btn})
        
        layout.addWidget(title_lbl)
        layout.addWidget(genre_lbl)
        layout.addStretch()
        layout.addLayout(btn_layout)
        card.setLayout(layout)
        return card

    # ==========================================
    # RENDERING TAB 2: RECOMANDĂRI SMART
    # ==========================================
    def load_recommendations(self):
        scroll_val = self.scroll_rec.verticalScrollBar().value()
        self.clear_layout(self.recs_layout)
        
        users = load_users()
        movie_ids = [m["id"] for m in self.all_movies_data]
        
        similarities, ranked_users = get_user_similarities(self.current_user, users, movie_ids)
        recs_movies, _ = get_collaborative_recommendations(self.current_user)
        favs, unfavs = get_user_preferences(self.current_user)
        
        # SECTIUNEA A: Utilizatori Similari
        title_a = QLabel("A. Similitudinea cu alți utilizatori")
        title_a.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_a.setStyleSheet("color: #89b4fa; padding-bottom: 5px;")
        self.recs_layout.addWidget(title_a)
        
        if not ranked_users:
            lbl = QLabel("Încă nu ai evaluat filme sau ești singurul utilizator din sistem.")
            lbl.setStyleSheet("color: #a6adc8;")
            self.recs_layout.addWidget(lbl)
        else:
            sim_scroll = QScrollArea()
            sim_scroll.setFixedHeight(120)
            sim_scroll.setWidgetResizable(True)
            sim_scroll.setStyleSheet("background: transparent; border: none;")
            
            sim_container = QWidget()
            sim_layout = QHBoxLayout()
            sim_container.setLayout(sim_layout)
            
            for u in ranked_users:
                u_card = QFrame()
                if u["similarity"] > 50:
                    u_card.setStyleSheet("background-color: #313244; border: 1px solid #a6e3a1; border-radius: 6px; padding: 10px;")
                else:
                    u_card.setStyleSheet("background-color: #313244; border-radius: 6px; padding: 10px;")
                    
                u_card.setFixedWidth(160)
                u_vbox = QVBoxLayout()
                u_vbox.addWidget(QLabel(f"👤 <b>{u['username']}</b>"))
                sim_pct = QLabel(f"{u['similarity']}% similitudine")
                sim_pct.setStyleSheet("color: #a6e3a1;" if u["similarity"] > 50 else "color: #f9e2af;")
                u_vbox.addWidget(sim_pct)
                u_card.setLayout(u_vbox)
                sim_layout.addWidget(u_card)
                
            sim_layout.addStretch()
            sim_scroll.setWidget(sim_container)
            self.recs_layout.addWidget(sim_scroll)
            
        self.add_separator(self.recs_layout)
        
        # SECTIUNEA B: Filme Recomandate
        title_b = QLabel("B. Recomandări pentru tine (Colaborativ)")
        title_b.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_b.setStyleSheet("color: #a6e3a1; padding-bottom: 5px;")
        self.recs_layout.addWidget(title_b)
        
        if not recs_movies:
            lbl = QLabel("Nu există recomandări disponibile momentan. Bazează-te pe topul global!")
            lbl.setStyleSheet("color: #a6adc8;")
            self.recs_layout.addWidget(lbl)
        else:
            for item in recs_movies:
                card = self.create_detailed_movie_card(item["movie"], favs, unfavs, item["score"], item["reason"])
                self.recs_layout.addWidget(card)
                
        self.recs_layout.addStretch()
        QTimer.singleShot(10, lambda: self.scroll_rec.verticalScrollBar().setValue(scroll_val))

    def create_detailed_movie_card(self, movie, favs, unfavs, score, reason):
        card = QFrame()
        card.setStyleSheet("background-color: #313244; border-radius: 8px; margin-bottom: 10px;")
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        header = QHBoxLayout()
        title_lbl = QLabel(f"<b>{movie['title']}</b> ({movie['year']})")
        title_lbl.setFont(QFont("Segoe UI", 15))
        
        score_lbl = QLabel(f"⭐ Recomandare: {score}%")
        score_lbl.setFont(QFont("Segoe UI", 12, QFont.Bold))
        score_lbl.setStyleSheet("color: #f9e2af;")
        score_lbl.setAlignment(Qt.AlignRight)
        
        header.addWidget(title_lbl)
        header.addWidget(score_lbl)
        
        genre_lbl = QLabel(f"Gen: {movie['genre']}")
        genre_lbl.setStyleSheet("color: #bac2de;")
        
        reason_lbl = QLabel(f"💡 {reason}")
        reason_lbl.setStyleSheet("color: #94e2d5; font-style: italic; margin-top: 5px;")
        reason_lbl.setWordWrap(True)
        
        btn_layout = QHBoxLayout()
        fav_btn = QPushButton("❤️ Adaugă la Favorite")
        unfav_btn = QPushButton("👎 Nu îmi place")
        fav_btn.setCursor(Qt.PointingHandCursor)
        unfav_btn.setCursor(Qt.PointingHandCursor)
        
        if movie['id'] in favs:
            fav_btn.setStyleSheet("background-color: #a6e3a1; color: #11111b; padding: 6px 15px; border-radius: 5px; font-weight: bold;")
        else:
            fav_btn.setStyleSheet("background-color: #45475a; padding: 6px 15px; border-radius: 5px; color: #cdd6f4;")
            
        if movie['id'] in unfavs:
            unfav_btn.setStyleSheet("background-color: #f38ba8; color: #11111b; padding: 6px 15px; border-radius: 5px; font-weight: bold;")
        else:
            unfav_btn.setStyleSheet("background-color: #45475a; padding: 6px 15px; border-radius: 5px; color: #cdd6f4;")
            
        fav_btn.clicked.connect(lambda checked, m_id=movie['id']: self.set_preference(m_id, 'favorite'))
        unfav_btn.clicked.connect(lambda checked, m_id=movie['id']: self.set_preference(m_id, 'unfavorite'))
        
        # Salvăm referințele butoanelor și aici pentru update in-place dacă se dă click de aici
        if movie['id'] not in self.movie_card_buttons:
            self.movie_card_buttons[movie['id']] = []
        self.movie_card_buttons[movie['id']].append({'fav': fav_btn, 'unfav': unfav_btn})
        
        btn_layout.addWidget(fav_btn)
        btn_layout.addWidget(unfav_btn)
        btn_layout.addStretch()
        
        layout.addLayout(header)
        layout.addWidget(genre_lbl)
        layout.addWidget(reason_lbl)
        layout.addSpacing(10)
        layout.addLayout(btn_layout)
        card.setLayout(layout)
        return card

    # ==========================================
    # RENDERING TAB 3: TOP GLOBAL
    # ==========================================
    def load_top_global(self):
        scroll_val = self.scroll_top.verticalScrollBar().value()
        self.clear_layout(self.top_layout)
        
        top_list = get_global_top()
        favs, unfavs = get_user_preferences(self.current_user)
        
        title = QLabel("🏆 Top Global al Preferințelor")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #f9e2af; padding-bottom: 10px;")
        self.top_layout.addWidget(title)
        
        if not top_list:
            lbl = QLabel("Niciun film nu a fost apreciat de vreun utilizator încă.")
            lbl.setStyleSheet("color: #a6adc8;")
            self.top_layout.addWidget(lbl)
        else:
            for rank, item in enumerate(top_list, start=1):
                movie = item["movie"]
                card = QFrame()
                card.setStyleSheet("background-color: #313244; border-radius: 8px; margin-bottom: 10px;")
                h_layout = QHBoxLayout()
                h_layout.setContentsMargins(15, 10, 15, 10)
                
                # Ranking nr
                rank_lbl = QLabel(f"#{rank}")
                rank_lbl.setFont(QFont("Arial", 22, QFont.Bold))
                rank_lbl.setStyleSheet("color: #f9e2af;")
                rank_lbl.setFixedWidth(50)
                
                # Info Film
                v_info = QVBoxLayout()
                v_info.addWidget(QLabel(f"<b>{movie['title']}</b> ({movie['year']}) - <i>{movie['genre']}</i>"))
                
                stats_lbl = QLabel(f"❤️ {item['favs']} aprecieri | 👎 {item['unfavs']} dezaprobări (Procent: {item['pct']}%)")
                stats_lbl.setStyleSheet("color: #bac2de; font-size: 12px;")
                v_info.addWidget(stats_lbl)
                
                # Buttons
                btn_layout = QVBoxLayout()
                fav_btn = QPushButton("Fav")
                unfav_btn = QPushButton("Nu")
                fav_btn.setFixedSize(60, 25)
                unfav_btn.setFixedSize(60, 25)
                
                if movie['id'] in favs:
                    fav_btn.setStyleSheet("background-color: #a6e3a1; color: #11111b; font-weight: bold; border-radius: 4px;")
                else:
                    fav_btn.setStyleSheet("background-color: #45475a; color: #cdd6f4; border-radius: 4px;")
                    
                if movie['id'] in unfavs:
                    unfav_btn.setStyleSheet("background-color: #f38ba8; color: #11111b; font-weight: bold; border-radius: 4px;")
                else:
                    unfav_btn.setStyleSheet("background-color: #45475a; color: #cdd6f4; border-radius: 4px;")
                    
                fav_btn.clicked.connect(lambda checked, m_id=movie['id']: self.set_preference(m_id, 'favorite'))
                unfav_btn.clicked.connect(lambda checked, m_id=movie['id']: self.set_preference(m_id, 'unfavorite'))
                
                if movie['id'] not in self.movie_card_buttons:
                    self.movie_card_buttons[movie['id']] = []
                self.movie_card_buttons[movie['id']].append({'fav': fav_btn, 'unfav': unfav_btn})
                
                btn_layout.addWidget(fav_btn)
                btn_layout.addWidget(unfav_btn)
                
                h_layout.addWidget(rank_lbl)
                h_layout.addLayout(v_info)
                h_layout.addStretch()
                h_layout.addLayout(btn_layout)
                
                card.setLayout(h_layout)
                self.top_layout.addWidget(card)
                
        self.top_layout.addStretch()
        QTimer.singleShot(10, lambda: self.scroll_top.verticalScrollBar().setValue(scroll_val))

    # ==========================================
    # UTILS
    # ==========================================
    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())
                    
    def add_separator(self, layout):
        layout.addSpacing(15)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #45475a;")
        layout.addWidget(line)
        layout.addSpacing(15)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MovieApp()
    ex.show()
    sys.exit(app.exec_())