import flet as ft
from database import db
from config import KKTP_TERCAPAI, KKTP_TIDAK_TERCAPAI, TAMPIL_DI_RAPOR, TIDAK_TAMPIL_DI_RAPOR


class FormatifPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.main_page = page
        self.route = "/formatif"

        # Dropdowns
        self.siswa_dropdown = ft.Dropdown(
            label="Pilih Siswa",
            width=300,
            on_change=self.on_siswa_change
        )

        self.mapel_dropdown = ft.Dropdown(
            label="Pilih Mata Pelajaran",
            width=300,
            on_change=self.on_mapel_change
        )

        self.load_siswa_options()
        self.load_mapel_options()

        # TP List with inputs
        self.tp_container = ft.Column(scroll=ft.ScrollMode.AUTO, height=400)

        self.controls = [
            ft.AppBar(
                title=ft.Text("Asesmen Formatif"),
                bgcolor=ft.Colors.BLUE_700,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/dashboard"))
            ),
            ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Text("Input Asesmen Formatif", size=18, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            controls=[
                                self.siswa_dropdown,
                                self.mapel_dropdown
                            ]
                        ),
                        ft.Divider(),
                        ft.Text("Tujuan Pembelajaran & KKTP", size=16, weight=ft.FontWeight.W_500),
                        self.tp_container,
                        ft.ElevatedButton(
                            "Simpan Semua",
                            icon=ft.Icons.SAVE,
                            on_click=self.save_all_formatif
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

    def load_mapel_options(self):
        mapel_list = db.get_all_mapel()
        self.mapel_dropdown.options = [
            ft.dropdown.Option(mapel['id_mapel'], mapel['nama_mapel'])
            for mapel in mapel_list
        ]

    def on_siswa_change(self, e):
        self.load_tp_inputs()

    def on_mapel_change(self, e):
        self.load_tp_inputs()

    def load_tp_inputs(self):
        if not self.mapel_dropdown.value:
            return

        id_mapel = self.mapel_dropdown.value
        tp_list = db.get_tp_by_mapel(id_mapel)

        self.tp_container.controls.clear()

        for tp in tp_list:
            # Check if already exists
            existing = db.get_formatif_by_siswa_mapel(
                self.siswa_dropdown.value or '', id_mapel
            )

            existing_data = next((x for x in existing if x['id_tp'] == tp['id_tp']), None)

            kktp_value = existing_data['kktp'] if existing_data else KKTP_TERCAPAI
            tampil_value = existing_data['tampil_di_rapor'] if existing_data else TAMPIL_DI_RAPOR

            kktp_dropdown = ft.Dropdown(
                label="KKTP",
                width=150,
                value=kktp_value,
                data_tp=tp['id_tp'],  # Custom attribute
                options=[
                    ft.dropdown.Option(KKTP_TERCAPAI, "Tercapai (1)"),
                    ft.dropdown.Option(KKTP_TIDAK_TERCAPAI, "Tidak Tercapai (0)")
                ]
            )

            tampil_dropdown = ft.Dropdown(
                label="Tampil di Rapor",
                width=150,
                value=tampil_value,
                data_tp=tp['id_tp'],
                options=[
                    ft.dropdown.Option(TAMPIL_DI_RAPOR, "Tampil (1)"),
                    ft.dropdown.Option(TIDAK_TAMPIL_DI_RAPOR, "Tidak Tampil (0)")
                ]
            )

            self.tp_container.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Column(
                            controls=[
                                ft.Text(f"{tp['id_tp']}", weight=ft.FontWeight.BOLD),
                                ft.Text(tp['tujuan_pembelajaran'], size=12),
                                ft.Row(
                                    controls=[kktp_dropdown, tampil_dropdown]
                                )
                            ]
                        )
                    )
                )
            )

        self.page.update()

    def save_all_formatif(self, e):
        if not self.siswa_dropdown.value or not self.mapel_dropdown.value:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Pilih siswa dan mata pelajaran terlebih dahulu!"),
                bgcolor=ft.Colors.RED_700
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        saved_count = 0

        for card in self.tp_container.controls:
            tp_id = card.content.content.controls[0].value
            kktp = card.content.content.controls[2].controls[0].value
            tampil = card.content.content.controls[2].controls[1].value

            data = {
                'uuid_siswa': self.siswa_dropdown.value,
                'id_mapel': self.mapel_dropdown.value,
                'id_tp': tp_id,
                'kktp': kktp,
                'tampil_di_rapor': tampil
            }

            db.save_formatif(data)
            saved_count += 1

        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Berhasil menyimpan {saved_count} data formatif!"),
            bgcolor=ft.Colors.GREEN_700
        )
        self.page.snack_bar.open = True
        self.page.update()