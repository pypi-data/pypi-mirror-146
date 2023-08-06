from functools import partial
from io import BytesIO
from math import ceil, sqrt
from typing import Callable
from json import dumps as json_dumps

from PIL import Image
from rectpack import newPacker

from svgwrite import Drawing

from cairosvg import svg2png


def draw_kp(drawing: Drawing):
    drawing.add(drawing.circle((100, 100), 80, fill="black"))


def draw_signal_circle(drawing: Drawing):
    drawing.add(drawing.circle((100, 100), 95, fill="white", stroke="black", stroke_width=5))


def draw_signal_square(drawing: Drawing):
    drawing.add(drawing.rect((5, 5), (190, 190), fill="white", stroke="black", stroke_width=5))


def draw_signal_speed_square(drawing: Drawing):
    drawing.add(drawing.rect(
        (5, 5 + 100 - (190 / 1.316 / 2)),
        (190, 190 / 1.316),
        fill="white",
        stroke="black",
        stroke_width=5,
    ))


def draw_signal_stop(drawing: Drawing):
    drawing.add(drawing.rect((0, 0), (200, 200 / 2.593), fill="black", rx=10, ry=10))


def draw_signal_letters(letters: str, drawing: Drawing):
    drawing.embed_font(name="Avenir", filename="symbolist/fonts/avenir_black.woff")
    drawing.embed_stylesheet(".signal_letters { font-family: \"Avenir\"; font-size: 100; }")
    drawing.add(drawing.text(
        letters,
        ("50%", "50%"),
        dominant_baseline="middle",
        text_anchor="middle",
        class_="signal_letters",
    ))


def draw_signal_speed_letters(letters: str, drawing: Drawing):
    drawing.embed_font(name="Avenir", filename="symbolist/fonts/avenir_black.woff")
    drawing.embed_stylesheet(".signal_speed_letters { font-family: \"Avenir\"; font-size: 50; }")
    drawing.add(drawing.text(
        letters,
        ("50%", "40%"),
        dominant_baseline="middle",
        text_anchor="middle",
        class_="signal_speed_letters",
    ))


def draw_signal_speed_arrow(drawing: Drawing):
    drawing.add(drawing.line(start=(45, 135), end=(200 - 45, 135), stroke="black", stroke_width=5))


def draw_signal_speed_arrow_left(drawing: Drawing):
    drawing.add(drawing.polygon(points=[(40, 135), (65, 120), (65, 150)], fill="black"))


def draw_signal_speed_arrow_right(drawing: Drawing):
    drawing.add(drawing.polygon(points=[(200 - 40, 135), (200 - 65, 120), (200 - 65, 150)], fill="black"))


def draw_png(drawers: list[Callable[[Drawing], None]]) -> bytes:
    drawing = Drawing(size=("5cm", "5cm"))
    drawing.viewbox(width=200, height=200)
    for drawer in drawers:
        drawer(drawing)
    return svg2png(bytestring=drawing.tostring(), dpi=200 / 2.54 / 1.55), drawing.tostring()


symbols = [
    ("rk", [draw_kp]),
    ("signal_guidon_arrêt", [draw_signal_stop]),
    ("signal_lumineux_carré", [draw_signal_square, partial(draw_signal_letters, "C")]),
    ("signal_lumineux_carré_violet", [draw_signal_square, partial(draw_signal_letters, "Cv")]),
    ("signal_lumineux_sémaphore", [draw_signal_square, partial(draw_signal_letters, "S")]),
    ("signal_lumineux_avertissement", [draw_signal_circle, partial(draw_signal_letters, "A")]),
    ("signal_lumineux_disque", [draw_signal_circle, partial(draw_signal_letters, "D")]),
]

for speed in [10, 12, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125,
              130, 135, 140, 145, 150, 155, 160, 170, 180, 190, 200, 210, 220, 230, 270, 300, 320, 350]:
    drawers = [draw_signal_speed_square, partial(draw_signal_speed_letters, str(speed)), draw_signal_speed_arrow]
    symbols.append((
        f"vitesse_max_ligne_{speed}",
        drawers + [draw_signal_speed_arrow_left, draw_signal_speed_arrow_right]
    ))
    symbols.append((f"vitesse_max_ligne_{speed}_gauche", drawers + [draw_signal_speed_arrow_left]))
    symbols.append((f"vitesse_max_ligne_{speed}_droite", drawers + [draw_signal_speed_arrow_right]))


if __name__ == "__main__":
    print("generating symbols")
    symbol_by_name = {}
    for symbol_name, drawers in symbols:
        print(f"    - generating {symbol_name}")
        png_bin, svg_str = draw_png(drawers)
        image = Image.open(BytesIO(png_bin))
        image = image.crop(image.getbbox())
        symbol_by_name[symbol_name] = image
        with open(f"/tmp/{symbol_name}.svg", "w") as svg_file:
            svg_file.write(svg_str)

    has_solution = False
    side_size = int(ceil(sqrt(len(symbols)))) // 2
    while not has_solution:
        print(f"trying to pack in {side_size}x{side_size} grid")
        packer = newPacker()
        packer.add_bin(side_size * 100, side_size * 100)
        for symbol_name, image in symbol_by_name.items():
            packer.add_rect(image.size[0], image.size[0], symbol_name)
        packer.pack()
        if len(packer[0]) == len(symbols):
            has_solution = True
        else:
            side_size += 1

    print("saving final sprite sheet")
    output_image = Image.new("RGBA", (side_size * 100, side_size * 100))
    output_json = {}
    for _, x, y, width, height, symbol_name in packer.rect_list():
        output_image.paste(symbol_by_name[symbol_name], (x, y))
        output_json[symbol_name] = {"x": x, "y": y, "width": width, "height": height}
    output_image.save("/tmp/output_image.png")
    with open("/tmp/output_json.json", "w") as output_json_file:
        output_json_file.write(json_dumps(output_json))
