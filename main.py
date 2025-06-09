import sys, requests
from PyQt5 import QtWidgets, QtCore
from ui import MainWindow

API_KEY   = "201a5c23024a0fe6f9dc940af3accfc2"
BASE_URL  = "https://v3.football.api-sports.io"

# Mapeo país → league_id en API-Football
LEAGUE_MAP = {
    "Inglaterra": 39,
    "España":    140,
    "Italia":    135
}

def fetch_matches(league_id, date):
    headers = {"x-apisports-key": API_KEY}
    params  = {"league": league_id, "season": 2025, "date": date}
    r = requests.get(f"{BASE_URL}/fixtures", headers=headers, params=params)
    return r.json().get("response", [])

def format_stats(fixture):
    s = fixture.get("statistics", [])
    # Busca las estadísticas que importan
    goals    = next((x for x in s if x["type"]=="Goals"), {}).get("value","–")
    corners  = next((x for x in s if x["type"]=="Corner Kicks"), {}).get("value","–")
    cards    = next((x for x in s if x["type"]=="Card"), {}).get("value","–")
    return goals, cards, corners

def calc_probability(home, away):
    # Ejemplo muy básico: prob = fuerza local / (suma fuerzas)
    total = home + away
    if total==0: return (33,33,33)
    p_home = int((home/total)*100)
    p_away = int((away/total)*100)
    p_draw = 100 - p_home - p_away
    return p_home, p_draw, p_away

def load_and_display(window):
    country = window.country_cb.currentText()
    day     = window.day_cb.currentText()
    date    = QtCore.QDate.currentDate()
    if day=="Mañana":
        date = date.addDays(1)
    date_str = date.toString("yyyy-MM-dd")

    league_id = LEAGUE_MAP[country]
    fixtures  = fetch_matches(league_id, date_str)

    window.match_list.clear()
    for f in fixtures:
        teams = f["teams"]["home"]["name"] + " vs " + f["teams"]["away"]["name"]
        # Stats
        goals, cards, corners = format_stats(f)
        # Probabilidades dummy (de momento con goles como fuerza)
        try:
            home_strength = int(goals)
            away_strength = int(goals)
        except:
            home_strength = away_strength = 1
        p_home, p_draw, p_away = calc_probability(home_strength, away_strength)
        line = f"{teams}\n Goles: {goals}  |  Tarjetas: {cards}  |  Corners: {corners}\n "
        line+= f"Prob: {p_home}% / {p_draw}% / {p_away}%"
        window.match_list.addItem(line)

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    w   = MainWindow()
    w.show()
    # Conecta botones
    w.reload_btn.clicked.connect(lambda: load_and_display(w))
    w.country_cb.currentIndexChanged.connect(lambda: load_and_display(w))
    w.day_cb.currentIndexChanged.connect(lambda: load_and_display(w))
    # Primera carga
    load_and_display(w)
    sys.exit(app.exec_())
