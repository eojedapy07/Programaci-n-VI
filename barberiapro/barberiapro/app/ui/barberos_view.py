import flet as ft
import traceback
from .. import models

def handle_error(page, e):
    print("ERROR:", e)
    print(traceback.format_exc())

def view(page: ft.Page, app_state, embed=True):
    table = ft.DataTable(columns=[ft.DataColumn(ft.Text("Nombre")), ft.DataColumn(ft.Text("Especialidad")), ft.DataColumn(ft.Text("Acciones"))],
                         rows=[], expand=True)

    sidebar = ft.Container(width=0, right=0, height=page.window_height, padding=16, bgcolor="#F5F5F5")

    nombre = ft.TextField(label="Nombre")
    espec = ft.TextField(label="Especialidad")
    current = None

    def show_sidebar(content, width=340):
        sidebar.content = content
        sidebar.width = width
        page.update()

    def hide_sidebar():
        sidebar.width = 0
        page.update()

    def open_form(row=None):
        nonlocal current
        current = row
        if row:
            nombre.value = row["nombre"]
            espec.value = row.get("especialidad") or ""
            title = "Editar Barbero"
        else:
            nombre.value = espec.value = ""
            title = "Nuevo Barbero"

        def save(e):
            try:
                if not nombre.value.strip():
                    page.snack_bar = ft.SnackBar(ft.Text("El nombre es obligatorio"))
                    page.snack_bar.open = True
                    page.update()
                    return
                if current:
                    models.update_barbero(current["id"], nombre.value.strip(), espec.value.strip())
                else:
                    models.create_barbero(nombre.value.strip(), espec.value.strip())
                hide_sidebar()
                load()
            except Exception as ex:
                handle_error(page, ex)

        content = ft.Column([
            ft.Row([ft.Text(title, weight="bold", size=16), ft.Row(expand=True), ft.IconButton(ft.icons.CLOSE, on_click=lambda e: hide_sidebar())]),
            ft.Divider(),
            nombre, espec,
            ft.Row([ft.ElevatedButton("Guardar", on_click=save), ft.OutlinedButton("Cancelar", on_click=lambda e: hide_sidebar())])
        ], tight=True, scroll="auto")

        show_sidebar(content)

    def delete(row):
        models.delete_barbero(row["id"])
        load()

    def load():
        table.rows.clear()
        for r in models.get_barberos():
            table.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(r["nombre"])),
                ft.DataCell(ft.Text(r.get("especialidad") or "")),
                ft.DataCell(ft.Row([ft.IconButton(ft.Icons.EDIT, on_click=lambda e, row=r: open_form(row)),
                                     ft.IconButton(ft.Icons.DELETE, on_click=lambda e, row=r: delete(row))]))
            ]))
        page.update()

    load()
    return ft.Stack([ft.Column([ft.Row([ft.ElevatedButton("Nuevo Barbero", on_click=lambda e: open_form())]), table]), sidebar])
