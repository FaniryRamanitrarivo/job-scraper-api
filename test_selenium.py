from app.browsers.selenium import SeleniumBrowser

if __name__ == "__main__":
    browser = SeleniumBrowser(headless=True)  # headless=False si tu veux voir le navigateur
    browser.open("https://www.portaljob-madagascar.com")
    
    # Exemple : récupérer tous les liens dans la page
    elements = browser.find_elements("a")
    print(f"Found {len(elements)} links")
    for el in elements[:5]:  # Affiche les 5 premiers
        print(browser.get_text(el), el.get_attribute("href"))

    browser.close()
