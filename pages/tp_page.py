import flet as ft
from database import db


class TPPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.main_page = page
        self.route = "/tp"

        self.mapel_dropdown = ft.Dropdown(
            label="Pilih Mata Pelajaran",
            width=300,
            on_change=self.on_mapel_change
        )

        self.load_mapel_options()

        self.id_field = ft.TextField(
            label="ID Tujuan Pembelajaran",
            read_only=True,
            value=db.generate_tp_id(),
            width=150
        )

        self.tp_field = ft.TextField(
            label="Tujuan Pembelajaran",
            width=400,
            multiline=True,
            min_lines=2
        )

        self.tp_list = ft.Column(scroll=ft.ScrollMode.AUTO, height=300)

        self.controls = [
            ft.AppBar(
                title=ft.Text("Data Tujuan Pembelajaran"),
                bgcolor=ft.colors.BLUE_700,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/dashboard"))
            ),
            ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Text("Input Tujuan Pembelajaran", size=18, weight=ft.FontWeight.BOLD),
                        self.mapel_dropdown,
                        ft.Row(
                            controls=[
                                self.id_field,
                                self.tp_field,
                                ft.ElevatedButton(
                                    "Tambah TP",
                                    icon=ft.Icons.ADD,
                                    on_click=self.save_tp
                                )
                            ]
                        ),
                        ft.Divider(),
                        ft.Text("Daftar Tujuan Pembelajaran", size=18, weight=ft.FontWeight.BOLD),
                        self.tp_list
                    ]
                )
            )
        ]

    def load_mapel_options(self):
        mapel_list = db.get_all_mapel()
        self.mapel_dropdown.options = [
            ft.dropdown.Option(mapel['id_mapel'], mapel['nama_mapel'])
            for mapel in mapel_list
        ]

    def on_mapel_change(self, e):
        if self.mapel_dropdown.value:
            self.load_tp_list()

    def load_tp_list(self):
        id_mapel = self.mapel_dropdown.value
        if not id_mapel:
            return

        tp_list = db.get_tp_by_mapel(id_mapel)
        self.tp_list.controls.clear()

        for tp in tp_list:
            self.tp_list.controls.append(
                ft.ListTile(
                    title=ft.Text(f"{tp['id_tp']}"),
                    subtitle=ft.Text(tp['tujuan_pembelajaran']),
                    trailing=ft.IconButton(ft.Icons.DELETE, tooltip="Hapus")
                )
            )
        self.page.update()

    def save_tp(self, e):
        if not self.mapel_dropdown.value or not self.tp_field.value:
            return

        data = {
            'id_tp': self.id_field.value,
            'id_mapel': self.mapel_dropdown.value,
            'tujuan_pembelajaran': self.tp_field.value
        }

        db.save_tp(data)
        self.id_field.value = db.generate_tp_id()
        self.tp_field.value = ""
        self.load_tp_list()

        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Tujuan Pembelajaran berhasil ditambahkan!"),
            bgcolor=ft.colors.GREEN_700
        )
        self.page.snack_bar.open = True
        self.page.update()