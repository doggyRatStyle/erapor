import flet as ft
from database import db


class SekolahPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.main_page = page
        self.route = "/sekolah"

        # Form fields
        self.fields = {}
        field_names = [
            'nama_sekolah', 'npsn', 'nss', 'alamat', 'kode_pos',
            'desa_kelurahan', 'kecamatan', 'kabupaten_kota', 'provinsi',
            'website', 'email', 'nama_kepala_sekolah', 'nip_kepala_sekolah',
            'nama_wali_kelas', 'nip_wali_kelas', 'kelas', 'fase',
            'semester', 'tahun_ajaran', 'tempat_tanggal_rapor'
        ]

        for name in field_names:
            self.fields[name] = ft.TextField(
                label=self.format_label(name),
                width=300 if name not in ['alamat'] else 400
            )

        # Load existing data
        existing = db.get_sekolah()
        if existing:
            for key, value in existing.items():
                if key in self.fields:
                    self.fields[key].value = value

        self.controls = [
            ft.AppBar(
                title=ft.Text("Data Sekolah"),
                bgcolor=ft.Colors.BLUE_700,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/dashboard"))
            ),
            ft.Container(
                expand=True,
                padding=20,
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Text("Informasi Sekolah", size=20, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            wrap=True,
                            spacing=10,
                            controls=[self.fields[name] for name in field_names[:10]]
                        ),
                        ft.Divider(),
                        ft.Text("Informasi Kepala Sekolah & Wali Kelas", size=20, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            wrap=True,
                            spacing=10,
                            controls=[self.fields[name] for name in field_names[10:16]]
                        ),
                        ft.Divider(),
                        ft.Text("Informasi Periode", size=20, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            wrap=True,
                            spacing=10,
                            controls=[self.fields[name] for name in field_names[16:]]
                        ),
                        ft.Divider(),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Simpan",
                                    icon=ft.Icons.SAVE,
                                    on_click=self.save_data,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.GREEN_700,
                                        color=ft.Colors.WHITE
                                    )
                                ),
                                ft.OutlinedButton(
                                    "Reset",
                                    icon=ft.Icons.RESTORE,
                                    on_click=self.reset_form
                                )
                            ]
                        )
                    ]
                )
            )
        ]

    def format_label(self, name):
        labels = {
            'nama_sekolah': 'Nama Sekolah',
            'npsn': 'NPSN',
            'nss': 'NSS',
            'alamat': 'Alamat Sekolah',
            'kode_pos': 'Kode Pos',
            'desa_kelurahan': 'Desa/Kelurahan',
            'kecamatan': 'Kecamatan',
            'kabupaten_kota': 'Kabupaten/Kota',
            'provinsi': 'Provinsi',
            'website': 'Website',
            'email': 'Email',
            'nama_kepala_sekolah': 'Nama Kepala Sekolah',
            'nip_kepala_sekolah': 'NIP Kepala Sekolah',
            'nama_wali_kelas': 'Nama Wali Kelas',
            'nip_wali_kelas': 'NIP Wali Kelas',
            'kelas': 'Kelas',
            'fase': 'Fase',
            'semester': 'Semester',
            'tahun_ajaran': 'Tahun Ajaran',
            'tempat_tanggal_rapor': 'Tempat/Tanggal Rapor'
        }
        return labels.get(name, name.replace('_', ' ').title())

    def save_data(self, e):
        data = {key: field.value for key, field in self.fields.items()}
        db.save_sekolah(data)

        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Data sekolah berhasil disimpan!"),
            bgcolor=ft.Colors.GREEN_700
        )
        self.page.snack_bar.open = True
        self.page.update()

    def reset_form(self, e):
        for field in self.fields.values():
            field.value = ""
        self.page.update()