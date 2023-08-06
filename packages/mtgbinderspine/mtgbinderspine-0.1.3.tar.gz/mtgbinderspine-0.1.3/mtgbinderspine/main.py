import io
import logging
import pathlib
from typing import List

import click
from cairosvg import svg2png
from PIL import Image, ImageDraw, ImageFont
from rich.logging import RichHandler
from rich.progress import Progress
from svglib.svglib import svg2rlg

from mtgbinderspine import client, render, util

logging.basicConfig(
    level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")


@click.command()
@click.argument("set_code", type=str, nargs=-1)
@click.option("--dpi", type=int, default=600, help="The dpi of the output image")
@click.option(
    "-o",
    "--output",
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
    help="The output file (if not provided, will make a directory called renders in current directory)",
)
@click.option(
    "-l",
    "--length",
    type=float,
    default=10.5,
    help="The length of each spine, in inches (the width of the output image)",
)
@click.option(
    "-w",
    "--width",
    type=float,
    default=1,
    help="The width of each spine, in inches (the height of the output image)",
)
@click.option(
    "--border-thickness",
    "_border_thickness",
    type=int,
    default=3,
    help="The thickness of the border between each spine, in pixels",
)
@click.option(
    "--border-color",
    "_border_color",
    type=int,
    default=160,
    help="The color of the border between each spine, in grayscale (int 0-255)",
)
@click.option(
    "--font-size",
    "_font_size",
    type=int,
    default=350,
    help="The size of the font used to render the set name, in points",
)
@click.option(
    "--custom-text",
    "_custom_text",
    type=str,
    default=None,
    help="If provided, will use this text instead of the set name, and will combine all set icons into a single spine",
)
def render_spine_command(
    set_code: List[str],
    output: str,
    dpi: int,
    length: float,
    width: float,
    _border_thickness: int,
    _border_color: int,
    _font_size: int,
    _custom_text: str,
):
    log.info("Starting render")

    ims = []

    if _custom_text is not None:
        with Progress() as progress:
            set_images = [client.get_set_image(c) for c in progress.track(set_code)]

            params = render.RenderParams(
                icons=set_images,
                text=_custom_text,
                icon_layout=render.IconLayout.CIRCLE,
                length_in=length,
                width_in=width,
                dpi=dpi,
                font_size=_font_size,
            )

            ims.append(render.render_spine(params))
    else:
        # Regular path
        with Progress() as progress:
            for code in progress.track(set_code):

                set_image = client.get_set_image(code)

                if not set_image:
                    log.error(f"Set {code} not found")
                    return 1

                set_name = client.get_set_name(code)

                params = render.RenderParams(
                    icons=[set_image],
                    text=set_name,
                    icon_layout=render.IconLayout.CENTER,
                    length_in=length,
                    width_in=width,
                    dpi=dpi,
                    font_size=_font_size,
                )

                im = render.render_spine(params)

                ims.append(im)

    log.info("Rendering full image...")
    # Stack images
    im = Image.new(size=(ims[0].width, 1 + (ims[0].height + 1) * len(ims)), mode="RGBA")
    for i, sub_im in enumerate(ims):
        im.paste(sub_im, (0, 1 + i * (ims[0].height + 1)))

    # Draw separating lines
    draw = ImageDraw.Draw(im)

    for i in range(0, len(ims) + 1):
        y = i * (ims[0].height + 1)
        # Draw the line
        line_greyness = _border_color
        draw.line(
            (0, y, ims[0].width, y),
            fill=(line_greyness, line_greyness, line_greyness, 255),
            width=_border_thickness,
        )

    if output is None:
        if _custom_text is not None:
            filename = util.txt2filename(_custom_text) + ".png"
        else:
            filename = "_".join(set_code) + ".png"

        parent_folder = pathlib.Path("renders/")
        parent_folder.mkdir(parents=True, exist_ok=True)

        output = str(parent_folder / filename)

    log.info("Saving...")
    im.save(output, dpi=(dpi, dpi))

    log.info("Complete!")


if __name__ == "__main__":
    render_spine_command()
