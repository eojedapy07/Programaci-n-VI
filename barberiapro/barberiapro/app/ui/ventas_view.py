import flet as ft
import traceback
from .. import models

def handle_error(page, e):
    print("ERROR:", e)
    print(traceback.format_exc())

def view(page: ft.Page, app_state, embed=True):
    table = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("Cliente")),
        ft.DataColumn(ft.Text("Servicio")),
        ft.DataColumn(ft.Text("Monto")),
        ft.DataColumn(ft.Text("Fecha")),
        ft.DataColumn(ft.Text("Acciones"))
    ], rows=[], expand=True)

    sidebar = ft.Container(width=0, right=0, height=page.window_height, padding=16, bgcolor="#F5F5F5")

    select_cliente = ft.Dropdown(label="Cliente", options=[])
    select_servicio = ft.Dropdown(label="Servicio", options=[])
    monto = ft.TextField(label="Monto")
    fecha = ft.TextField(label="Fecha (YYYY-MM-DD)")
    current = None

    def load_dropdowns():
        select_cliente.options = [ft.dropdown.Option(str(c["id"]), c["nombre"]) for c in models.get_clientes()]
        select_servicio.options = [ft.dropdown.Option(str(s["id"]), s["nombre"]) for s in models.get_servicios()]

    def show_sidebar(content, width=420):
        sidebar.content = content
        sidebar.width = width
        page.update()

    def hide_sidebar():
        sidebar.width = 0
        page.update()

    def open_form(row=None):
        nonlocal current
        load_dropdowns()
        current = row
        if row:
            select_cliente.value = str(row.get("cliente_id") or "")
            select_servicio.value = str(row.get("servicio_id") or "")
            monto.value = str(row.get("monto") or "")
            fecha.value = row.get("fecha") or ""
            title = "Editar Venta"
        else:
            select_cliente.value = select_servicio.value = None
            monto.value = fecha.value = ""
            title = "Nueva Venta"

        def save(e):
            try:
                if not select_cliente.value or not select_servicio.value or not monto.value.strip():
                    page.snack_bar = ft.SnackBar(ft.Text("Completa cliente, servicio y monto"))
                    page.snack_bar.open = True
                    page.update()
                    return
                if current:
                    models.update_venta(current["id"],
                                        int(select_cliente.value),
                                        int(select_servicio.value),
                                        float(monto.value),
                                        fecha.value.strip())
                else:
                    models.create_venta(int(select_cliente.value),
                                        int(select_servicio.value),
                                        float(monto.value),
                                        fecha.value.strip())
                hide_sidebar()
                load()
            except Exception as ex:
                handle_error(page, ex)

        content = ft.Column([
            ft.Row([ft.Text(title, weight="bold", size=16), ft.Row(expand=True), ft.IconButton(ft.icons.CLOSE, on_click=lambda e: hide_sidebar())]),
            ft.Divider(),
            select_cliente, select_servicio, monto, fecha,
            ft.Row([ft.ElevatedButton("Guardar", on_click=save), ft.OutlinedButton("Cancelar", on_click=lambda e: hide_sidebar())])
        ], tight=True, scroll="auto")

        show_sidebar(content)

    def delete(row):
        models.delete_venta(row["id"])
        load()

    def load():
        table.rows.clear()
        for r in models.get_ventas():
            table.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(r.get("cliente") or "")),
                ft.DataCell(ft.Text(r.get("servicio") or "")),
                ft.DataCell(ft.Text(str(r.get("monto") or ""))),
                ft.DataCell(ft.Text(r.get("fecha") or "")),
                ft.DataCell(ft.Row([ft.IconButton(ft.Icons.EDIT, on_click=lambda e, row=r: open_form(row)),
                                     ft.IconButton(ft.Icons.DELETE, on_click=lambda e, row=r: delete(row))]))
            ]))
        page.update()

    load()
    return ft.Stack([ft.Column([ft.Row([ft.ElevatedButton("Nueva Venta", on_click=lambda e: open_form())]), table]), sidebar])
