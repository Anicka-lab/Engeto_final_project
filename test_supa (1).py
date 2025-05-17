import pytest

from playwright.sync_api import sync_playwright
from playwright.sync_api import expect



BASE_URL = "https://rohlik.cz/"


@pytest.fixture
def browser():
	with sync_playwright() as p:
		browser = p.chromium.launch(
			headless=False, # bez otevrenyho okna
            slow_mo=500, # cekani na akce (v milisekundach)
            timeout=5000 
            )
		yield browser
		browser.close()

@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

def test_rohlik_in_title(page):
    """
    string "rohlik.cz" musi byt v titulku stranky
    """
    page.goto(BASE_URL)
    assert "rohlik.cz" in page.title().casefold()

def test_logo_is_visible(page):
    """
    po nacteni stranky musi byt viditelne logo
    """
    page.goto(BASE_URL)
    page.wait_for_load_state("load")
    assert page.get_by_role("link", name="Online supermarket Rohlik.cz").is_visible()

def test_otevri_a_zavri_kosik(page):
    """
    po kliknuti na kosik se zobrazi prazdny kosik
    a po kliknuti na krizek se zavre
    """
    page.goto(BASE_URL)
    page.wait_for_load_state("load")
    page.locator("[data-test=\"cart-header-wrapper\"]").click()
    expect(page.locator("[data-test=\"empty-cart-wrapper\"]")).to_be_visible()
    page.locator("[data-test=\"cart-close-button\"]").click()
    expect(page.locator("[data-test=\"empty-cart-wrapper\"]")).not_to_be_visible()

def test_otevri_menu_kategorie(page):
    """
    po najeti mysi na menu kategorie se zobrazi menu
    """
    page.goto(BASE_URL)
    page.wait_for_load_state("load")
    kategorie = page.locator("[data-test=\"navigation-tab-CATEGORY\"]").get_by_text("Kategorie")
    kategorie.hover()
    expect(page.locator("[data-test=\"categories-list\"]").get_by_role("link", name="Ovoce a zelenina")).to_be_visible()

    



    




    