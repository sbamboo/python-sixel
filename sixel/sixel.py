#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2012-2014 Hayaki Saito <user@zuse.jp>
# Copyright 2023 Lubosz Sarnecki <lubosz@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import os
from .converter import SixelConverter


class SixelWriter:

    def __init__(self, f8bit=False, body_only=False):
        self.f8bit = f8bit
        self._body_only = body_only
        if f8bit:  # 8bit mode
            self.CSI = '\x9b'
        else:
            self.CSI = '\x1b['

    def save_position(self, output):
        if not self._body_only:
            if os.isatty(output.fileno()):
                output.write('\x1b7')  # DECSC

    def restore_position(self, output):
        if not self._body_only:
            if os.isatty(output.fileno()):
                output.write('\x1b8')  # DECRC

    def move_x(self, n, fabsolute, output):
        if not self._body_only:
            output.write(self.CSI)
            if fabsolute:
                output.write('%d`' % n)
            elif n > 0:
                output.write('%dC' % n)
            elif n < 0:
                output.write('%dD' % -n)

    def move_y(self, n, fabsolute, output):
        if not self._body_only:
            output.write(self.CSI)
            if fabsolute:
                output.write('%dd' % n)
            elif n > 0:
                output.write('%dB' % n)
            elif n < 0:
                output.write('%dA' % n)

    def draw(self,
             filename,
             output=sys.stdout,
             absolute=False,
             x=None,
             y=None,
             w=None,
             h=None,
             ncolor=256,
             alpha_threshold=0,
             chromakey=False,
             fast=True):

        try:
            filename.seek(0)
        except Exception:
            pass
        self.save_position(output)

        try:
            if x is not None:
                self.move_x(x, absolute, output)

            if y is not None:
                self.move_y(y, absolute, output)

            sixel_converter = SixelConverter(filename,
                                             self.f8bit,
                                             w,
                                             h,
                                             ncolor,
                                             alpha_threshold=alpha_threshold,
                                             chromakey=chromakey,
                                             fast=fast)
            sixel_converter.write(output, body_only=self._body_only)

        finally:
            self.restore_position(output)
