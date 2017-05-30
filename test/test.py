import os
import json
import unittest
import requests

"""
Unittest
Compares each of the possible sorting types against the expected-api-responses.
"""


def load_test_cases():
    "PWD - {0}".format(os.environ['PWD'])
    with open("../resources/expected-api-responses.json") as f:
        return json.load(f)

test_cases = load_test_cases()

class TestApi(unittest.TestCase):
    def test_all(self):
        for t in test_cases["tests"]:
            print("Run test for {0}".format(t["test_url"]))
            self.assertEqual(0, 1)

if __name__ == '__main__':
    unittest.main()
