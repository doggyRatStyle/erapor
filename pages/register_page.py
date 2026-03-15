import flet as ft
from gas_service import gas_service


class RegisterPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.main_page = page
        self.route = "/register"

        self.nama_field = ft.TextField(
            label="Nama Lengkap",
            prefix_icon=ft.Icons.PERSON,
            width=350
        )

        self.hp_field = ft.TextField(
            label="Nomor HP",
            prefix_icon=ft.Icons.PHONE,
            keyboard_type=ft.KeyboardType.PHONE,
            width=350
        )

        self.email_field = ft.TextField(
            label="Email",
            prefix_icon=ft.Icons.EMAIL,
            keyboard_type=ft.KeyboardType.EMAIL,
            width=350
        )

        self.password_field = ft.TextField(
            label="Password",
            prefix_icon=ft.Icons.LOCK,
            password=True,
            can_reveal_password=True,
            width=350
        )

        self.confirm_password = ft.TextField(
            label="Konfirmasi Password",
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            password=True,
            width=350
        )

        self.error_text = ft.Text(color=ft.Colors.RED_500, size=12)
        self.loading = ft.ProgressRing(visible=False, width=20, height=20)

        # OTP Dialog
        self.otp_field = ft.TextField(
            label="Kode OTP",
            hint_text="Masukkan 6 digit kode",
            width=200,
            text_align=ft.TextAlign.CENTER
        )

        self.otp_dialog = ft.AlertDialog(
            title=ft.Text("Verifikasi OTP"),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Text("Kode OTP telah dikirim ke email Anda"),
                    self.otp_field,
                    ft.TextButton("Kirim Ulang OTP", on_click=self.resend_otp)
                ],
                tight=True,
                height=150
            ),
            actions=[
                ft.TextButton("Batal", on_click=self.close_otp_dialog),
                ft.ElevatedButton("Verifikasi", on_click=self.verify_otp)
            ]
        )

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
                            spacing=15,
                            controls=[
                                ft.Icon(ft.Icons.APP_REGISTRATION, size=60, color=ft.Colors.BLUE_700),
                                ft.Text("Register Akun", size=24, weight=ft.FontWeight.BOLD),
                                self.nama_field,
                                self.hp_field,
                                self.email_field,
                                self.password_field,
                                self.confirm_password,
                                self.error_text,
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        self.loading,
                                        ft.ElevatedButton(
                                            "Register",
                                            icon=ft.Icons.PERSON_ADD,
                                            on_click=self.register_click,
                                            style=ft.ButtonStyle(
                                                padding=ft.padding.symmetric(horizontal=40, vertical=15)
                                            )
                                        )
                                    ]
                                ),
                                ft.TextButton(
                                    "Sudah punya akun? Login",
                                    on_click=lambda _: page.go("/login")
                                )
                            ]
                        )
                    )
                )
            )
        ]

    def register_click(self, e):
        self.error_text.value = ""

        # Validation
        if not all([self.nama_field.value, self.hp_field.value,
                    self.email_field.value, self.password_field.value]):
            self.error_text.value = "Semua field harus diisi!"
            self.page.update()
            return

        if self.password_field.value != self.confirm_password.value:
            self.error_text.value = "Password tidak cocok!"
            self.page.update()
            return

        self.loading.visible = True
        self.page.update()

        # Register via GAS
        result = gas_service.register(
            self.nama_field.value,
            self.hp_field.value,
            self.email_field.value,
            self.password_field.value
        )

        self.loading.visible = False

        if result['success']:
            self.page.dialog = self.otp_dialog
            self.otp_dialog.open = True
            self.page.update()
        else:
            self.error_text.value = result['message']
            self.page.update()

    def verify_otp(self, e):
        if not self.otp_field.value:
            return

        result = gas_service.verify_otp(self.email_field.value, self.otp_field.value)

        if result['success']:
            self.otp_dialog.open = False
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Verifikasi berhasil! Silakan login."),
                bgcolor=ft.Colors.GREEN_700
            )
            self.page.snack_bar.open = True
            self.page.go("/login")
        else:
            self.otp_field.error_text = result['message']
            self.page.update()

    def resend_otp(self, e):
        result = gas_service.resend_otp(self.email_field.value)
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(result.get('message', 'OTP dikirim ulang')),
            bgcolor=ft.Colors.BLUE_700
        )
        self.page.snack_bar.open = True
        self.page.update()

    def close_otp_dialog(self, e):
        self.otp_dialog.open = False
        self.page.update()