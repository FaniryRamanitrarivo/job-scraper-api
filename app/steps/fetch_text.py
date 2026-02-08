def fetch_text(step, ctx):
    """
    Récupère le texte d'un élément et l'ajoute dans ctx.data.
    Si la clé existe déjà, on append dans la liste pour ne pas écraser.
    """
    selector = step["selector"]
    save_as = step["save_as"]

    ctx.log(f"Fetching text for selector {selector}")

    # Récupérer le texte via le navigateur
    value = ctx.browser.get_text(selector)

    # Stocker dans une liste pour accumuler tous les items
    if save_as in ctx.data:
        ctx.data[save_as].append(value)
    else:
        ctx.data[save_as] = [value]

    ctx.log(f"Saved text under '{save_as}': {value}")
