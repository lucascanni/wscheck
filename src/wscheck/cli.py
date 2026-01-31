import typer

app = typer.Typer(help="wscheck - Workstation Health Check CLI")

@app.callback()
def main():
    """
    Outil CLI pour diagnostiquer l'état d'un poste (Windows).
    """
    # callback = commande racine (sans action par défaut)
    pass

@app.command("hello")
def hello():
    """Commande de test"""
    print("wscheck prêt")
