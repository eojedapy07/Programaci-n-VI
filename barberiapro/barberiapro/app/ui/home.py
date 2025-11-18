import flet as ft
import traceback
from . import clientes_view, barberos_view, servicios_view, turnos_view, ventas_view

def handle_error(page, e):
    print("ERROR:", e)
    print(traceback.format_exc())

def view(page: ft.Page, app_state):
    try:
        page.controls.clear()

        tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(text="Clientes", icon=ft.Icons.PERSON),
                ft.Tab(text="Barberos", icon=ft.Icons.CONTENT_CUT),
                ft.Tab(text="Servicios", icon=ft.Icons.MONEY),
                ft.Tab(text="Turnos", icon=ft.Icons.EVENT_AVAILABLE),
                ft.Tab(text="Ventas", icon=ft.Icons.ATTACH_MONEY),
            ],
            expand=1
        )
        content = ft.Container()

        def get_view(idx):
            try:
                if idx == 0:
                    return clientes_view.view(page, app_state, embed=True)
                if idx == 1:
                    return barberos_view.view(page, app_state, embed=True)
                if idx == 2:
                    return servicios_view.view(page, app_state, embed=True)
                if idx == 3:
                    return turnos_view.view(page, app_state, embed=True)
                if idx == 4:
                    return ventas_view.view(page, app_state, embed=True)
                return ft.Text("No view")
            except Exception as e:
                handle_error(page, e)

        def on_tab_change(e):
            content.content = get_view(e.control.selected_index)
            page.update()

        tabs.on_change = on_tab_change
        content.content = get_view(0)

        username = app_state.get("user", {}).get("username") if app_state.get("user") else "Invitado"
        header = ft.Row([
            ft.Text(f"Usuario: {username}", style="labelLarge"),
            ft.Row(expand=True),
            ft.ElevatedButton("Cerrar sesión", on_click=lambda e: logout(page, app_state))
        ])

        page.add(header, tabs, ft.Divider(), content)
        page.update()
    except Exception as e:
        handle_error(page, e)

def logout(page, app_state):
    app_state["user"] = None
    from . import login_view
    login_view.view(page, lambda u: view(page, app_state), app_state)
