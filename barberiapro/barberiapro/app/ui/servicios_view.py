import flet as ft
import traceback
from .. import models

def handle_error(page, e):
    print("ERROR:", e)
    print(traceback.format_exc())

def view(page: ft.Page, app_state, embed=True):
    table = ft.DataTable(columns=[ft.DataColumn(ft.Text("Servicio")), ft.DataColumn(ft.Text("Precio")), ft.DataColumn(ft.Text("Acciones"))],
                         rows=[], expand=True)

    sidebar = ft.Container(width=0, right=0, height=page.window_height, padding=16, bgcolor="#F5F5F5")

    nombre = ft.TextField(label="Servicio")
    precio = ft.TextField(label="Precio")
    current = None

    def show_sidebar(content, width=360):
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
            precio.value = str(row.get("precio", 0))
            title = "Editar Servicio"
        else:
            nombre.value = precio.value = ""
            title = "Nuevo Servicio"

        def save(e):
            try:
                if not nombre.value.strip():
                    page.snack_bar = ft.SnackBar(ft.Text("El nombre es obligatorio"))
                    page.snack_bar.open = True
                    page.update()
                    return
                p = float(precio.value or 0)
                if current:
                    models.update_servicio(current["id"], nombre.value.strip(), p)
                else:
                    models.create_servicio(nombre.value.strip(), p)
                hide_sidebar()
                load()
            except Exception as ex:
                handle_error(page, ex)

        content = ft.Column([
            ft.Row([ft.Text(title, weight="bold", size=16), ft.Row(expand=True), ft.IconButton(ft.icons.CLOSE, on_click=lambda e: hide_sidebar())]),
            ft.Divider(),
            nombre, precio,
            ft.Row([ft.ElevatedButton("Guardar", on_click=save), ft.OutlinedButton("Cancelar", on_click=lambda e: hide_sidebar())])
        ], tight=True, scroll="auto")

        show_sidebar(content)

    def delete(row):
        models.delete_servicio(row["id"])
        load()

    def load():
        table.rows.clear()
        for r in models.get_servicios():
            table.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(r["nombre"])),
                ft.DataCell(ft.Text(f"{r.get('precio', 0):.2f}")),
                ft.DataCell(ft.Row([ft.IconButton(ft.Icons.EDIT, on_click=lambda e, row=r: open_form(row)),
                                     ft.IconButton(ft.Icons.DELETE, on_click=lambda e, row=r: delete(row))]))
            ]))
        page.update()

    load()
    return ft.Stack([ft.Column([ft.Row([ft.ElevatedButton("Nuevo Servicio", on_click=lambda e: open_form())]), table]), sidebar])
