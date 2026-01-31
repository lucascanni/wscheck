import typer

app = typer.Typer()

@app.command()
def hello():
    print("wscheck prêt")

def main():
    app()

if __name__ == "__main__":
    main()
