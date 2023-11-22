import typer
import yaml
from uvicorn.importer import import_from_string


def export(app: str = "main:app", out: str = "openapi.yaml"):
    app = import_from_string(app)
    openapi = app.openapi()
    with open(out, "w") as f:
        yaml.dump(openapi, f, allow_unicode=True)


if __name__ == "__main__":
    typer.run(export)
