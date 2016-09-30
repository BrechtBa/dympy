#!/usr/bin/env/ python
################################################################################
#    Copyright (c) 2016 Brecht Baeten
#    This file is part of dympy.
#    
#    Permission is hereby granted, free of charge, to any person obtaining a
#    copy of this software and associated documentation files (the "Software"), 
#    to deal in the Software without restriction, including without limitation 
#    the rights to use, copy, modify, merge, publish, distribute, sublicense, 
#    and/or sell copies of the Software, and to permit persons to whom the 
#    Software is furnished to do so, subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be included in 
#    all copies or substantial portions of the Software.
################################################################################
import unittest

import dympy

class TestDympy(unittest.TestCase):

    def test_version(self):
        self.assertGreater( len(dympy.__version__), 0 )

if __name__ == '__main__':
    unittest.main()
