# python-sixel

Display images in the terminal using [Sixel](https://en.wikipedia.org/wiki/Sixel).

This is a fork targeting windows, the version that was forked is itself a fork of the no longer maintained [PySixel](https://github.com/saitoha/PySixel).

Check [arewesixelyet.com](https://www.arewesixelyet.com/) for supported terminals.

## Installation

### PyPI release
```
pip install sixel
```

### git main branch
```
pip install git+https://github.com/lubosz/python-sixel.git
```

### Local copy
```
git clone https://github.com/lubosz/python-sixel.git
cd python-sixel
pip install -e .
```

## Example

```python
import sys
from sixel import converter

c = converter.SixelConverter("foo.png")
c.write(sys.stdout)
```

See examples directory for more examples.

## sixelconv

python-sixel provides a command line tool.

Display an image in the terminal
```
sixelconv [options] filename
```

Or by using a pipe
```
cat filename | sixelconv [options]
```

### Options

```
-h, --help                                            show this help message and exit
-8, --8bit-mode                                       Generate a sixel image for 8bit terminal or printer
-7, --7bit-mode                                       Generate a sixel image for 7bit terminal or printer
-r, --relative-position                               Treat specified position as relative one
-a, --absolute-position                               Treat specified position as absolute one
-x LEFT, --left=LEFT                                  Left position in cell size, or pixel size with unit 'px'
-y TOP, --top=TOP                                     Top position in cell size, or pixel size with unit 'px'
-w WIDTH, --width=WIDTH                               Width in cell size, or pixel size with unit 'px'
-e HEIGHT, --height=HEIGHT                            Height in cell size, or pixel size with unit 'px'
-t ALPHATHRESHOLD, --alpha-threshold=ALPHATHRESHOLD   Alpha threshold for PNG-to-SIXEL image conversion
-c, --chromakey                                       Enable auto chroma key processing
-n NCOLOR, --ncolor=NCOLOR                            Specify number of colors
-b, --body-only                                       Output sixel without header and DCS envelope
-f, --fast                                            The speed priority mode (default)
-s, --size                                            The size priority mode
```

### Examples

View an image file
```
sixelconv test.png
```

Generate sixel file from an image file
```
sixelconv < test.png > test.six
```

View generated sixel file
```
cat test.six
```
