"""Generate the docs."""

from pathlib import Path
import pdoc
import pdoc.render


here = Path(__file__).parent

pdoc.render.configure(
    docformat="google",
    footer_text="usaddress",
    favicon="https://whubsch.github.io/usaddress/fav.svg",
    logo="https://whubsch.github.io/usaddress/logo.png",
)
pdoc.pdoc("src/usaddress", output_directory=here.parent / "docs")
