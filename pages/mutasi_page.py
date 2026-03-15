import flet as ft
from database import db
from config import MUTASI_MASUK, MUTASI_KELUAR


class MutasiPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.siswa_dropdown = None
        self.main_page = page
        self.route = "/mutasi"

        self.jenis_dropdown = ft.Dropdown(
            label="Jenis Mutasi",
            width=200,
            on_change=self.on_jenis_change,
            options=[
                ft.dropdown.Option(MUTASI_MASUK, "MASUK"),
                ft.dropdown.Option(MUTASI_KELUAR, "KELUAR"),
            ]
        )

        self.form_container = ft.Column()

        # Table for mutasi keluar
        self.mutasi_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Tanggal")),
                ft.DataColumn(ft.Text("Nama Siswa")),
                ft.DataColumn(ft.Text("Kelas")),
                ft.DataColumn(ft.Text("Alasan")),
            ],
            rows=[]
        )

        self.load_mutasi_keluar()

        self.controls = [
            ft.AppBar(
                title=ft.Text("Data Mutasi"),
                bgcolor=ft.colors.BLUE_700,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/dashboard"))
            ),
            ft.Container(
                padding=20,
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Text("Form Mutasi", size=18, weight=ft.FontWeight.BOLD),
                        self.jenis_dropdown,
                        self.form_container,
                        ft.Divider(),
                        ft.Text("Daftar Mutasi Keluar", size=18, weight=ft.FontWeight.BOLD),
                        self.mutasi_table
                    ]
                )
            )
        ]

    def on_jenis_change(self, e):
        self.form_container.controls.clear()

        if self.jenis_dropdown.value == MUTASI_KELUAR:
            self.build_form_keluar()
        elif self.jenis_dropdown.value == MUTASI_MASUK:
            self.build_form_masuk()

        self.page.update()

    def build_form_keluar(self):
        siswa_list = db.get_all_siswa()

        self.siswa_dropdown = ft.Dropdown(
            label="Pilih Siswa",
            width=400,
            options=[
                ft.dropdown.Option(s['uuid'], f"{s['nis']} - {s['nama_lengkap']}")
                for s in siswa_list
            ]
        )

        self.kelas_field = ft.TextField(label="Kelas yang Ditinggalkan", width=200)
        self.alasan_field = ft.TextField(label="Alasan Keluar", width=400, multiline=True)

        self.form_container.controls.extend([
            self.siswa_dropdown,
            self.kelas_field,
            self.alasan_field,
            ft.ElevatedButton(
                "Simpan Mutasi Keluar",
                icon=ft.Icons.SAVE,
                on_click=self.save_mutasi_keluar
            )
        ])

    def build_form_masuk(self):
        self.form_container.controls.append(
            ft.Column(
                controls=[
                    ft.Text("Mutasi Masuk - Tambah Data Siswa Baru", size=14),
                    ft.ElevatedButton(
                        "Buka Form Tambah Siswa",
                        icon=ft.Icons.PERSON_ADD,
                        on_click=lambda _: self.page.go("/siswa")
                    )
                ]
            )
        )

    def save_mutasi_keluar(self, e):
        if not all([self.siswa_dropdown.value, self.kelas_field.value]):
            return

        data = {
            'jenis_mutasi': MUTASI_KELUAR,
            'uuid_siswa': self.siswa_dropdown.value,
            'kelas_ditinggalkan': self.kelas_field.value,
            'alasan': self.alasan_field.value
        }

        db.save_mutasi(data)
        self.load_mutasi_keluar()

        # Reset form
        self.siswa_dropdown.value = None
        self.kelas_field.value = ""
        self.alasan_field.value = ""

        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Mutasi keluar berhasil dicatat!"),
            bgcolor=ft.colors.GREEN_700
        )
        self.page.snack_bar.open = True
        self.page.update()

    def load_mutasi_keluar(self):
        mutasi_list = db.get_mutasi_keluar()
        self.mutasi_table.rows.clear()

        for m in mutasi_list:
            self.mutasi_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(m['tanggal_mutasi'])[:10])),
                        ft.DataCell(ft.Text(m['nama_lengkap'])),
                        ft.DataCell(ft.Text(m['kelas_ditinggalkan'] or "-")),
                        ft.DataCell(ft.Text(m['alasan'] or "-")),
                    ]
                )
            )