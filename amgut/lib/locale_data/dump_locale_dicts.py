#!/usr/bin/env python
from __future__ import division

# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The American Gut Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
import importlib
from sys import argv
from os import mkdir
from os.path import join

from future.utils import viewitems


def _write_file_dict(basefolder, name, outdict):
    with open(join(basefolder, "%s.txt" % name), 'w') as f:
        f.write("VARIABLE\tTEXT\n")
        for variable, name in viewitems(outdict):
            f.write("%s\t%s\n" % (variable, name))


def write_locale(module):
    # import the module given
    current_locale_module = '.'.join(['amgut.lib.locale_data', module])
    try:
        current_locale = importlib.import_module(current_locale_module)
    except ImportError:
        raise ImportError("Cannot import locale! %s" % current_locale_module)

    # make a folder to hold all the files
    mkdir(module)

    # export media_locale dict to file
    _write_file_dict(module, "media_locale", current_locale.media_locale)

    # export all page dicts to file
    for page, pagedict in viewitems(current_locale.text_locale):
        _write_file_dict(module, page, pagedict)

if __name__ == "__main__":
    write_locale(argv[1])
