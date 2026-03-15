import flet as ft
from database import db


class MapelPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.main_page = page
        self.route = "/mapel"

        self.id_field = ft.TextField(
            label="ID Mapel",
            read_only=True,
            value=db.generate_mapel_id(),
            width=150
        )

        self.nama_field = ft.TextField(
            label="Nama Mata Pelajaran",
            width=300
        )

        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID Mapel")),
                ft.DataColumn(ft.Text("Nama Mata Pelajaran")),
                ft.DataColumn(ft.Text("Aksi")),
            ],
            rows=[]
        )

        self.load_data()

        self.controls = [
            ft.AppBar(
                title=ft.Text("Data Intrakurikuler"),
                bgcolor=ft.Colors.BLUE_700,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/dashboard"))
            ),
            ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Text("Input Mata Pelajaran", size=18, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            controls=[
                                self.id_field,
                                self.nama_field,
                                ft.ElevatedButton(
                                    "Tambah",
                                    icon=ft.Icons.ADD,
                                    on_click=self.save_mapel
                                )
                            ]
                        ),
                        ft.Divider(),
                        ft.Text("Daftar Mata Pelajaran", size=18, weight=ft.FontWeight.BOLD),
                        self.data_table
                    ]
                )
            )
        ]

    def load_data(self):
        mapel_list = db.get_all_mapel()
        self.data_table.rows.clear()

        for mapel in mapel_list:
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(mapel['id_mapel'])),
                        ft.DataCell(ft.Text(mapel['nama_mapel'])),
                        ft.DataCell(
                            ft.IconButton(ft.Icons.DELETE, tooltip="Hapus")
                        ),
                    ]
                )
            )

    def save_mapel(self, e):
        if not self.nama_field.value:
            return

        data = {
            'id_mapel': self.id_field.value,
            'nama_mapel': self.nama_field.value
        }

        db.save_mapel(data)
        self.id_field.value = db.generate_mapel_id()
        self.nama_field.value = ""
        self.load_data()

        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Mata pelajaran berhasil ditambahkan!"),
            bgcolor=ft.Colors.GREEN_700
        )
        self.page.snack_bar.open = True
        self.page.update()