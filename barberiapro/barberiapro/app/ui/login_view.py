import flet as ft
import traceback
from .. import auth

def handle_error(page, e):
    print("ERROR:", e)
    print(traceback.format_exc())

def view(page: ft.Page, on_login_callback, app_state):
    try:
        page.controls.clear()
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        username = ft.TextField(label="Usuario", width=320)
        password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=320)
        message = ft.Text("", color=ft.Colors.RED)

        def do_login(e=None):
            try:
                u = (username.value or "").strip()
                p = (password.value or "").strip()
                if not u or not p:
                    message.value = "Completa ambos campos"
                    page.update()
                    return
                user = auth.verify_user(u, p)
                if user:
                    on_login_callback(user)
                else:
                    message.value = "Usuario o contraseña inválidos"
                    page.update()
            except Exception as ex:
                handle_error(page, ex)

        username.on_submit = do_login
        password.on_submit = do_login

        card = ft.Card(
            ft.Container(
                ft.Column([
                    ft.Text("Barbería Pro", style="headlineSmall"),
                    ft.Text("Panel administrativo", style="labelLarge"),
                    ft.Divider(),
                    username,
                    password,
                    message,
                    ft.ElevatedButton("Ingresar", on_click=do_login, width=320),
                ], spacing=12),
                padding=24, width=420
            ), elevation=4
        )

        page.add(ft.Column([card], alignment=ft.MainAxisAlignment.CENTER))
        page.update()
    except Exception as e:
        handle_error(page, e)
