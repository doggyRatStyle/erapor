import asyncio
import flet as ft

import traceback
import json
import os
import sys

from auth import auth_manager
from database import db
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.dashboard import DashboardPage
from pages.sekolah_page import SekolahPage
from pages.siswa_page import SiswaPage
from pages.mapel_page import MapelPage
from pages.ekskul_page import EkskulPage
from pages.tp_page import TPPage
from pages.lm_page import LMPage
from pages.formatif_page import FormatifPage
from pages.sumatif_page import SumatifPage
from pages.nilai_ekskul_page import NilaiEkskulPage
from pages.nilai_akhir_page import NilaiAkhirPage
from pages.rapor_pages import SampulRaporPage, RaporPage, BukuIndukPage
from pages.mutasi_page import MutasiPage


def main(page: ft.Page):
    # Debug mode
    page.title = "e-Rapor Digital"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20  # Jangan 0 untuk debug
    page.spacing = 10
    page.window_width = 1200
    page.window_height = 800

    # Tampilkan versi Flet
    print(f"Flet version: {ft.version}")
    print(f"Python version: {sys.version}")

    def route_change(route):
        try:
            print(f"Route change: {page.route}")
            page.views.clear()

            # Check session
            session = db.load_session()
            print(f"Session: {session}")

            routes = {
                "/login": LoginPage,
                "/register": RegisterPage,
                "/dashboard": DashboardPage,
                "/sekolah": SekolahPage,
                "/siswa": SiswaPage,
                "/mapel": MapelPage,
                "/ekskul": EkskulPage,
                "/tp": TPPage,
                "/lm": LMPage,
                "/formatif": FormatifPage,
                "/sumatif": SumatifPage,
                "/nilai-ekskul": NilaiEkskulPage,
                "/nilai-akhir": NilaiAkhirPage,
                "/sampul-rapor": SampulRaporPage,
                "/rapor": RaporPage,
                "/buku-induk": BukuIndukPage,
                "/mutasi": MutasiPage,
            }

            path = page.route or "/login"
            print(f"Navigating to: {path}")

            # Check auth untuk protected routes
            protected = ["/dashboard", "/sekolah", "/siswa", "/mapel", "/ekskul",
                         "/tp", "/lm", "/formatif", "/sumatif", "/nilai-ekskul",
                         "/nilai-akhir", "/sampul-rapor", "/rapor", "/buku-induk", "/mutasi"]

            if path in protected and not session:
                print("Redirect to login - no session")
                page.views.append(LoginPage(page))
            elif path in routes:
                print(f"Loading page: {path}")
                try:
                    view = routes[path](page)
                    print(f"View created: {type(view)}")
                    page.views.append(view)
                    print(f"View appended, controls count: {len(view.controls)}")
                except Exception as e:
                    print(f"Error creating view: {e}")
                    traceback.print_exc()
                    # Show error page
                    page.views.append(ft.View(
                        "/error",
                        [ft.Text(f"Error: {str(e)}", color=ft.colors.RED)]
                    ))
            else:
                print(f"Unknown route: {path}, redirecting to login")
                page.views.append(LoginPage(page))

            page.update()
            print("Page updated")

        except Exception as e:
            print(f"Critical error in route_change: {e}")
            traceback.print_exc()
            page.views.append(ft.View(
                "/error",
                [ft.Text(f"Critical Error: {str(e)}", color=ft.colors.RED_500, size=20)]
            ))
            page.update()

    def view_pop(view):
        page.views.pop()
        if page.views:
            top_view = page.views[-1]
            page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Initial route
    asyncio.create_task(
        page.push_route("/")
    )


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")

# import flet as ft
#
#
# def main(page: ft.Page):
#     ornament = ft.Container(
#         ft.LinearGradient(
#             begin=ft.alignment.Alignment.TOP_LEFT,
#             end=ft.alignment.Alignment.BOTTOM_RIGHT,
#             colors=[
#                 ft.Colors.with_opacity(0.3, ft.Colors.PURPLE_50),
#                 ft.Colors.with_opacity(0.3, ft.Colors.BLUE_50)
#             ]
#         ),
#         expand=True,
#     )
#
#     wave_shape = ft.Container(
#         bgcolor=ft.Colors.WHITE,
#         height=200,
#         bottom=0,
#         left=0,
#         right=0,
#         border_radius=ft.BorderRadius.only(
#             top_left=100,
#             top_right=100,
#             bottom_left=0,
#             bottom_right=0
#         ),
#     )
#
#     login_page = ft.Card(
#         content=ft.Container(
#             padding=10,
#             content=ft.Column(
#                 controls=[
#                     ft.Row(
#                         controls=[
#                             ft.Image(
#                                 src="assets/challenge.png",
#                                 width=150,
#                                 height=150
#                             ),
#                         ],
#                         alignment=ft.MainAxisAlignment.CENTER
#                     ),
#                     ft.TextField(
#                         label="Username",
#                         hint_text="Username",
#                         prefix_icon=ft.Icon(ft.Icons.ACCOUNT_CIRCLE),
#                         expand=True
#                     ),
#                     ft.TextField(
#                         label="Password",
#                         hint_text="Password",
#                         password=True,
#                         prefix_icon=ft.Icon(ft.Icons.LOCK),
#                         can_reveal_password=True,
#                         expand=True
#                     ),
#                     ft.Row(
#                         controls=[
#                             ft.Button(
#                                 content="Login",
#                                 bgcolor=ft.Colors.INDIGO_300,
#                                 color=ft.Colors.WHITE_54
#                             )
#                         ],
#                         alignment=ft.MainAxisAlignment.END
#                     )
#
#                 ]
#             )
#         ),
#         # scroll=ft.ScrollMode.AUTO,
#         # spacing=10
#     )
#
#     welcome = ft.Text("Happy to see you again!"),
#
#     stack = ft.Stack(
#         [
#             ornament,
#             welcome,
#             wave_shape,
#             login_page
#         ]
#     )
#
#     page.add(stack)
#
#
# ft.run(main)
