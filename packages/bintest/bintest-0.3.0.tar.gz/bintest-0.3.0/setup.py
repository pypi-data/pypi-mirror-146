# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bintest']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'scripttest>=1.3,<2.0']

setup_kwargs = {
    'name': 'bintest',
    'version': '0.3.0',
    'description': 'python library for test binarys',
    'long_description': '# Bintest\n\nBintest is a extension for `unitest`, it will provide a way to run a command and assert the output.\n\n## Installation\n\n``` shell\npip install bintest\n```\n\n### Usage\n\n1. Create a file in your project: testcase.py for example\n``` python\nfrom bintest import bintest\nimport unittest\n\n\nclass MyTestCase(unittest.TestCase, bintest.BinTest):\n    __test__ = True\n\n    def setUp(self):\n        self.set_env(\n            env="./output",  # temp dir\n            input="./tests_case.yml",  # yml file\n        )\n\n    # This works\n    def test_simple_cat(self):\n        output, err = self.run_bin(name="SimpleCAT")\n        # two ways of test, this both will do exactly the same\n        self.assertEqual(output, "test\\n")\n        # this one is more auto because is reading from the yml\n        self.assertOutput(name="SimpleCAT", output=output)\n\n    # This Fails\n    def test_simple_cat_fail(self):\n        output, err = self.run_bin(name="SimpleCATFail")\n        # this one will fail\n        self.assertOutput(name="SimpleCATFail", output=output)\n\n\nif __name__ == "__main__":\n    unittest.main()\n```\n\n2. Create the config file: tests_case.yml\n\n``` yaml\n---\n\n# Example test file\n# required: bin, output\n# everything in the middle will be passing as paramters to the binary: only the values\n\nSimpleCAT:\n  bin: /bin/cat\n  path: /Users/artur.gomes/projects/pybintest/examples/test.txt\n  output: "test\\n"\n\nSimpleCATFail:\n  bin: /bin/cat\n  path: /Users/artur.gomes/projects/pybintest/examples/test.txt\n  output: "not test\\n"\n```\n\nIn this case we are testing the cat command, using a file test.txt as argument and expecting the output\n\n3. Create the test.txt file\n\n``` sh\ntest\n```\n\n\n4. Then run:\n\n``` shell\npython3 -m unittest discover  -vvv\n```\n\n5. Unittest will find yout test and run it for you.\n\n``` shell\ntest_simple_cat (testcase.MyTestCase) ... ok\ntest_simple_cat_fail (testcase.MyTestCase) ... FAIL\n\n======================================================================\nFAIL: test_simple_cat_fail (testcase.MyTestCase)\n----------------------------------------------------------------------\nTraceback (most recent call last):\n  File "/Users/artur.gomes/projects/test_bintest/testcase.py", line 26, in test_simple_cat_fail\n    self.assertOutput(name="SimpleCATFail", output=output)\n  File "/Users/artur.gomes/Library/Caches/pypoetry/virtualenvs/test-bintest-LukI1uz2-py3.9/lib/python3.9/site-packages/bintest/bintest.py", line 34, in assertOutput\n    raise self.failureException(msg)\nAssertionError: Error: not test\n != test\n\n\n----------------------------------------------------------------------\nRan 2 tests in 0.011s\n\nFAILED (failures=1)\n```\n\n## Contribution\n\nIf this helps you consider help me to improve.\n',
    'author': 'Artur Gomes',
    'author_email': 'contato@arturgomes.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/arturgoms/python-bintest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
