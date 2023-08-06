from setuptools import setup, find_packages
import codecs

with codecs.open("README.md", encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "1.0.0"
DESCRIPTION = "Execute JavaScript Code From Python."

# Setting up
setup(
    name="py_js_runner",
    version=VERSION,
    author="Yasir",
    author_email="<yasirsadman@outlook.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=["python", "javascript", "js", "runjsfrompython"],
)
