import flet as ft
from database import db
from config import SUMATIF_LM, SUMATIF_STS, SUMATIF_SAS


class SumatifPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.main_page = page
        self.route = "/sumatif"

        self.mapel_dropdown = ft.Dropdown(
            label="Pilih Mata Pelajaran",
            width=300,
            on_change=self.on_mapel_change
        )

        self.siswa_dropdown = ft.Dropdown(
            label="Pilih Siswa",
            width=300
        )

        self.jenis_dropdown = ft.Dropdown(
            label="Jenis Sumatif",
            width=200,
            on_change=self.on_jenis_change,
            options=[
                ft.dropdown.Option(SUMATIF_LM, "Lingkup Materi"),
                ft.dropdown.Option(SUMATIF_STS, "STS"),
                ft.dropdown.Option(SUMATIF_SAS, "SAS")
            ]
        )

        self.load_mapel_options()
        self.load_siswa_options()

        self.input_container = ft.Column()

        self.controls = [
            ft.AppBar(
                title=ft.Text("Asesmen Sumatif"),
                bgcolor=ft.Colors.BLUE_700,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/dashboard"))
            ),
            ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Text("Input Asesmen Sumatif", size=18, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            controls=[
                                self.mapel_dropdown,
                                self.siswa_dropdown,
                                self.jenis_dropdown
                            ]
                        ),
                        ft.Divider(),
                        self.input_container,
                        ft.ElevatedButton(
                            "Simpan Nilai",
                            icon=ft.Icons.SAVE,
                            on_click=self.save_sumatif
                        )
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

    def load_siswa_options(self):
        siswa_list = db.get_all_siswa()
        self.siswa_dropdown.options = [
            ft.dropdown.Option(siswa['uuid'], f"{siswa['nis']} - {siswa['nama_lengkap']}")
            for siswa in siswa_list
        ]

    def on_mapel_change(self, e):
        self.on_jenis_change(e)

    def on_jenis_change(self, e):
        self.input_container.controls.clear()

        if not self.jenis_dropdown.value or not self.mapel_dropdown.value:
            return

        jenis = self.jenis_dropdown.value

        if jenis == SUMATIF_LM:
            # Show inputs for each LM
            lm_list = db.get_lm_by_mapel(self.mapel_dropdown.value)

            for lm in lm_list:
                self.input_container.controls.append(
                    ft.Row(
                        controls=[
                            ft.Text(lm['lingkup_materi'], width=300),
                            ft.TextField(
                                label="Nilai",
                                width=100,
                                keyboard_type=ft.KeyboardType.NUMBER,
                                data_lm=lm['id_lm']
                            )
                        ]
                    )
                )
        else:
            # STS or SAS - single input
            self.input_container.controls.append(
                ft.TextField(
                    label=f"Nilai {jenis}",
                    width=150,
                    keyboard_type=ft.KeyboardType.NUMBER
                )
            )

        self.page.update()

    def save_sumatif(self, e):
        if not all([self.mapel_dropdown.value, self.siswa_dropdown.value, self.jenis_dropdown.value]):
            return

        jenis = self.jenis_dropdown.value

        if jenis == SUMATIF_LM:
            for row in self.input_container.controls:
                nilai_field = row.controls[1]
                data = {
                    'uuid_siswa': self.siswa_dropdown.value,
                    'id_mapel': self.mapel_dropdown.value,
                    'jenis_sumatif': jenis,
                    'id_lm': nilai_field.data_lm,
                    'nilai': float(nilai_field.value or 0),
                    'semester': '1',  # Get from sekolah data
                    'tahun_ajaran': '2025/2026'
                }
                db.save_sumatif(data)
        else:
            nilai_field = self.input_container.controls[0]
            data = {
                'uuid_siswa': self.siswa_dropdown.value,
                'id_mapel': self.mapel_dropdown.value,
                'jenis_sumatif': jenis,
                'id_lm': None,
                'nilai': float(nilai_field.value or 0),
                'semester': '1',
                'tahun_ajaran': '2025/2026'
            }
            db.save_sumatif(data)

        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Nilai sumatif berhasil disimpan!"),
            bgcolor=ft.Colors.GREEN_700
        )
        self.page.snack_bar.open = True
        self.page.update()