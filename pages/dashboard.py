import flet as ft
from database import db
from auth import auth_manager


class DashboardPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.session = None
        self.main_page = page
        self.route = "/dashboard"

        self.user = auth_manager.get_current_user()
        if not self.user:
            page.go("/login")
            return

        self.user = db.load_session()

        # Navigation Rail
        self.nav_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.DASHBOARD_OUTLINED,
                    selected_icon=ft.Icons.DASHBOARD,
                    label="Dashboard",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SCHOOL_OUTLINED,
                    selected_icon=ft.Icons.SCHOOL,
                    label="Data Utama",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.ASSESSMENT_OUTLINED,
                    selected_icon=ft.Icons.ASSESSMENT,
                    label="Input Nilai",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.PICTURE_AS_PDF_OUTLINED,
                    selected_icon=ft.Icons.PICTURE_AS_PDF,
                    label="Output",
                ),
            ],
            on_change=self.nav_change,
        )

        # Content area
        self.content_area = ft.Container(expand=True, content=self.build_dashboard_home())

        # AppBar
        self.appbar = ft.AppBar(
            title=ft.Text("e-Rapor Digital"),
            center_title=False,
            bgcolor=ft.Colors.BLUE_700,
            actions=[
                ft.PopupMenuButton(
                    icon=ft.Icons.PERSON,
                    items=[
                        ft.PopupMenuItem(
                            text=f"Logged in as: {self.session['nama_lengkap']}",
                            disabled=True
                        ),
                        ft.PopupMenuItem(
                            text=f"Account: {self.session['account_type']}",
                            disabled=True
                        ),
                        ft.PopupMenuItemDivider(),
                        ft.PopupMenuItem(
                            text="Logout",
                            icon=ft.Icons.LOGOUT,
                            on_click=self.logout
                        ),
                    ]
                )
            ]
        )

        self.controls = [
            ft.Row(
                expand=True,
                controls=[
                    self.nav_rail,
                    ft.VerticalDivider(width=1),
                    self.content_area
                ]
            )
        ]

    def build_dashboard_home(self):
        return ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    padding=20,
                    content=ft.Column(
                        controls=[
                            ft.Text(f"Selamat Datang, {self.session['nama_lengkap']}!",
                                    size=24, weight=ft.FontWeight.BOLD),
                            ft.Text("Ringkasan Data", size=18, weight=ft.FontWeight.W_500),
                            ft.Row(
                                controls=[
                                    self.build_stat_card("Total Siswa", "0", ft.Icons.PEOPLE, ft.Colors.BLUE),
                                    self.build_stat_card("Mata Pelajaran", "0", ft.Icons.BOOK, ft.Colors.GREEN),
                                    self.build_stat_card("Ekstrakurikuler", "0", ft.Icons.SPORTS, ft.Colors.ORANGE),
                                ]
                            ),
                            ft.Divider(),
                            ft.Text("Menu Cepat", size=18, weight=ft.FontWeight.W_500),
                            ft.Row(
                                wrap=True,
                                spacing=10,
                                controls=[
                                    ft.ElevatedButton(
                                        "Input Data Sekolah",
                                        icon=ft.Icons.SCHOOL,
                                        on_click=lambda _: self.page.go("/sekolah")
                                    ),
                                    ft.ElevatedButton(
                                        "Input Data Siswa",
                                        icon=ft.Icons.PEOPLE,
                                        on_click=lambda _: self.page.go("/siswa")
                                    ),
                                    ft.ElevatedButton(
                                        "Input Nilai",
                                        icon=ft.Icons.ASSESSMENT,
                                        on_click=lambda _: self.page.go("/formatif")
                                    ),
                                    ft.ElevatedButton(
                                        "Cetak Rapor",
                                        icon=ft.Icons.PRINT,
                                        on_click=lambda _: self.page.go("/rapor")
                                    ),
                                ]
                            )
                        ]
                    )
                )
            ]
        )

    def build_stat_card(self, title, value, icon, color):
        return ft.Card(
            content=ft.Container(
                padding=20,
                width=200,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(icon, size=40, color=color),
                        ft.Text(value, size=32, weight=ft.FontWeight.BOLD),
                        ft.Text(title, size=14, color=ft.Colors.GREY_600)
                    ]
                )
            )
        )

    def nav_change(self, e):
        index = e.control.selected_index
        if index == 0:
            self.content_area.content = self.build_dashboard_home()
        elif index == 1:
            self.content_area.content = self.build_data_utama_menu()
        elif index == 2:
            self.content_area.content = self.build_input_nilai_menu()
        elif index == 3:
            self.content_area.content = self.build_output_menu()
        self.page.update()

    def build_data_utama_menu(self):
        return ft.Container(
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text("Data Utama", size=24, weight=ft.FontWeight.BOLD),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.SCHOOL),
                        title=ft.Text("Data Sekolah"),
                        subtitle=ft.Text("Informasi identitas sekolah"),
                        on_click=lambda _: self.page.go("/sekolah")
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.PEOPLE),
                        title=ft.Text("Data Siswa"),
                        subtitle=ft.Text("Data peserta didik"),
                        on_click=lambda _: self.page.go("/siswa")
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.BOOK),
                        title=ft.Text("Data Intrakurikuler"),
                        subtitle=ft.Text("Mata pelajaran"),
                        on_click=lambda _: self.page.go("/mapel")
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.SPORTS),
                        title=ft.Text("Data Ekstrakurikuler"),
                        subtitle=ft.Text("Kegiatan ekstrakurikuler"),
                        on_click=lambda _: self.page.go("/ekskul")
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.TARGET),
                        title=ft.Text("Data Tujuan Pembelajaran"),
                        subtitle=ft.Text("Capaian pembelajaran"),
                        on_click=lambda _: self.page.go("/tp")
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.MENU_BOOK),
                        title=ft.Text("Data Lingkup Materi"),
                        subtitle=ft.Text("Materi pembelajaran"),
                        on_click=lambda _: self.page.go("/lm")
                    ),
                ]
            )
        )

    def build_input_nilai_menu(self):
        return ft.Container(
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text("Input Nilai", size=24, weight=ft.FontWeight.BOLD),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.FORMAT_LIST_BULLETED),
                        title=ft.Text("Asesmen Formatif"),
                        subtitle=ft.Text("Input capaian tujuan pembelajaran"),
                        on_click=lambda _: self.page.go("/formatif")
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.NUMBERS),
                        title=ft.Text("Asesmen Sumatif"),
                        subtitle=ft.Text("Input nilai sumatif"),
                        on_click=lambda _: self.page.go("/sumatif")
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.SCOREBOARD),
                        title=ft.Text("Nilai Ekstrakurikuler"),
                        subtitle=ft.Text("Input nilai kegiatan ekstrakurikuler"),
                        on_click=lambda _: self.page.go("/nilai-ekskul")
                    ),
                ]
            )
        )

    def build_output_menu(self):
        return ft.Container(
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text("Output Data", size=24, weight=ft.FontWeight.BOLD),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.CALCULATE),
                        title=ft.Text("Nilai Akhir"),
                        subtitle=ft.Text("Rekapitulasi nilai akhir"),
                        on_click=lambda _: self.page.go("/nilai-akhir")
                    ),
                    ft.ListTile(
                        leading=ft.Icons.Icons.COVER_IMAGE if hasattr(ft.icons, 'COVER_IMAGE') else ft.Icon(
                            ft.Icons.IMAGE),
                        title=ft.Text("Sampul Rapor"),
                        subtitle=ft.Text("Cover dan profil siswa"),
                        on_click=lambda _: self.page.go("/sampul-rapor")
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.DESCRIPTION),
                        title=ft.Text("Rapor"),
                        subtitle=ft.Text("Laporan hasil belajar"),
                        on_click=lambda _: self.page.go("/rapor")
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.BOOK),
                        title=ft.Text("Buku Induk"),
                        subtitle=ft.Text("Data induk siswa"),
                        on_click=lambda _: self.page.go("/buku-induk")
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.SWAP_HORIZ),
                        title=ft.Text("Data Mutasi"),
                        subtitle=ft.Text("Mutasi masuk/keluar"),
                        on_click=lambda _: self.page.go("/mutasi")
                    ),
                ]
            )
        )

    def logout(self, e):
        db.clear_session()
        self.page.go("/login")