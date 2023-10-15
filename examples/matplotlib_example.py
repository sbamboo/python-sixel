#!/usr/bin/env python
from io import BytesIO
import matplotlib
import matplotlib.pyplot as plt
import numpy
import sixel


def sixel_fig():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')

    writer = sixel.SixelWriter()
    writer.draw(buffer)


def main():
    matplotlib.rcParams["backend"] = "Agg"
    plt.figure(figsize=(4, 3))
    x = numpy.linspace(0, 1, 100)
    y = x**2
    plt.plot(x,y)
    sixel_fig()


if __name__ == "__main__":
    main()

