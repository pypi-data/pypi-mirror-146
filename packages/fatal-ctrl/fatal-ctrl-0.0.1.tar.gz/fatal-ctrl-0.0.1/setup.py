import os
from setuptools import setup, find_packages

path = os.path.abspath(os.path.dirname(__file__))

try:
  with open(os.path.join(path, 'README.md')) as f:
    long_description = f.read()
except Exception as e:
  long_description = "An auto control frame for mouse & keyboard simulation."

setup(
    name = "fatal-ctrl",
    version = "0.0.1",
    keywords = ("pip", "control", "mouse", "autotest", "simulation", "yangyang"),
    description = "An auto control frame for mouse & keyboard simulation.",
    long_description = long_description,
    long_description_content_type='text/markdown',
    python_requires=">=3.5.0",
    license = "MIT Licence",

    url = "https://gitee.com/yy_kuhaha/fatal_control",
    author = "yangyang",
    author_email = "bityyt@126.com",

    packages = find_packages(),
    include_package_data = True,
    install_requires = ["pynput"],
    platforms = "any",

    scripts = [],
    entry_points = {
        'console_scripts': []
    }
)