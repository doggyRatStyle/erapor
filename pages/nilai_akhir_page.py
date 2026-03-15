import flet as ft
from database import db


class NilaiAkhirPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.main_page = page
        self.route = "/nilai-akhir"

        self.data_table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text("No"))],
            rows=[],
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=5
        )

        self.load_nilai_akhir()

        self.controls = [
            ft.AppBar(
                title=ft.Text("Nilai Akhir"),
                bgcolor=ft.Colors.BLUE_700,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/dashboard")),
                actions=[
                    ft.IconButton(ft.Icons.DOWNLOAD, tooltip="Export Excel")
                ]
            ),
            ft.Container(
                expand=True,
                padding=20,
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Text("Rekapitulasi Nilai Akhir", size=18, weight=ft.FontWeight.BOLD),
                        self.data_table
                    ]
                )
            )
        ]

    def load_nilai_akhir(self):
        siswa_list = db.get_all_siswa()
        mapel_list = db.get_all_mapel()

        # Build columns
        self.data_table.columns = [ft.DataColumn(ft.Text("No"))]
        self.data_table.columns.append(ft.DataColumn(ft.Text("Nama Siswa")))

        for mapel in mapel_list:
            self.data_table.columns.append(ft.DataColumn(ft.Text(mapel['nama_mapel'][:15])))

        # Build rows
        self.data_table.rows.clear()

        for idx, siswa in enumerate(siswa_list, 1):
            cells = [ft.DataCell(ft.Text(str(idx))), ft.DataCell(ft.Text(siswa['nama_lengkap']))]

            for mapel in mapel_list:
                # Calculate average from sumatif
                sumatif_data = db.get_sumatif_by_siswa_mapel(siswa['uuid'], mapel['id_mapel'])

                if sumatif_data:
                    nilai_list = [s['nilai'] for s in sumatif_data if s['nilai']]
                    rata_rata = sum(nilai_list) / len(nilai_list) if nilai_list else 0
                    cells.append(ft.DataCell(ft.Text(f"{rata_rata:.1f}")))
                else:
                    cells.append(ft.DataCell(ft.Text("-")))

            self.data_table.rows.append(ft.DataRow(cells=cells))