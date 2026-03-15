import flet as ft
from database import db


class LMPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.main_page = page
        self.route = "/lm"

        self.mapel_dropdown = ft.Dropdown(
            label="Pilih Mata Pelajaran",
            width=300,
            on_change=self.on_mapel_change
        )

        self.load_mapel_options()

        self.id_field = ft.TextField(
            label="ID Lingkup Materi",
            read_only=True,
            value=db.generate_lm_id(),
            width=150
        )

        self.lm_field = ft.TextField(
            label="Lingkup Materi",
            width=400,
            multiline=True,
            min_lines=2
        )

        self.lm_list = ft.Column(scroll=ft.ScrollMode.AUTO, height=300)

        self.controls = [
            ft.AppBar(
                title=ft.Text("Data Lingkup Materi"),
                bgcolor=ft.Colors.BLUE_700,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/dashboard"))
            ),
            ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Text("Input Lingkup Materi", size=18, weight=ft.FontWeight.BOLD),
                        self.mapel_dropdown,
                        ft.Row(
                            controls=[
                                self.id_field,
                                self.lm_field,
                                ft.ElevatedButton(
                                    "Tambah LM",
                                    icon=ft.Icons.ADD,
                                    on_click=self.save_lm
                                )
                            ]
                        ),
                        ft.Divider(),
                        ft.Text("Daftar Lingkup Materi", size=18, weight=ft.FontWeight.BOLD),
                        self.lm_list
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
            self.load_lm_list()

    def load_lm_list(self):
        id_mapel = self.mapel_dropdown.value
        if not id_mapel:
            return

        lm_list = db.get_lm_by_mapel(id_mapel)
        self.lm_list.controls.clear()

        for lm in lm_list:
            self.lm_list.controls.append(
                ft.ListTile(
                    title=ft.Text(f"{lm['id_lm']}"),
                    subtitle=ft.Text(lm['lingkup_materi']),
                    trailing=ft.IconButton(ft.Icons.DELETE, tooltip="Hapus")
                )
            )
        self.page.update()

    def save_lm(self, e):
        if not self.mapel_dropdown.value or not self.lm_field.value:
            return

        data = {
            'id_lm': self.id_field.value,
            'id_mapel': self.mapel_dropdown.value,
            'lingkup_materi': self.lm_field.value
        }
        db.save_lm(data)
        self.id_field.value = db.generate_lm_id()
        self.lm_field.value = ""
        self.load_lm_list()

        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Lingkup Materi berhasil ditambahkan!"),
            bgcolor=ft.Colors.GREEN_700
        )
        self.page.snack_bar.open = True
        self.page.update()