import flet as ft
import traceback
from .. import models

def handle_error(page, e):
    print("ERROR:", e)
    print(traceback.format_exc())

def view(page: ft.Page, app_state, embed=True):
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Nota")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[],
        expand=True
    )

    # Sidebar container on the right (initial width 0)
    sidebar = ft.Container(width=0, right=0, height=page.window_height, padding=16,
                          bgcolor="#F5F5F5")  # neutral light background

    nombre = ft.TextField(label="Nombre")
    telefono = ft.TextField(label="Teléfono")
    nota = ft.TextField(label="Nota (opcional)")
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
            telefono.value = row.get("telefono") or ""
            nota.value = row.get("nota") or ""
            title = "Editar Cliente"
        else:
            nombre.value = telefono.value = nota.value = ""
            title = "Nuevo Cliente"

        def save(e):
            try:
                if not nombre.value.strip():
                    page.snack_bar = ft.SnackBar(ft.Text("El nombre es obligatorio"))
                    page.snack_bar.open = True
                    page.update()
                    return
                if current:
                    models.update_cliente(current["id"], nombre.value.strip(), telefono.value.strip(), nota.value.strip())
                else:
                    models.create_cliente(nombre.value.strip(), telefono.value.strip(), nota.value.strip())
                hide_sidebar()
                load()
            except Exception as ex:
                handle_error(page, ex)

        content = ft.Column([
            ft.Row([ft.Text(title, weight="bold", size=16), ft.Row(expand=True), ft.IconButton(ft.icons.CLOSE, on_click=lambda e: hide_sidebar())]),
            ft.Divider(),
            nombre, telefono, nota,
            ft.Row([ft.ElevatedButton("Guardar", on_click=save), ft.OutlinedButton("Cancelar", on_click=lambda e: hide_sidebar())])
        ], tight=True, scroll="auto")

        show_sidebar(content)

    def delete(row):
        models.delete_cliente(row["id"])
        load()

    def load():
        table.rows.clear()
        for r in models.get_clientes():
            table.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(r["nombre"])),
                ft.DataCell(ft.Text(r.get("telefono") or "")),
                ft.DataCell(ft.Text(r.get("nota") or "")),
                ft.DataCell(ft.Row([ft.IconButton(ft.Icons.EDIT, on_click=lambda e, row=r: open_form(row)),
                                     ft.IconButton(ft.Icons.DELETE, on_click=lambda e, row=r: delete(row))]))
            ]))
        page.update()

    load()
    # Use Stack so sidebar overlays on the right of the table
    return ft.Stack([ft.Column([ft.Row([ft.ElevatedButton("Nuevo Cliente", on_click=lambda e: open_form())]), table]), sidebar])
