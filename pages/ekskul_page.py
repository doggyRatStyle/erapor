import flet as ft
from database import db


class EkskulPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.main_page = page
        self.route = "/ekskul"

        self.id_field = ft.TextField(
            label="ID Ekstrakurikuler",
            read_only=True,
            value=db.generate_ekskul_id(),
            width=150
        )

        self.nama_field = ft.TextField(
            label="Nama Ekstrakurikuler",
            width=300
        )

        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID Ekstrakurikuler")),
                ft.DataColumn(ft.Text("Nama Ekstrakurikuler")),
                ft.DataColumn(ft.Text("Aksi")),
            ],
            rows=[]
        )

        self.load_data()

        self.controls = [
            ft.AppBar(
                title=ft.Text("Data Ekstrakurikuler"),
                bgcolor=ft.Colors.BLUE_700,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/dashboard"))
            ),
            ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Text("Input Ekstrakurikuler", size=18, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            controls=[
                                self.id_field,
                                self.nama_field,
                                ft.ElevatedButton(
                                    "Tambah",
                                    icon=ft.Icons.ADD,
                                    on_click=self.save_ekskul
                                )
                            ]
                        ),
                        ft.Divider(),
                        ft.Text("Daftar Ekstrakurikuler", size=18, weight=ft.FontWeight.BOLD),
                        self.data_table
                    ]
                )
            )
        ]

    def load_data(self):
        ekskul_list = db.get_all_ekskul()
        self.data_table.rows.clear()

        for ekskul in ekskul_list:
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(ekskul['id_ekskul'])),
                        ft.DataCell(ft.Text(ekskul['nama_ekskul'])),
                        ft.DataCell(
                            ft.IconButton(ft.Icons.DELETE, tooltip="Hapus")
                        ),
                    ]
                )
            )

    def save_ekskul(self, e):
        if not self.nama_field.value:
            return

        data = {
            'id_ekskul': self.id_field.value,
            'nama_ekskul': self.nama_field.value
        }

        db.save_ekskul(data)
        self.id_field.value = db.generate_ekskul_id()
        self.nama_field.value = ""
        self.load_data()

        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Ekstrakurikuler berhasil ditambahkan!"),
            bgcolor=ft.Colors.GREEN_700
        )
        self.page.snack_bar.open = True
        self.page.update()