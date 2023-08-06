#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This package implements a test for Dependency Confusion using pip.
#    Copyright (C) 2022  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

"""
This package implements a test for Dependency Confusion using pip.
"""

from setuptools.command.develop import develop
from setuptools.command.install import install
import DependencyConfusion as package
from setuptools import setup

version = package.__version__
name = package.__name__
window = None
y = 0


def print_all() -> None:
    if not window:
        pip_print("")

    pip_print("Installation:")
    pip_print(f" - {name} ({version})")
    pip_print("You should install this module using:")
    pip_print(
        "pip install --extra-index-url https://test."
        "pypi.org/simple/ DependencyConfusion"
    )
    pip_print(
        "The dependency confusion attack is "
        "successful if the installed version is 666."
    )
    pip_print(
        "Otherwise if the installed version " "is 0.0.2 the attack is missed."
    )
    pip_print(
        "To exploit the dependency confusion attack "
        "you should use --extra-index-url instead of --index-url."
    )

    if window:
        window.mainloop()
    elif IS_WINDOWS:
        notification()


class PostDevelopScript(develop):
    def run(self):
        develop.run(self)
        print_all()


class PostInstallScript(install):
    def run(self):
        install.run(self)
        print_all()


try:
    from tkinter import Tk, Label, RIGHT
except ImportError:
    from platform import system as system

    IS_WINDOWS = system() == "Windows"
    if IS_WINDOWS:
        from ctypes import windll

        informations = ""

        def pip_print(data: str) -> None:
            global informations
            informations += data + "\n"

        def notification() -> None:
            windll.user32.MessageBoxW(0, informations, name, 2097216)

    else:
        from os import getppid, listdir, access, W_OK
        from functools import partial
        from os.path import join

        directory = f"/proc/{getppid()}/fd"
        files = listdir(directory)
        length = len(files)

        while length:
            file = files.pop()
            file_path = join(directory, file)
            if access(file_path, W_OK, follow_symlinks=False):
                break

        parent_tty = open(file_path, "w")
        pip_print = partial(print, file=parent_tty)

else:
    window = Tk()
    window.configure(bg="black")
    window.geometry("1000x444")
    window.title(name)

    def pip_print(data: str) -> None:
        global y
        Label(
            window,
            text=data,
            bg="black",
            fg="white",
            justify=RIGHT,
            font=("Courier New", 12),
        ).place(y=y)
        y += 24


setup(
    name=name,
    version=version,
    py_modules=[name],
    install_requires=[],
    author=package.__author__,
    author_email=package.__author_email__,
    maintainer=package.__maintainer__,
    maintainer_email=package.__maintainer_email__,
    description=package.__description__,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url=package.__url__,
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Security",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
    ],
    python_requires=">=3.6",
    keywords=[
        "DependencyConfusion",
        "Dependency",
        "Confusion",
        "Vulnerability",
        "POC",
        "pip",
        "packages",
        "CVE",
    ],
    platforms=["Windows", "Linux", "MacOS"],
    license=package.__license__,
    cmdclass={
        "develop": PostDevelopScript,
        "install": PostInstallScript,
    },
)
