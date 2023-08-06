from config_manager import *

import unittest


class ConfigA:
    def __init__(self):
        self.A= 5
        self.B ="ahaha"



class ConfigB:
    def __init__(self):
        self.C = ConfigA()
        self.D = 3.7
        self.E = ConfigA()



class TestCases(unittest.TestCase):
    def test_toDict(self):

        a = ConfigA()
        a.A = 7
        a.B = "ah"

        b = ConfigB()

        b.C.A =99
        b.D = 8

        aSerialized = (toDict(a))
        bSerialzied = (toDict(b))

        self.assertDictEqual({'A': 7, 'B': 'ah'}, aSerialized)
        self.assertDictEqual({'C': {'A': 99, 'B': 'ahaha'}, 'D': 8, 'E': {'A': 5, 'B': 'ahaha'}},
                            bSerialzied)


    def test_fromDict(self):
        a = loadDict(ConfigA(), {'A': 7, 'B': 'ah'})
        b = loadDict(ConfigB(), {'C': {'A': 99, 'B': 'ahaha'}, 'D': 8, 'E': {'A': 5, 'B': 'ahaha'}})
        


        aSerialized = (toDict(a))
        bSerialzied = (toDict(b))

        self.assertDictEqual({'A': 7, 'B': 'ah'}, aSerialized)
        self.assertDictEqual({'C': {'A': 99, 'B': 'ahaha'}, 'D': 8, 'E': {'A': 5, 'B': 'ahaha'}},
                            bSerialzied)

    def test_makeModuleConfig(self):
        mConfig = (makeModuleConfig("testConfig", "ConfigB"))
        serialized = (mConfig.toDict())

        loaded = loadDict(ModuleConfig(), serialized)
        self.assertDictEqual(serialized, loaded.toDict())
