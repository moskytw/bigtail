#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.2'

import os

def tac_chunks(file_or_path, buffer_size=None):

    if buffer_size is None:
        # `buffer_size` is not a constant.
        buffer_size = 4096 # 4 kB

    open_by_me = None

    if isinstance(file_or_path, basestring):
        f = open(file_or_path)
        f.seek(0, os.SEEK_END)
        open_by_me = True
    else:
        f = file_or_path
        open_by_me = False

    while True:

        # move to the start of next chunk
        if f.tell()-buffer_size > 0:
            f.seek(-buffer_size, os.SEEK_CUR)
        else:
            buffer_size = f.tell()
            f.seek(0)

        chunk = f.read(buffer_size)
        if not chunk: break

        # restore the pointer after reading the file
        f.seek(-buffer_size, os.SEEK_CUR)

        yield chunk

    if open_by_me:
        f.close()

def tac(file_or_path, buffer_size=None):
    
    fragment = ''

    for chunk in tac_chunks(file_or_path, buffer_size):

        lines = chunk.splitlines(True)

        # check the integrity of the fragment
        if fragment and lines[-1].endswith('\n'):
            # fragment is a complete line, because the last line ends with '\n'
            yield fragment
            fragment = ''

        # the last line of this chunk may be a part of previous fragment
        fragment = lines.pop(-1)+fragment

        if lines:

            # the fragment is a complete line, because there has other '\n'
            yield fragment

            # the first line may be a fragment
            fragment = lines[0]

            for line in reversed(lines[1:]):
                yield line

    if fragment:
        yield fragment