# -*- coding: utf-8 -*-
# Copyright 2012-2014 Hayaki Saito <user@zuse.jp>
# Copyright 2023 Lubosz Sarnecki <lubosz@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import os
import termios
import select


def __set_raw():
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
    fd = sys.stdin.fileno()
    termios.tcsetattr(fd, termios.TCSAFLUSH, old)


def __get_report(query):
    result = ''
    fd = sys.stdin.fileno()
    rfds = [fd]
    wfds = []
    xfds = []

    sys.stdout.write(query)
    sys.stdout.flush()

    rfd, wfd, xfd = select.select(rfds, wfds, xfds, 0.5)
    if rfd:
        result = os.read(fd, 1024)
        return result[:-1].split(';')[1:]
    return None


def get_size():

    backup_termios = __set_raw()
    try:
        height, width = __get_report("\x1b[14t")
        row, column = __get_report("\x1b[18t")

        char_width = int(width) / int(column)
        char_height = int(height) / int(row)
    finally:
        __reset_raw(backup_termios)
    return char_width, char_height
