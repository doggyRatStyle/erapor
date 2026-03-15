import flet as ft
from database import db


class NilaiEkskulPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.main_page = page
        self.route = "/nilai-ekskul"

        self.siswa_dropdown = ft.Dropdown(
            label="Pilih Siswa",
            width=400,
            on_change=self.on_siswa_change
        )

        self.load_siswa_options()

        self.ekskul_container = ft.Column(scroll=ft.ScrollMode.AUTO, height=400)

        self.controls = [
            ft.AppBar(
                title=ft.Text("Nilai Ekstrakurikuler"),
                bgcolor=ft.Colors.BLUE_700,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/dashboard"))
            ),
            ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Text("Input Nilai Ekstrakurikuler", size=18, weight=ft.FontWeight.BOLD),
                        self.siswa_dropdown,
                        ft.Divider(),
                        ft.Text("Input per Ekstrakurikuler", size=16),
                        self.ekskul_container,
                        ft.ElevatedButton(
                            "Simpan Nilai Ekskul",
                            icon=ft.Icons.SAVE,
                            on_click=self.save_nilai_ekskul
                        )
                    ]
                )
            )
        ]

    def load_siswa_options(self):
        siswa_list = db.get_all_siswa()
        self.siswa_dropdown.options = [
            ft.dropdown.Option(siswa['uuid'], f"{siswa['nis']} - {siswa['nama_lengkap']}")
            for siswa in siswa_list
        ]

    def on_siswa_change(self, e):
        self.load_ekskul_inputs()

    def load_ekskul_inputs(self):
        ekskul_list = db.get_all_ekskul()
        self.ekskul_container.controls.clear()

        for ekskul in ekskul_list:
            self.ekskul_container.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Column(
                            controls=[
                                ft.Text(ekskul['nama_ekskul'], weight=ft.FontWeight.BOLD),
                                ft.Row(
                                    controls=[
                                        ft.TextField(
                                            label="Nilai (A/B/C/D)",
                                            width=100,
                                            data_ekskul=ekskul['id_ekskul']
                                        ),
                                        ft.TextField(
                                            label="Deskripsi Capaian",
                                            width=400,
                                            multiline=True,
                                            data_ekskul_desc=ekskul['id_ekskul']
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                )
            )

        self.page.update()

    def save_nilai_ekskul(self, e):
        if not self.siswa_dropdown.value:
            return

        saved = 0
        for card in self.ekskul_container.controls:
            ekskul_id = card.content.content.controls[2].controls[0].data_ekskul
            nilai = card.content.content.controls[2].controls[0].value
            deskripsi = card.content.content.controls[2].controls[1].value

            if nilai:
                data = {
                    'uuid_siswa': self.siswa_dropdown.value,
                    'id_ekskul': ekskul_id,
                    'nilai': nilai,
                    'deskripsi': deskripsi,
                    'semester': '1',
                    'tahun_ajaran': '2025/2026'
                }
                db.save_nilai_ekskul(data)
                saved += 1

        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Berhasil menyimpan {saved} nilai ekstrakurikuler!"),
            bgcolor=ft.Colors.GREEN_700
        )
        self.page.snack_bar.open = True
        self.page.update()