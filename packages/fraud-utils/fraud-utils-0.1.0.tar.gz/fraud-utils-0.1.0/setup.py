import pathlib
import sys
from distutils.core import setup
from distutils.command.install import install as _install
from params import PACKAGE_NAME, PACKAGE_VERSION

class install(_install):
    def run(self):
        print("Wrong repo from public pypi")
        sys.exit(1)
        _install.run(self)

HERE = pathlib.Path(__file__).parent

setup(
    cmdclass={'install': install},
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    description="Public version of the package",
    long_description="Public version of the package",
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=[PACKAGE_NAME],
    include_package_data=True,
)