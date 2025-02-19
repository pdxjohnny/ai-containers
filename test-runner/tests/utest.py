# Copyright (c) 2024 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys

import pytest
import yaml
from hypothesis import given
from hypothesis.strategies import dictionaries, text

sys.path.append(os.environ.get("PWD"))
# pylint: disable-next=wrong-import-position
from utils.test import Test


@pytest.fixture
def test_input():
    "PyTest input fixture."
    tests_list = []
    tests_json = []
    with open("tests.yaml", "r", encoding="utf-8") as test_file:
        try:
            tests_json = yaml.full_load(test_file)
        except yaml.YAMLError as yaml_exc:
            pytest.raises(yaml_exc)
            for test in tests_json:
                tests_list[test] = tests_json[test]
    return [Test(name=test, **tests_list[test]) for test in tests_list]


def test_container_run(test_input):
    "Test container_run() method."
    for idx, test in enumerate(test_input):
        if hasattr(test, "img") and not hasattr(test, "serving") and idx == 0:
            log, returncode = test.container_run()
            assert returncode == 0
            assert log == "expandvars"


def test_container_run_serving(test_input):
    "Test container_run() method with serving input."
    for test in test_input:
        if hasattr(test, "img") and hasattr(test, "serving"):
            log, returncode = test.container_run()
            assert returncode == 0
            assert log == "Python 3.11.7"


def test_run(test_input):
    "test run() method."
    for test in test_input:
        if not hasattr(test, "img"):
            log, returncode = test.run()
            assert returncode == 0
            assert log == "Hello World"


@given(name=text(), arguments=dictionaries(text(), text()))
def test_fuzz_container_run(name, arguments):
    "Fuzz container_run()."
    try:
        test = Test(name=name, **arguments)
        test.container_run()
    except Exception as e:
        print(f"Caught exception: {e}")


@given(name=text(), arguments=dictionaries(text(), text()))
def test_fuzz_run(name, arguments):
    "Fuzz run()."
    try:
        test = Test(name=name, **arguments)
        test.run()
    except Exception as e:
        print(f"Caught exception: {e}")
