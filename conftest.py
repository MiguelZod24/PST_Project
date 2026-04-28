import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Fixture función-scoped: cada test recibe una instancia fresca de LoginPage.

    El fixture `page` lo provee pytest-playwright automáticamente con un nuevo
    contexto de navegador (sin cookies ni localStorage previos), garantizando
    que los tests sean completamente independientes entre sí.
    """
    return LoginPage(page)
