import io
import logging
import math
import pathlib
from dataclasses import dataclass
from enum import Enum
from typing import List

from cairosvg import svg2png
from PIL import Image, ImageDraw, ImageFont
from svglib.svglib import svg2rlg

log = logging.getLogger("rich")


class IconLayout(Enum):
    CENTER = "center"
    CIRCLE = "circle"


@dataclass
class RenderParams:
    icons: List[bytes]
    text: str
    icon_layout: IconLayout = IconLayout.CENTER
    length_in: float = 10.5
    width_in: float = 1
    dpi: int = 600
    font_size: int = 350


def render_spine(params: RenderParams) -> Image:
    """
    Renders the card spine as a Pillow Image
    """

    width = int(params.length_in * params.dpi)

    height = int(params.width_in * params.dpi)

    # Create the spine image
    im = Image.new(size=(width, height), mode="RGBA")

    # Draw Set Icon
    set_icon_margin = 0.1

    if params.icon_layout == IconLayout.CENTER:
        if len(params.icons) != 1:
            raise ValueError("Only one icon is supported for the center layout")

        pil_icon = _convert_svg_bytes_to_im(
            svg_bytes=params.icons[0],
            icon_size=params.width_in - set_icon_margin * 2,
            dpi=params.dpi,
        )

        icon_area_width = max(int(params.dpi * 2.5), pil_icon.width)

        # Paste the set icon in on the left side
        im.alpha_composite(
            pil_icon,
            (
                (icon_area_width - pil_icon.width) // 2,
                int(set_icon_margin * params.dpi),
            ),
        )
    elif params.icon_layout == IconLayout.CIRCLE:
        if len(params.icons) > 8:
            raise ValueError("Only 8 icons maximum are supported for the circle layout")

        # TODO: vary this based on the number of icons
        if len(params.icons) <= 4:
            icon_size = (params.width_in - set_icon_margin * 2) / 2
            radius = (params.width_in - set_icon_margin * 2) / 3
        else:
            icon_size = (params.width_in - set_icon_margin * 2) / 3.5
            radius = (params.width_in - set_icon_margin * 2) / 2.5

        for i, icon in enumerate(params.icons):
            pil_icon = _convert_svg_bytes_to_im(
                svg_bytes=icon,
                icon_size=icon_size,
                dpi=params.dpi,
            )

            icon_area_width = max(int(params.dpi * 2.5), pil_icon.width)

            center_px = (
                icon_area_width // 2,
                (params.width_in * params.dpi // 2),
            )

            angle = (i / len(params.icons)) * 2 * math.pi

            dx = math.cos(angle) * radius * params.dpi
            dy = math.sin(angle) * radius * params.dpi

            icon_loc = (
                int(center_px[0] + dx - pil_icon.width // 2),
                int(center_px[1] + dy - pil_icon.height // 2),
            )

            im.alpha_composite(pil_icon, icon_loc)

    # Draw the set name
    draw = ImageDraw.Draw(im)

    default_font_path = (
        pathlib.Path(__file__).parent.parent / "fonts" / "Beleren2016-Bold.ttf"
    )

    font = ImageFont.truetype(str(default_font_path), size=params.font_size)

    text_size = draw.textsize(params.text, font)

    x_offset = icon_area_width

    draw.text(
        (x_offset + (width - x_offset - text_size[0]) / 2, (height - text_size[1]) / 2),
        params.text,
        fill=(0, 0, 0, 255),
        font=font,
    )

    return im


def _convert_svg_bytes_to_im(svg_bytes: bytes, icon_size: int, dpi: int) -> Image:
    """
    Converts a SVG image to a Pillow Image
    """

    svg_bytesio = io.BytesIO(svg_bytes)

    raw_image = io.BytesIO()

    rlg = svg2rlg(svg_bytesio)

    svg2png_scale = (icon_size / rlg.height) * dpi

    svg2png(
        file_obj=svg_bytesio,
        write_to=raw_image,
        background_color="transparent",
        scale=svg2png_scale,
    )

    return Image.open(raw_image).convert("RGBA")
