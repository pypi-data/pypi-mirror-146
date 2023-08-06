#!/usr/bin/env python

"""Import the pyx version of rolling_checksum_mod, else import the pure python version."""

try:
    from rolling_checksum_pyx_mod import min_max_chunker
except ImportError:
    from rolling_checksum_py_mod import min_max_chunker

_ = min_max_chunker
