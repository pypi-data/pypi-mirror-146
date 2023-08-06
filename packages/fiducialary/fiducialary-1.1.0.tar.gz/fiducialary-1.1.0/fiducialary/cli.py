import typer

from . import generate_page_of_markers_A4

app = typer.Typer()


@app.command()
def main():
    generate_page_of_markers_A4()


if __name__ == "__main__":
    app()
