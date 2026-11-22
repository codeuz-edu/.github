# .github

Public profile and shared defaults for the **codeuz** GitHub organization.

- [`profile/README.md`](./profile/README.md): the organization page, in Uzbek
- [`brand/`](./brand/): every codeuz image, and the information needed to draw it again

## Brand images

Each image in [`brand/`](./brand/) has a JSON file next to it with the same name. The JSON holds the size in pixels, the background, and every layer: its position, and for text the font, size, weight and colour. [`brand/brand.json`](./brand/brand.json) holds the colours, the fonts and the proportions of the logo.

| Folder | Images |
|---|---|
| [`brand/logo/`](./brand/logo/) | the logo for light and dark backgrounds, and the square icon |
| [`brand/github/`](./brand/github/) | the organization picture and profile banner, the README banner of each course (`readme/`), the link preview of each course (`preview/`) |
| [`brand/youtube/`](./brand/youtube/) | the channel banner and picture |

To change an image, edit its JSON and run `python brand/render.py`. To add one, copy a JSON file, change it, and run the same command. It needs Google Chrome, an internet connection for the fonts, and Pillow.

## Shared defaults

- [`CONTRIBUTING.md`](./CONTRIBUTING.md): contributing guide for every repository without its own
- [`.github/ISSUE_TEMPLATE/`](./.github/ISSUE_TEMPLATE/): issue forms for every repository without its own
