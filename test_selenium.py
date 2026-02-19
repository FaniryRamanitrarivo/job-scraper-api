from app.browsers.selenium_browser import SeleniumBrowser


def test_selenium():
    # Crée une instance de ton navigateur depuis le pool
    browser = SeleniumBrowser()

    try:
        # Ouvre une page de test
        browser.open("https://example.com")

        # Récupère le titre de la page
        title = browser.driver.title
        print(f"Page title: {title}")

        # Cherche tous les éléments <p> de la page
        paragraphs = browser.find_elements("p")
        print(f"Found {len(paragraphs)} paragraph(s) on the page.")

        # Affiche le texte du premier paragraphe si présent
        if paragraphs:
            print("First paragraph:", browser.get_text(paragraphs[0]))

    finally:
        # Libère le navigateur dans le pool
        browser.quit()

if __name__ == "__main__":
    test_selenium()