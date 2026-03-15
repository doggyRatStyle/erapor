import flet as ft
import pandas as pd
from database import db
import uuid


class SiswaPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.main_page = page
        self.route = "/siswa"

        self.selected_file = ft.Text()
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("NIS")),
                ft.DataColumn(ft.Text("NISN")),
                ft.DataColumn(ft.Text("Nama")),
                ft.DataColumn(ft.Text("L/P")),
                ft.DataColumn(ft.Text("Aksi")),
            ],
            rows=[]
        )

        self.load_siswa_data()

        self.controls = [
            ft.AppBar(
                title=ft.Text("Data Siswa"),
                bgcolor=ft.Colors.BLUE_700,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/dashboard")),
                actions=[
                    ft.IconButton(ft.Icons.ADD, on_click=self.show_add_dialog),
                    ft.IconButton(ft.Icons.UPLOAD_FILE, on_click=self.show_import_dialog)
                ]
            ),
            ft.Container(
                expand=True,
                padding=20,
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Text("Daftar Siswa", size=20, weight=ft.FontWeight.BOLD),
                        self.data_table
                    ]
                )
            )
        ]

    def load_siswa_data(self):
        siswa_list = db.get_all_siswa()
        self.data_table.rows.clear()

        for siswa in siswa_list:
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(siswa['nis'])),
                        ft.DataCell(ft.Text(siswa['nisn'])),
                        ft.DataCell(ft.Text(siswa['nama_lengkap'])),
                        ft.DataCell(ft.Text(siswa['jenis_kelamin'])),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.IconButton(ft.Icons.EDIT, tooltip="Edit"),
                                    ft.IconButton(ft.Icons.DELETE, tooltip="Hapus"),
                                ]
                            )
                        ),
                    ]
                )
            )

    def show_add_dialog(self, e):
        # Dialog untuk tambah siswa manual
        fields = {}
        field_list = [
            'nis', 'nisn', 'nama_lengkap', 'jenis_kelamin', 'tempat_lahir',
            'tanggal_lahir', 'agama', 'pendidikan_sebelumnya', 'alamat_siswa',
            'nama_ayah', 'nama_ibu', 'pekerjaan_ayah', 'pekerjaan_ibu',
            'alamat_ortu_jalan', 'alamat_ortu_kelurahan', 'alamat_ortu_kecamatan',
            'alamat_ortu_kabupaten', 'alamat_ortu_provinsi',
            'nama_wali', 'pekerjaan_wali', 'alamat_wali', 'no_telepon'
        ]

        for field_name in field_list:
            fields[field_name] = ft.TextField(label=field_name.replace('_', ' ').title())

        def save_siswa(e):
            data = {k: v.value for k, v in fields.items()}
            data['uuid'] = str(uuid.uuid4())
            db.save_siswa(data)
            self.load_siswa_data()
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Tambah Siswa"),
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=list(fields.values()),
                height=400,
                width=500
            ),
            actions=[
                ft.TextButton("Batal", on_click=lambda e: setattr(dialog, 'open', False) or self.page.update()),
                ft.ElevatedButton("Simpan", on_click=save_siswa)
            ]
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def show_import_dialog(self, e):
        def pick_files_result(e: ft.FilePickerResultEvent):
            if e.files:
                file_path = e.files[0].path
                try:
                    df = pd.read_csv(file_path)
                    db.import_siswa_csv(df)
                    self.load_siswa_data()
                    self.page.snack_bar = ft.SnackBar(
                        content=ft.Text(f"Berhasil import {len(df)} data siswa!"),
                        bgcolor=ft.Colors.GREEN_700
                    )
                    self.page.snack_bar.open = True
                except Exception as ex:
                    self.page.snack_bar = ft.SnackBar(
                        content=ft.Text(f"Error: {str(ex)}"),
                        bgcolor=ft.Colors.RED_700
                    )
                    self.page.snack_bar.open = True
                self.page.update()

        file_picker = ft.FilePicker(on_result=pick_files_result)
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.pick_files(allowed_extensions=["csv"])