import typer

from . import ContourHeightmap

app = typer.Typer()


@app.command()
def main(input_filename: str, output_filename: str = typer.Option(None)):
    c = ContourHeightmap()
    if not output_filename:
        output_filename = "output.png"
    c.contour(input_filename, output_filename)


if __name__ == "__main__":
    app()
