"""Draw the codeuz images from their specifications.

    python brand/render.py                 every image
    python brand/render.py youtube         one folder (logo, github, youtube)
    python brand/render.py --guides        also draw each safe area, into a <name>.guides.png copy

Every image is described by a JSON file next to it: its size in pixels, its background, and its layers
(logo, text, rect, image), each with a position, and for text the font, size, weight and colour. The image is
drawn from that file alone, plus the logo and fonts in brand/brand.json. To change an image, edit its JSON and
run this again. It needs Google Chrome (set CHROME to its path if it is somewhere else), an internet
connection for the fonts, and Pillow for the two images marked "trim".
"""

import html
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRAND = json.loads((ROOT / 'brand.json').read_text(encoding='utf-8'))
CHROME_PATHS = ('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', 'google-chrome', 'google-chrome-stable',
                'chromium', 'chromium-browser')
SHIFT = {'left': '0', 'center': '-50%', 'right': '-100%', 'top': '0', 'middle': '-50%', 'bottom': '-100%'}


def find_chrome() -> str:
    for candidate in (os.environ.get('CHROME'), *CHROME_PATHS):
        if candidate and (Path(candidate).is_file() or shutil.which(candidate)):
            return candidate
    sys.exit('Google Chrome not found. Set CHROME to its path.')


def place(layer: dict) -> str:
    """Put the layer's anchor point (align, valign) at its x and y, counted in pixels from the top left."""
    wrap = f'width:{layer["max_width"]}px;' if 'max_width' in layer else 'white-space:pre;'
    return (f'position:absolute;left:{layer["x"]}px;top:{layer["y"]}px;{wrap}'
            f'transform:translate({SHIFT[layer.get("align", "left")]},{SHIFT[layer.get("valign", "top")]});')


def draw_logo(layer: dict) -> str:
    logo, pad, cursor = BRAND['logo'], BRAND['logo']['padding_em'], BRAND['logo']['cursor_em']
    colors = logo['colors'][f'on_{layer.get("on", "dark")}']
    box = (f'display:inline-flex;align-items:baseline;box-sizing:content-box;font-family:\'{logo["font"]}\',monospace;'
           f'font-weight:{logo["weight"]};font-size:{layer["font_size"]}px;letter-spacing:{logo["letter_spacing_em"]}em;'
           f'line-height:{logo["line_height"]};color:{colors["code"]};border:{logo["border_em"]}em solid {colors["outline"]};'
           f'border-radius:{logo["radius_em"]}em;'
           f'padding:{pad["top"]}em {pad["right"]}em {pad["bottom"]}em {pad["left"]}em;')
    bar = (f'display:inline-block;width:{cursor["width"]}em;height:{cursor["height"]}em;margin-left:{cursor["gap"]}em;'
           f'background:{colors["cursor"]};')
    return (f'<div style="{place(layer)}{box}">{logo["text"][0]}<span style="color:{colors["uz"]}">{logo["text"][1]}</span>'
            f'<span style="{bar}"></span></div>')


def draw_text(layer: dict) -> str:
    style = (f'font-family:\'{layer["font"]}\',sans-serif;font-size:{layer["size"]}px;font-weight:{layer["weight"]};'
             f'color:{layer["color"]};letter-spacing:{layer.get("letter_spacing_em", 0)}em;'
             f'line-height:{layer.get("line_height", 1.15)};text-align:{layer.get("align", "left")};'
             'font-variant-ligatures:none;')
    return f'<div style="{place(layer)}{style}">{html.escape(layer["text"])}</div>'


def draw_rect(layer: dict) -> str:
    border = f'border:{layer["border"]["width"]}px solid {layer["border"]["color"]};' if 'border' in layer else ''
    return (f'<div style="position:absolute;left:{layer["x"]}px;top:{layer["y"]}px;width:{layer["width"]}px;'
            f'height:{layer["height"]}px;box-sizing:border-box;background:{layer.get("fill", "transparent")};{border}'
            f'border-radius:{layer.get("radius", 0)}px"></div>')


def draw_image(layer: dict, folder: Path) -> str:
    return (f'<img src="{(folder / layer["src"]).as_uri()}" style="position:absolute;left:{layer["x"]}px;'
            f'top:{layer["y"]}px;width:{layer["width"]}px;height:{layer["height"]}px">')


DRAW = {'logo': lambda layer, folder: draw_logo(layer), 'text': lambda layer, folder: draw_text(layer),
        'rect': lambda layer, folder: draw_rect(layer), 'image': draw_image}


def draw_guide(area: dict) -> str:
    radius = '50%' if area.get('shape') == 'circle' else '0'
    return (f'<div style="position:absolute;left:{area["x"]}px;top:{area["y"]}px;width:{area["width"]}px;'
            f'height:{area["height"]}px;box-sizing:border-box;border:3px dashed #ff4d6d;border-radius:{radius}"></div>')


def page(spec: dict, folder: Path, guides: bool) -> str:
    layers = ''.join(DRAW[layer['type']](layer, folder) for layer in spec['layers'])
    if guides and 'safe_area' in spec:
        layers += draw_guide(spec['safe_area'])
    return (f'<!doctype html><html><head><meta charset="utf-8"><link href="{BRAND["fonts"]["source"]}" rel="stylesheet">'
            f'<style>html,body{{margin:0;background:transparent}}.canvas{{position:relative;overflow:hidden;'
            f'width:{spec["width"]}px;height:{spec["height"]}px;background:{spec["background"]};'
            f'border-radius:{spec.get("radius", 0)}px}}</style></head>'
            f'<body><div class="canvas">{layers}</div></body></html>')


def main() -> None:
    args = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
    guides = '--guides' in sys.argv
    chrome = find_chrome()
    with tempfile.TemporaryDirectory() as name:
        tmp = Path(name)
        for file in sorted(ROOT.glob('*/**/*.json')):
            if args and file.relative_to(ROOT).parts[0] not in args:
                continue
            spec = json.loads(file.read_text(encoding='utf-8'))
            out = file.parent / spec['output']
            if guides:
                out = out.with_name(out.stem + '.guides.png')
            source = tmp / '-'.join(file.relative_to(ROOT).with_suffix('.html').parts)
            source.write_text(page(spec, file.parent, guides), encoding='utf-8')
            subprocess.run([chrome, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                            f'--window-size={spec["width"]},{spec["height"]}',
                            f'--force-device-scale-factor={spec.get("scale", 1)}',
                            '--default-background-color=00000000', '--allow-file-access-from-files',
                            '--virtual-time-budget=6000', f'--user-data-dir={tmp / "profile"}', f'--screenshot={out}',
                            source.as_uri()], check=True, capture_output=True)
            if spec.get('trim'):
                from PIL import Image
                image = Image.open(out)
                image.crop(image.getbbox()).save(out)
            print('wrote', out.relative_to(ROOT.parent))


if __name__ == '__main__':
    main()
