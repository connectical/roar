
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name         = "roar",
    version      = "0.1.2",
    scripts      = ["roar"],

    description  = "Static website generator based on Growl",
    url          = "http://github.com/Connectical/roar",
    author       = "Adrian Perez",
    author_email = "aperez@connectical.com",
    classifiers  = ["Environment :: Console",
                    "Development Status :: 4 - Beta",
                    "Intended Audience :: Developers",
                    "Intended Audience :: End Users/Desktop",
                    "License :: OSI Approved :: GNU General Public License (GPL)",
                    "Natural Language :: English",
                    "Operating System :: OS Independent",
                    "Programming Language :: Python :: 2",
                    "Topic :: Internet :: WWW/HTTP :: Site Management"],
)
