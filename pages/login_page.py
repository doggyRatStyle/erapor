import flet as ft
from gas_service import gas_service
from database import db
from auth import auth_manager


class LoginPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.main_page = page
        self.route = "/login"

        self.email_field = ft.TextField(
            label="Email",
            hint_text="Masukkan email Anda",
            prefix_icon=ft.Icons.EMAIL,
            keyboard_type=ft.KeyboardType.EMAIL,
            width=350
        )

        self.password_field = ft.TextField(
            label="Password",
            hint_text="Masukkan password",
            prefix_icon=ft.Icons.LOCK,
            password=True,
            can_reveal_password=True,
            width=350
        )

        self.error_text = ft.Text(color=ft.Colors.RED_500, size=12)
        self.loading = ft.ProgressRing(visible=False, width=20, height=20)

        self.controls = [
            ft.Container(
                expand=True,
                alignment=ft.alignment.Alignment.CENTER,
                content=ft.Card(
                    elevation=5,
                    content=ft.Container(
                        padding=40,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                            controls=[
                                ft.Icon(ft.Icons.SCHOOL, size=80, color=ft.Colors.BLUE_700),
                                ft.Text("e-Rapor Digital", size=28, weight=ft.FontWeight.BOLD),
                                ft.Text("Sistem Rapor Elektronik", size=14, color=ft.Colors.GREY_600),
                                ft.Divider(),
                                self.email_field,
                                self.password_field,
                                self.error_text,
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        self.loading,
                                        ft.ElevatedButton(
                                            "Login",
                                            icon=ft.Icons.LOGIN,
                                            on_click=self.login_click,
                                            style=ft.ButtonStyle(
                                                padding=ft.padding.symmetric(horizontal=40, vertical=15)
                                            )
                                        )
                                    ]
                                ),
                                ft.TextButton(
                                    "Belum punya akun? Register",
                                    on_click=lambda _: page.go("/register")
                                )
                            ]
                        )
                    )
                )
            )
        ]

    def login_click(self, e):
        self.error_text.value = ""
        self.loading.visible = True
        self.page.update()

        email = self.email_field.value.strip()
        password = self.password_field.value

        if not email or not password:
            self.error_text.value = "Email dan password harus diisi!"
            self.loading.visible = False
            self.page.update()
            return

        # Call GAS Login
        result = gas_service.login(email, password)

        if result['success']:
            token = auth_manager.generate_token(result['user']['email'])
            # Save session
            user_data = {
                'token': result['token'],
                'email': result['user']['email'],
                'nama_lengkap': result['user']['nama_lengkap'],
                'account_type': result['user'].get('account_type', 'Free')
            }
            db.save_session(user_data)

            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Selamat datang, {user_data['nama_lengkap']}!"),
                bgcolor=ft.Colors.GREEN_700
            )
            self.page.snack_bar.open = True
            self.page.go("/dashboard")
        else:
            self.error_text.value = result['message']
            self.loading.visible = False
            self.page.update()
