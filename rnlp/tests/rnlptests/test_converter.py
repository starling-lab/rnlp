# Copyright (C) 2017-2018 StARLinG Lab
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (at the base of this repository). If not,
# see <http://www.gnu.org/licenses/>

import hashlib
import os
import unittest

from rnlp import converter
from rnlp.corpus import declaration


class converterTest(unittest.TestCase):
    """
    This performs a similar test to test_parse.py, but uses rnlp.converter.
    """
    def __init__(self, *args, **kwargs):
        super(converterTest, self).__init__(*args, **kwargs)
        
        self._path = os.getcwd()
        self._fileSet = [
            "wordIDs.txt",
            "sentenceIDs.txt",
            "blockIDs.txt",
            "facts.txt",
            "bk.txt"
        ]

    def tearDown(self):
        """
        Removes files created by ``parse.makeIdentifiers``, since the current
        version appends to the end of the files each time the function runs.
        """
        for f in self._fileSet:
            f = os.path.join(self._path, f)
            if os.path.isfile(f):
                os.remove(f)

    def EqualFileContents(self, fileName, expectedHash):
        """
        Open ``fileName`` and return true if the list ``expectedContents``
        match the contents of the file.
        """

        with open(fileName) as f:
            contents = f.read()

        trueHash = hashlib.md5(contents.encode("utf-8")).hexdigest()

        return trueHash == expectedHash

    def runner(self, example, blockLength, hashlist):
        """
        Creates identifiers with makeIdentifiers, and asserts that
        the md5 hashes match.

        example: str.
        blockLength: int.
        hashlist: list of five hash values.
        """

        converter(example, blockLength)

        for index, fileName in enumerate(self._fileSet):
            fileName = os.path.join(self._path, fileName)
            self.assertTrue(self.EqualFileContents(fileName, hashlist[index]))

    def test_makeIdentifiers_1(self):
        self.runner("Hello there. How are you?", 1,
                    ["bbaccb43cf22eeea851df721a40fddb7",
                     "60ffc99bc55eaab87b74d77557164bd0",
                     "41f2b5849b50502d31152bc20ec9f81d",
                     "53e96b0214838323def0375b0ac40023",
                     "f8f91289b8db5fa0270ffc0b0c94bd09"])

    def test_makeIdentifiers_2(self):
        self.runner("A B. C D. E F.", 1, ["87a3b6464acc41ca7939fe6e2062a60b",
                                          "049b7a05061ed1478669c23e8bd946c6",
                                          "62131ea41b1bf0363d61c34a72d6b34c",
                                          "1a4273067a5f959ed78a6f571a63ae1c",
                                          "f8f91289b8db5fa0270ffc0b0c94bd09"])

    def test_makeIdentifiers_3(self):
        self.runner(declaration(), 1, ["3beca96390f114e4bb5513aed359e090",
                                       "3e7168dc0ecfc76b1710edb8fb147d41",
                                       "3778793bd861a1bc658c2b55bdc2eaf3",
                                       "8ec3d7d72ffedf1740f04b838a7164b6",
                                       "f8f91289b8db5fa0270ffc0b0c94bd09"])

    def test_makeIdentifiers_4(self):
        self.runner(declaration(), 2, ["9ef701f7a5c1da8eb8d0e87ba63025f6",
                                       "28f7f057e5a5a9a66a0d37686716c9f6",
                                       "56d6a375bb36a4e68b1a1a6e3d194fda",
                                       "1af5996e085f3ba7fe906992ee723513",
                                       "f8f91289b8db5fa0270ffc0b0c94bd09"])

    def test_makeIdentifiers_5(self):
        self.runner(declaration(), 3, ["7c653cc6e226acfb685144581bec0c10",
                                       "06441a60380e2b3915ee9de25019df9f",
                                       "368f35fe0a34ba6984ed4e977cca3687",
                                       "6ce50160bc795d4a8476916d4e688a51",
                                       "f8f91289b8db5fa0270ffc0b0c94bd09"])
