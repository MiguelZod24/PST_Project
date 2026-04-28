import re
from playwright.sync_api import Page, expect


class LoginPage:
    """Page Object Model para la página de login de Practice Software Testing."""

    def __init__(self, page: Page):
        self.page = page
        # Selectores centralizados aquí para que un cambio en el HTML solo requiera
        # editar este archivo, no todos los tests.
        self.email_input = page.locator("#email")
        self.password_input = page.locator("#password")
        # data-test es la convención más resistente al refactoring de estilos
        self.submit_button = page.locator('[data-test="login-submit"]')
        self.alert_error = page.locator('[data-test="login-error"]')
        # Locators de navegación centralizados en el POM para que los tests no
        # construyan locators en línea; un cambio de selector se resuelve aquí.
        self.forgot_password_link = page.locator('[data-test="forgot-password-link"]')
        self.register_link = page.locator('[data-test="register-link"]')

    def navigate(self) -> None:
        """Navega a /auth/login y espera que el campo email esté visible.

        wait_for con state='visible' garantiza que Angular terminó de montar el
        componente antes de que el test intente interactuar con él; sin esta
        espera, fill() puede lanzar ElementNotFound en cargas lentas.
        El timeout de 90s cubre los runners de CI con CPU/red limitada.
        """
        self.page.goto(
            "https://practicesoftwaretesting.com/auth/login",
            timeout=90_000,
        )
        self.email_input.wait_for(state="visible", timeout=90_000)

    def fill_email(self, email: str) -> None:
        """Rellena el campo #email con el valor dado (reemplaza contenido previo)."""
        self.email_input.fill(email)

    def fill_password(self, password: str) -> None:
        """Rellena el campo #password con el valor dado (reemplaza contenido previo)."""
        self.password_input.fill(password)

    def click_login(self) -> None:
        """Hace clic en el botón submit y espera la primera señal concreta del resultado.

        networkidle es frágil en SPAs porque Angular puede mantener conexiones de
        polling o WebSocket abiertas indefinidamente, haciendo que la espera nunca
        termine o supere el timeout. En su lugar esperamos hasta 8 s al primer
        evento observable: redirección de URL (login OK) o aparición del alert de
        error (login KO). Si ninguno ocurre (p.ej. validación HTML5 bloqueó el
        submit sin producir cambios en el DOM), se captura la excepción y el test
        continúa; sus assertions determinarán el resultado real.
        """
        self.submit_button.click()
        try:
            self.page.wait_for_function(
                """() => {
                    const notOnLogin = !window.location.href.includes('/auth/login');
                    const err = document.querySelector('[data-test="login-error"]');
                    const errorVisible = !!err && err.offsetHeight > 0;
                    return notOnLogin || errorVisible;
                }""",
                timeout=8000,
            )
        except Exception:
            pass

    def login(self, email: str, password: str) -> None:
        """Flujo completo de login: rellena ambos campos y hace clic en submit."""
        self.fill_email(email)
        self.fill_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        """Espera hasta 5 s a que el alert de error sea visible y retorna su texto.

        El timeout cubre la latencia del servidor al rechazar credenciales inválidas.
        """
        self.alert_error.wait_for(state="visible", timeout=5000)
        return self.alert_error.inner_text()

    def is_logged_in(self) -> bool:
        """Retorna True si Angular redirigió al usuario fuera de /auth/login.

        La redirección de URL es la señal inequívoca de que el token JWT fue
        emitido y el estado de sesión se actualizó en el cliente.
        """
        try:
            expect(self.page).not_to_have_url(
                re.compile(r".*/auth/login.*"), timeout=5000
            )
            return True
        except Exception:
            return False

    def get_current_url(self) -> str:
        """Retorna la URL actual de la página."""
        return self.page.url
