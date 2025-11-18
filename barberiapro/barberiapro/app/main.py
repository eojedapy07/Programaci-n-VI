import sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

print("PYTHONPATH:", sys.path)  # Debug

import flet as ft
from app import db, auth
from app.ui import login_view, home

def main(page: ft.Page):
    page.title = "Barbería Pro — Panel"
    page.window_width = 1100
    page.window_height = 720
    page.padding = 12

    # Init DB & default admin
    db.init_db()
    auth.ensure_default_admin()

    app_state = {"page": page, "user": None}

    def on_login(user):
        app_state["user"] = user
        page.controls.clear()
        home.view(page, app_state)

    login_view.view(page, on_login, app_state)

if __name__ == "__main__":
    ft.app(target=main)
