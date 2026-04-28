import re

import allure
from playwright.sync_api import expect

from pages.login_page import LoginPage

# ---------------------------------------------------------------------------
# Credenciales de prueba (definidas una sola vez para facilitar el mantenimiento)
# ---------------------------------------------------------------------------
CUSTOMER_EMAIL = "customer@practicesoftwaretesting.com"
ADMIN_EMAIL = "admin@practicesoftwaretesting.com"
VALID_PASSWORD = "welcome01"


def _screenshot(login_page: LoginPage, name: str = "captura") -> None:
    """Adjunta una captura de pantalla al reporte Allure en el paso actual."""
    allure.attach(
        login_page.page.screenshot(),
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )


# ===========================================================================
# TC-001 — Login exitoso con rol customer
# ===========================================================================
@allure.epic("Autenticación")
@allure.feature("Módulo Login")
@allure.story("Login exitoso")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC-001 | Login con credenciales válidas (customer)")
@allure.description(
    "Dado un usuario con rol customer y credenciales correctas, "
    "cuando inicia sesión, debe ser redirigido fuera de /auth/login."
)
def test_tc001_login_valid_customer(login_page: LoginPage):
    """
    escenario: El usuario ingresa email y contraseña válidos de un customer y hace clic en Login.
    esperado: El sistema autentica al usuario y lo redirige fuera de la página de login.
    impacto: Si falla, los clientes no pueden acceder a la plataforma.
    accion: Verificar credenciales de prueba y disponibilidad del servidor.
    """
    login_page.navigate()
    login_page.login(CUSTOMER_EMAIL, VALID_PASSWORD)
    # La redirección fuera de /auth/login confirma la autenticación exitosa
    expect(login_page.page).not_to_have_url(re.compile(r".*/auth/login.*"))
    _screenshot(login_page, "TC001_login_customer_exitoso")


# ===========================================================================
# TC-002 — Login exitoso con rol admin
# ===========================================================================
@allure.epic("Autenticación")
@allure.feature("Módulo Login")
@allure.story("Login exitoso")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC-002 | Login con credenciales válidas (admin)")
@allure.description(
    "Dado un usuario con rol admin y credenciales correctas, "
    "cuando inicia sesión, debe ser redirigido fuera de /auth/login."
)
def test_tc002_login_valid_admin(login_page: LoginPage):
    """
    escenario: El usuario ingresa email y contraseña válidos de un admin y hace clic en Login.
    esperado: El sistema autentica al administrador y lo redirige fuera de la página de login.
    impacto: Si falla, los administradores no pueden gestionar la plataforma.
    accion: Verificar credenciales de admin y disponibilidad del servidor.
    """
    login_page.navigate()
    login_page.login(ADMIN_EMAIL, VALID_PASSWORD)
    expect(login_page.page).not_to_have_url(re.compile(r".*/auth/login.*"))
    _screenshot(login_page, "TC002_login_admin_exitoso")


# ===========================================================================
# TC-003 — Login fallido: email incorrecto
# ===========================================================================
@allure.epic("Autenticación")
@allure.feature("Módulo Login")
@allure.story("Login fallido - credenciales inválidas")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC-003 | Login con email incorrecto")
@allure.description(
    "Dado un email que no existe en el sistema, "
    "cuando se intenta iniciar sesión, debe aparecer un mensaje de error "
    "y el usuario debe permanecer en la página de login."
)
def test_tc003_login_wrong_email(login_page: LoginPage):
    """
    escenario: El usuario ingresa un email que no existe en el sistema.
    esperado: El sistema muestra un mensaje de error y el usuario permanece en login.
    impacto: Si falla, usuarios no registrados podrían acceder sin credenciales válidas.
    accion: Revisar la validación de credenciales en el backend.
    """
    login_page.navigate()
    login_page.login("usuarioinexistente@correo.com", VALID_PASSWORD)
    expect(login_page.alert_error).to_be_visible()
    _screenshot(login_page, "TC003_email_incorrecto")


# ===========================================================================
# TC-004 — Login fallido: contraseña incorrecta
# ===========================================================================
@allure.epic("Autenticación")
@allure.feature("Módulo Login")
@allure.story("Login fallido - credenciales inválidas")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC-004 | Login con contraseña incorrecta")
@allure.description(
    "Dado un email válido con contraseña incorrecta, "
    "cuando se intenta iniciar sesión, debe aparecer un mensaje de error."
)
def test_tc004_login_wrong_password(login_page: LoginPage):
    """
    escenario: El usuario ingresa un email válido pero una contraseña incorrecta.
    esperado: El sistema muestra un mensaje de error y el usuario permanece en login.
    impacto: Si falla, la seguridad de las cuentas queda comprometida.
    accion: Revisar la validación de contraseña en el backend.
    """
    login_page.navigate()
    login_page.login(CUSTOMER_EMAIL, "contrasena_incorrecta_999")
    expect(login_page.alert_error).to_be_visible()
    _screenshot(login_page, "TC004_contrasena_incorrecta")


# ===========================================================================
# TC-005 — Login fallido: email y contraseña incorrectos
# ===========================================================================
@allure.epic("Autenticación")
@allure.feature("Módulo Login")
@allure.story("Login fallido - credenciales inválidas")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC-005 | Login con email y contraseña incorrectos")
@allure.description(
    "Dado un email y contraseña que no corresponden a ningún usuario registrado, "
    "cuando se intenta iniciar sesión, debe aparecer un mensaje de error."
)
def test_tc005_login_wrong_both(login_page: LoginPage):
    """
    escenario: El usuario ingresa email y contraseña que no corresponden a ningún usuario.
    esperado: El sistema muestra un mensaje de error y el usuario permanece en login.
    impacto: Si falla, cualquier combinación de datos podría acceder al sistema.
    accion: Revisar la lógica de autenticación completa en el backend.
    """
    login_page.navigate()
    login_page.login("nadie@prueba.com", "clave_invalida_000")
    expect(login_page.alert_error).to_be_visible()
    _screenshot(login_page, "TC005_credenciales_invalidas")


# ===========================================================================
# TC-006 — Login fallido: email en formato inválido
# ===========================================================================
@allure.epic("Autenticación")
@allure.feature("Módulo Login")
@allure.story("Login fallido - validación de formato")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC-006 | Login con email en formato inválido")
@allure.description(
    "Dado un valor de email sin el símbolo '@', "
    "cuando se hace clic en login, la validación HTML5 o Angular debe bloquear "
    "el envío y el usuario debe permanecer en /auth/login."
)
def test_tc006_invalid_email_format(login_page: LoginPage):
    """
    escenario: El usuario ingresa un email sin el símbolo @ y hace clic en Login.
    esperado: El sistema bloquea el envío o muestra error de formato.
    impacto: Si falla, datos malformados podrían llegar al servidor sin validación.
    accion: Revisar la validación de formato de email en el frontend.
    """
    login_page.navigate()
    login_page.fill_email("emailsinformato")
    login_page.fill_password(VALID_PASSWORD)
    login_page.click_login()
    # Angular puede interceptar el submit antes que la validación HTML5 del navegador;
    # en ese caso muestra su propio error en lugar de bloquear el envío.
    # Verificamos que AL MENOS UNO de los dos sea verdad: URL en /auth/login o error visible.
    try:
        expect(login_page.page).to_have_url(re.compile(r".*/auth/login.*"), timeout=2000)
    except AssertionError:
        expect(login_page.alert_error).to_be_visible()
    _screenshot(login_page, "TC006_formato_email_invalido")


# ===========================================================================
# TC-007 — Login fallido: ambos campos vacíos
# ===========================================================================
@allure.epic("Autenticación")
@allure.feature("Módulo Login")
@allure.story("Login fallido - validación de campos obligatorios")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC-007 | Login con campos vacíos (ambos)")
@allure.description(
    "Cuando se hace clic en el botón de login sin rellenar ningún campo, "
    "el sistema no debe autenticar al usuario y debe permanecer en /auth/login."
)
def test_tc007_empty_fields(login_page: LoginPage):
    """
    escenario: El usuario hace clic en Login sin rellenar ningún campo.
    esperado: El sistema no autentica al usuario y permanece en la página de login.
    impacto: Si falla, el formulario podría enviarse vacío al servidor.
    accion: Revisar la validación de campos obligatorios en el frontend.
    """
    login_page.navigate()
    # No se rellena nada; se hace clic directamente en submit
    login_page.click_login()
    expect(login_page.page).to_have_url(re.compile(r".*/auth/login.*"))
    _screenshot(login_page, "TC007_campos_vacios")


# ===========================================================================
# TC-008 — Login fallido: solo email, contraseña vacía
# ===========================================================================
@allure.epic("Autenticación")
@allure.feature("Módulo Login")
@allure.story("Login fallido - validación de campos obligatorios")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC-008 | Login solo con email (contraseña vacía)")
@allure.description(
    "Cuando se ingresa solo el email sin contraseña y se hace clic en login, "
    "el sistema no debe autenticar al usuario."
)
def test_tc008_only_email(login_page: LoginPage):
    """
    escenario: El usuario ingresa solo el email sin contraseña y hace clic en Login.
    esperado: El sistema no autentica al usuario y permanece en la página de login.
    impacto: Si falla, un campo vacío podría ser aceptado como credencial válida.
    accion: Revisar la validación del campo contraseña en el frontend.
    """
    login_page.navigate()
    login_page.fill_email(CUSTOMER_EMAIL)
    # Se omite fill_password intencionalmente
    login_page.click_login()
    expect(login_page.page).to_have_url(re.compile(r".*/auth/login.*"))
    _screenshot(login_page, "TC008_solo_email")


# ===========================================================================
# TC-009 — Login fallido: solo contraseña, email vacío
# ===========================================================================
@allure.epic("Autenticación")
@allure.feature("Módulo Login")
@allure.story("Login fallido - validación de campos obligatorios")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC-009 | Login solo con contraseña (email vacío)")
@allure.description(
    "Cuando se ingresa solo la contraseña sin email y se hace clic en login, "
    "el sistema no debe autenticar al usuario."
)
def test_tc009_only_password(login_page: LoginPage):
    """
    escenario: El usuario ingresa solo la contraseña sin email y hace clic en Login.
    esperado: El sistema no autentica al usuario y permanece en la página de login.
    impacto: Si falla, un campo vacío podría ser aceptado como credencial válida.
    accion: Revisar la validación del campo email en el frontend.
    """
    login_page.navigate()
    # Se omite fill_email intencionalmente
    login_page.fill_password(VALID_PASSWORD)
    login_page.click_login()
    expect(login_page.page).to_have_url(re.compile(r".*/auth/login.*"))
    _screenshot(login_page, "TC009_solo_contrasena")


# ===========================================================================
# TC-010 — Login fallido: espacios en blanco en ambos campos
# ===========================================================================
@allure.epic("Autenticación")
@allure.feature("Módulo Login")
@allure.story("Login fallido - validación de campos obligatorios")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC-010 | Login con espacios en blanco en los campos")
@allure.description(
    "Cuando se ingresan solo espacios en blanco en email y contraseña, "
    "el sistema no debe autenticar al usuario; debe mostrar error o bloquear el envío."
)
def test_tc010_whitespace_fields(login_page: LoginPage):
    """
    escenario: El usuario ingresa solo espacios en blanco en ambos campos y hace clic en Login.
    esperado: El sistema no autentica al usuario y permanece en la página de login.
    impacto: Si falla, espacios en blanco podrían ser aceptados como credenciales válidas.
    accion: Revisar que el frontend aplique trim() antes de validar los campos.
    """
    login_page.navigate()
    login_page.fill_email("   ")
    login_page.fill_password("   ")
    login_page.click_login()
    # Espacios en blanco no son credenciales válidas; no debe producirse redirección
    expect(login_page.page).to_have_url(re.compile(r".*/auth/login.*"))
    _screenshot(login_page, "TC010_espacios_en_blanco")


# ===========================================================================
# TC-011 — Contraseña enmascarada (type="password")
# ===========================================================================
@allure.epic("Autenticación")
@allure.feature("Módulo Login")
@allure.story("Seguridad - enmascaramiento de contraseña")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC-011 | Verificar que la contraseña está enmascarada")
@allure.description(
    "El campo de contraseña debe tener el atributo type='password' para que "
    "el texto ingresado no sea legible en pantalla durante la escritura."
)
def test_tc011_password_masked(login_page: LoginPage):
    """
    escenario: El usuario observa el campo de contraseña en la página de login.
    esperado: El campo tiene type=password y el texto ingresado aparece enmascarado.
    impacto: Si falla, las contraseñas quedan expuestas en pantalla.
    accion: Verificar el atributo type del campo password en el HTML.
    """
    login_page.navigate()
    # type="password" es el mecanismo estándar del navegador para ocultar el texto
    expect(login_page.password_input).to_have_attribute("type", "password")
    _screenshot(login_page, "TC011_contrasena_enmascarada")


# ===========================================================================
# TC-012 — Enlace "Forgot password" visible y clickeable
# ===========================================================================
@allure.epic("Autenticación")
@allure.feature("Módulo Login")
@allure.story("UI - recuperación de contraseña")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC-012 | Verificar que el enlace 'Forgot password' existe y es clickeable")
@allure.description(
    "La página de login debe mostrar el enlace de recuperación de contraseña. "
    "Al hacer clic, el usuario debe navegar fuera de /auth/login."
)
def test_tc012_forgot_password_link(login_page: LoginPage):
    """
    escenario: El usuario hace clic en el enlace Forgot Password de la página de login.
    esperado: El enlace es visible y al hacer clic navega fuera de la página de login.
    impacto: Si falla, los usuarios no pueden recuperar su contraseña.
    accion: Verificar que el enlace existe y que la ruta de recuperación está activa.
    """
    login_page.navigate()
    expect(login_page.forgot_password_link).to_be_visible()
    login_page.forgot_password_link.click()
    login_page.page.wait_for_load_state("networkidle")
    # Verificar que la navegación tuvo lugar (ya no estamos en /auth/login)
    expect(login_page.page).not_to_have_url(re.compile(r".*/auth/login.*"))
    _screenshot(login_page, "TC012_forgot_password")


# ===========================================================================
# TC-013 — Navegación al formulario de registro
# ===========================================================================
@allure.epic("Autenticación")
@allure.feature("Módulo Login")
@allure.story("Navegación - acceso al registro")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC-013 | Verificar navegación al registro desde la página de login")
@allure.description(
    "La página de login debe contener un enlace hacia el registro de usuarios. "
    "Al hacer clic, el usuario debe navegar a /auth/register."
)
def test_tc013_navigate_to_register(login_page: LoginPage):
    """
    escenario: El usuario hace clic en el enlace de registro desde la página de login.
    esperado: El sistema navega a la página de registro /auth/register.
    impacto: Si falla, los nuevos usuarios no pueden crear una cuenta desde el login.
    accion: Verificar que el enlace de registro existe y apunta a /auth/register.
    """
    login_page.navigate()
    expect(login_page.register_link).to_be_visible()
    login_page.register_link.click()
    login_page.page.wait_for_load_state("networkidle")
    expect(login_page.page).to_have_url(re.compile(r".*/auth/register.*"))
    _screenshot(login_page, "TC013_navegacion_registro")
