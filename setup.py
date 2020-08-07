# Copyright 2019 TerraPower, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Setup.py script for Hallam ARMI plugin"""

from setuptools import setup, find_namespace_packages

with open("README.md") as f:
    README = f.read()

setup(
    name="happ",
    version="0.1",
    description=("ARMI plugin for Hallam"),
    author="Nick Touran",
    author_email="ntouran@terrapower.com",
    packages=find_namespace_packages(),
    package_data={"happ": []},
    license="Apache 2.0",
    long_description=README,
    install_requires=["armi", "jinja2"],
    keywords=["ARMI"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: Apache Software License",
    ],
    test_suite="tests",
    include_package_data=True,
)
