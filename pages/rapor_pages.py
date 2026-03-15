import flet as ft
from database import db
from models import siswa


class SampulRaporPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.main_page = page
        self.route = "/sampul-rapor"

        self.siswa_dropdown = ft.Dropdown(
            label="Pilih Siswa",
            width=400,
            on_change=self.on_siswa_change
        )

        self.load_siswa_options()

        self.preview_container = ft.Column()

        self.controls = [
            ft.AppBar(
                title=ft.Text("Sampul Rapor"),
                bgcolor=ft.Colors.BLUE_700,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/dashboard")),
                actions=[
                    ft.IconButton(ft.Icons.PRINT, tooltip="Cetak")
                ]
            ),
            ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        self.siswa_dropdown,
                        ft.Divider(),
                        ft.Container(
                            bgcolor=ft.Colors.WHITE,
                            padding=40,
                            border=ft.border.all(1, ft.Colors.BLACK),
                            content=self.preview_container
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
        if not self.siswa_dropdown.value:
            return

        siswa = db.get_siswa_by_uuid(self.siswa_dropdown.value)
        sekolah = db.get_sekolah()

        if not siswa or not sekolah:
            return

        jenjang = "SMP"  # Detect from sekolah name or setting

        self.preview_container.controls = [
            # Cover Page
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Icon(ft.Icons.SCHOOL, size=100, color=ft.Colors.BLUE_700),
                    ft.Text("RAPOR PESERTA DIDIK", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text(f"JENJANG {jenjang}", size=18),
                    ft.Divider(height=40),
                    ft.Text(siswa['nama_lengkap'], size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(f"NIS: {siswa['nis']} / NISN: {siswa['nisn']}", size=14),
                    ft.Divider(height=40),
                    ft.Text("KEMENTERIAN PENDIDIKAN DASAR DAN MENENGAH", size=12),
                    ft.Text("REPUBLIK INDONESIA", size=12, weight=ft.FontWeight.BOLD),
                ]
            ),
            ft.Divider(height=60),
            # Profile Page
            ft.Column(
                controls=[
                    ft.Text("PROFIL PESERTA DIDIK", size=18, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    self.build_profile_row("Nama Lengkap", siswa['nama_lengkap']),
                    self.build_profile_row("NIS", siswa['nis']),
                    self.build_profile_row("NISN", siswa['nisn']),
                    self.build_profile_row("Tempat, Tanggal Lahir",
                                           f"{siswa['tempat_lahir']}, {siswa['tanggal_lahir']}"),
                    self.build_profile_row("Jenis Kelamin",
                                           "Laki-laki" if siswa['jenis_kelamin'] == 'L' else "Perempuan"),
                    self.build_profile_row("Agama", siswa['agama']),
                    self.build_profile_row("Alamat", siswa['alamat_siswa']),
                    ft.Divider(),
                    ft.Text("ORANG TUA", size=14, weight=ft.FontWeight.BOLD),
                    self.build_profile_row("Nama Ayah", siswa['nama_ayah']),
                    self.build_profile_row("Nama Ibu", siswa['nama_ibu']),
                    self.build_profile_row("Pekerjaan Ayah", siswa['pekerjaan_ayah']),
                    self.build_profile_row("Pekerjaan Ibu", siswa['pekerjaan_ibu']),
                    self.build_profile_row("Alamat", f"{siswa['alamat_ortu_jalan']}, {siswa['alamat_ortu_kelurahan']}"),
                ]
            )
        ]

        self.page.update()

    def build_profile_row(self, label, value):
        return ft.Row(
            controls=[
                ft.Text(label, width=150, weight=ft.FontWeight.BOLD),
                ft.Text(": "),
                ft.Text(value or "-", expand=True)
            ]
        )


class RaporPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.main_page = page
        self.route = "/rapor"

        self.siswa_dropdown = ft.Dropdown(
            label="Pilih Siswa",
            width=400,
            on_change=self.on_siswa_change
        )

        self.load_siswa_options()

        self.rapor_container = ft.Column()

        self.controls = [
            ft.AppBar(
                title=ft.Text("Rapor"),
                bgcolor=ft.Colors.BLUE_700,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/dashboard")),
                actions=[
                    ft.IconButton(ft.Icons.PRINT, tooltip="Cetak Rapor"),
                    ft.IconButton(ft.Icons.DOWNLOAD, tooltip="Download PDF")
                ]
            ),
            ft.Container(
                expand=True,
                padding=20,
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        self.siswa_dropdown,
                        ft.Container(
                            bgcolor=ft.Colors.WHITE,
                            padding=30,
                            border=ft.border.all(1, ft.Colors.BLACK),
                            content=self.rapor_container
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
        if not self.siswa_dropdown.value:
            return

        siswa = db.get_siswa_by_uuid(self.siswa_dropdown.value)
        sekolah = db.get_sekolah()

        if not siswa or not sekolah:
            return

        # Build Rapor Content
        self.rapor_container.controls = [
            # Header Info
            ft.Row(
                controls=[
                    ft.Column(
                        width=300,
                        controls=[
                            ft.Text(f"Nama: {siswa['nama_lengkap']}"),
                            ft.Text(f"NISN: {siswa['nisn']}"),
                            ft.Text(f"Sekolah: {sekolah['nama_sekolah']}"),
                            ft.Text(f"Alamat: {sekolah['alamat'][:30]}..."),
                        ]
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(f"Kelas: {sekolah['kelas']}"),
                            ft.Text(f"Fase: {sekolah['fase']}"),
                            ft.Text(f"Semester: {sekolah['semester']}"),
                            ft.Text(f"Tahun Pelajaran: {sekolah['tahun_ajaran']}"),
                        ]
                    )
                ]
            ),
            ft.Divider(),
            ft.Text("A. Laporan Hasil Belajar", size=16, weight=ft.FontWeight.BOLD),
            self.build_nilai_table(siswa['uuid']),
            ft.Divider(),
            ft.Text("B. Ekstrakurikuler", size=16, weight=ft.FontWeight.BOLD),
            self.build_ekskul_table(siswa['uuid']),
            ft.Divider(),
            ft.Text("C. Kehadiran", size=16, weight=ft.FontWeight.BOLD),
            self.build_kehadiran(siswa['uuid']),
            ft.Divider(),
            ft.Text("D. Tanda Tangan", size=16, weight=ft.FontWeight.BOLD),
            self.build_tanda_tangan(sekolah, siswa),
        ]

        self.page.update()

    def build_nilai_table(self, uuid_siswa):
        mapel_list = db.get_all_mapel()

        rows = []
        for idx, mapel in enumerate(mapel_list, 1):
            # Get nilai
            sumatif_data = db.get_sumatif_by_siswa_mapel(uuid_siswa, mapel['id_mapel'])
            nilai_list = [s['nilai'] for s in sumatif_data if s['nilai']]
            rata_rata = sum(nilai_list) / len(nilai_list) if nilai_list else 0

            # Get capaian from formatif
            formatif_data = db.get_formatif_by_siswa_mapel(uuid_siswa, mapel['id_mapel'])
            capaian = self.build_capaian_text(siswa['nama_lengkap'], formatif_data)

            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(idx))),
                        ft.DataCell(ft.Text(mapel['nama_mapel'])),
                        ft.DataCell(ft.Text(f"{rata_rata:.0f}")),
                        ft.DataCell(ft.Text(capaian, size=10)),
                    ]
                )
            )

        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("No")),
                ft.DataColumn(ft.Text("Muatan Pelajaran")),
                ft.DataColumn(ft.Text("Nilai Akhir")),
                ft.DataColumn(ft.Text("Capaian Kompetensi")),
            ],
            rows=rows
        )

    def build_capaian_text(self, nama_siswa, formatif_data):
        tercapai = []
        tidak_tercapai = []

        for f in formatif_data:
            if f['kktp'] == '1' and f['tampil_di_rapor'] == '1':
                tercapai.append(f['tujuan_pembelajaran'][:30])
            elif f['kktp'] == '0' and f['tampil_di_rapor'] == '1':
                tidak_tercapai.append(f['tujuan_pembelajaran'][:30])

        text = []
        if tercapai:
            text.append(f"Ananda {nama_siswa} menunjukkan pemahaman dalam: {', '.join(tercapai[:2])}")
        if tidak_tercapai:
            text.append(f"Ananda {nama_siswa} membutuhkan bimbingan dalam: {', '.join(tidak_tercapai[:2])}")

        return " ".join(text) if text else "Capaian kompetensi sesuai standar"

    def build_ekskul_table(self, uuid_siswa):
        nilai_ekskul = db.get_nilai_ekskul_by_siswa(uuid_siswa)

        rows = []
        for idx, ne in enumerate(nilai_ekskul, 1):
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(idx))),
                        ft.DataCell(ft.Text(ne['nama_ekskul'])),
                        ft.DataCell(ft.Text(ne['deskripsi'] or f"Ananda telah mengikuti kegiatan {ne['nama_ekskul']}")),
                    ]
                )
            )

        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("No")),
                ft.DataColumn(ft.Text("Ekstrakurikuler")),
                ft.DataColumn(ft.Text("Keterangan")),
            ],
            rows=rows if rows else [ft.DataRow(
                cells=[ft.DataCell(ft.Text("-")), ft.DataCell(ft.Text("Tidak ada data")), ft.DataCell(ft.Text("-"))])]
        )

    def build_kehadiran(self, uuid_siswa):
        # Get from database or default
        return ft.Column(
            controls=[
                ft.Text("Sakit: 0 hari"),
                ft.Text("Ijin: 0 hari"),
                ft.Text("Tanpa Keterangan: 0 hari"),
            ]
        )

    def build_tanda_tangan(self, sekolah, siswa):
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Orang Tua/Wali"),
                        ft.Divider(height=40),
                        ft.Text(siswa['nama_ayah'] or "..................."),
                    ]
                ),
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(f"Mengetahui,"),
                        ft.Text("Kepala Sekolah"),
                        ft.Divider(height=40),
                        ft.Text(sekolah['nama_kepala_sekolah'] or "..................."),
                        ft.Text(f"NIP. {sekolah['nip_kepala_sekolah'] or '...................'}"),
                    ]
                ),
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(sekolah['tempat_tanggal_rapor'] or ".................."),
                        ft.Text("Wali Kelas"),
                        ft.Divider(height=40),
                        ft.Text(sekolah['nama_wali_kelas'] or "..................."),
                        ft.Text(f"NIP. {sekolah['nip_wali_kelas'] or '...................'}"),
                    ]
                ),
            ]
        )


class BukuIndukPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.main_page = page
        self.route = "/buku-induk"

        self.siswa_dropdown = ft.Dropdown(
            label="Pilih Siswa",
            width=400,
            on_change=self.on_siswa_change
        )

        self.load_siswa_options()

        self.content_container = ft.Column()

        self.controls = [
            ft.AppBar(
                title=ft.Text("Buku Induk"),
                bgcolor=ft.Colors.BLUE_700,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/dashboard")),
                actions=[
                    ft.IconButton(ft.Icons.PRINT, tooltip="Cetak")
                ]
            ),
            ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        self.siswa_dropdown,
                        ft.Container(
                            bgcolor=ft.Colors.WHITE,
                            padding=30,
                            border=ft.border.all(1, ft.Colors.BLACK),
                            content=self.content_container
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
        if not self.siswa_dropdown.value:
            return

        siswa = db.get_siswa_by_uuid(self.siswa_dropdown.value)
        sekolah = db.get_sekolah()

        if not siswa or not sekolah:
            return

        # Build Buku Induk (similar to rapor but without capaian kompetensi)
        self.content_container.controls = [
            ft.Text("BUKU INDUK SISWA", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Divider(),
            # Data Siswa Lengkap
            ft.Text("A. IDENTITAS SISWA", weight=ft.FontWeight.BOLD),
            self.build_info_row("Nama Lengkap", siswa['nama_lengkap']),
            self.build_info_row("NIS", siswa['nis']),
            self.build_info_row("NISN", siswa['nisn']),
            self.build_info_row("Tempat/Tgl Lahir", f"{siswa['tempat_lahir']}, {siswa['tanggal_lahir']}"),
            self.build_info_row("Jenis Kelamin", siswa['jenis_kelamin']),
            self.build_info_row("Agama", siswa['agama']),
            self.build_info_row("Alamat", siswa['alamat_siswa']),
            ft.Divider(),
            ft.Text("B. DATA ORANG TUA", weight=ft.FontWeight.BOLD),
            self.build_info_row("Nama Ayah", siswa['nama_ayah']),
            self.build_info_row("Nama Ibu", siswa['nama_ibu']),
            self.build_info_row("Pekerjaan", f"{siswa['pekerjaan_ayah']} / {siswa['pekerjaan_ibu']}"),
            ft.Divider(),
            ft.Text("C. NILAI AKADEMIK", weight=ft.FontWeight.BOLD),
            self.build_nilai_table(siswa['uuid']),
        ]

        self.page.update()

    def build_info_row(self, label, value):
        return ft.Row(
            controls=[
                ft.Text(label, width=150),
                ft.Text(": "),
                ft.Text(value or "-")
            ]
        )

    def build_nilai_table(self, uuid_siswa):
        mapel_list = db.get_all_mapel()

        rows = []
        for idx, mapel in enumerate(mapel_list, 1):
            sumatif_data = db.get_sumatif_by_siswa_mapel(uuid_siswa, mapel['id_mapel'])
            nilai_list = [s['nilai'] for s in sumatif_data if s['nilai']]
            rata_rata = sum(nilai_list) / len(nilai_list) if nilai_list else 0

            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(idx))),
                        ft.DataCell(ft.Text(mapel['nama_mapel'])),
                        ft.DataCell(ft.Text(f"{rata_rata:.0f}")),
                    ]
                )
            )

        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("No")),
                ft.DataColumn(ft.Text("Mata Pelajaran")),
                ft.DataColumn(ft.Text("Nilai Akhir")),
            ],
            rows=rows
        )