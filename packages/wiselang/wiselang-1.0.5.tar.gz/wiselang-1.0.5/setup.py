from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.5'
DESCRIPTION = 'A Wise language, for wise members of AUI'
LONG_DESCRIPTION = 'WiseLang is a fun parody language of AUI, from AUI and for the AUI, hoping that everyone would be successful like our great sir Chintu!'

# Setting up
setup(
    name="wiselang",
    version=VERSION,
    author="BLA4KM4MBA, SEG-V",
    author_email="tarunpreetsingh@protonmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    project_urls={
        "Website": 'https://bla4km4mba.github.io/wiselang-site',
	"Wiki": "https://github.com/BLA4KM4MBA/WiseLang/wiki",
	"Docs": "https://bla4km4mba.github.io/wiselang-site/docs.html",
    },
    install_requires=['sly'],
    keywords=['python', 'language', 'esoteric', 'wise', 'hindi'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
