# -*- coding: utf-8 -*-
# Copyright 2012-2014 Hayaki Saito <user@zuse.jp>
# Copyright 2023 Lubosz Sarnecki <lubosz@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import sys
import platform

if platform.system() == "Windows":
    import ctypes
else:
    import termios
    import select


def get_terminal_size_windows():
    """Gets the terminal size on Windows using ctypes."""
    try:
        from ctypes import windll, create_string_buffer

        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        if res:
            (
                bufx,
                bufy,
                curx,
                cury,
                wattr,
                left,
                top,
                right,
                bottom,
                maxx,
                maxy,
            ) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            width = right - left + 1
            height = bottom - top + 1
            return width, height
        else:
            return 80, 25  # Default values if unable to get size
    except Exception:
        return 80, 25


def __set_raw():
    """Sets the terminal to raw mode."""
    fd = sys.stdin.fileno()
    backup = termios.tcgetattr(fd)
    try:
        new = termios.tcgetattr(fd)
        new[0] = 0  # c_iflag = 0
        new[3] = 0  # c_lflag = 0
        new[3] = new[3] & ~(termios.ECHO | termios.ICANON)
        termios.tcsetattr(fd, termios.TCSANOW, new)
    except Exception:
        termios.tcsetattr(fd, termios.TCSANOW, backup)
    return backup


def __reset_raw(old):
    """Resets the terminal to its original mode."""
    fd = sys.stdin.fileno()
    termios.tcsetattr(fd, termios.TCSAFLUSH, old)


def __get_report(query):
    """Sends a query to the terminal and returns the response."""
    result = ""
    fd = sys.stdin.fileno()
    rfds = [fd]
    wfds = []
    xfds = []

    sys.stdout.write(query)
    sys.stdout.flush()

    rfd, wfd, xfd = select.select(rfds, wfds, xfds, 0.5)
    if rfd:
        result = os.read(fd, 1024)
        return result[:-1].split(";")
    return None


def get_size():
    """Gets the character width and height of the terminal."""
    if platform.system() == "Windows":
        # Use Windows-specific method to get terminal size

        return 1, 1  # Doesn't make sense on windows
    else:
        # Use ANSI escape codes to query terminal size

        backup_termios = __set_raw()
        try:
            height_width = __get_report("\x1b[14t")
            row_column = __get_report("\x1b[18t")

            if height_width is None or row_column is None:
                return 1, 1

            height, width = height_width[1:]
            row, column = row_column[1:]

            char_width = int(width) / int(column)
            char_height = int(height) / int(row)
        finally:
            __reset_raw(backup_termios)
        return char_width, char_height
