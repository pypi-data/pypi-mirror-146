# MTG Binder Spine Generator

Generates an image that can be printed and inserted into the spine of a binder.

## Installation

`pip install mtgbinderspine`

## Usage

Run `mtgbinderspine --help` for usage information.

## Examples

Generate an image with spines for Throne of Eldraine and Kaladesh:

`mtgbinderspine eld kld`

Generate a spine for a 2" binder:

`mtgbinderspine -w 2 m13`

Generate a spine with multiple icons and a custom image:

`poetry run mtgbinderspine ddn ddk ddg ddd dde ddc dd1 ddl --custom-text "Duel Decks"`

## Images

![bfz_ktk_chk](docs/images/bfz_ktk_chk.png)

![duel_decks](docs/images/duel_decks.png)
