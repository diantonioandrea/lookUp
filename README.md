# lookUp

<!-- Description -->
Make sure to take a look at the [contributing guidelines](https://github.com/diantonioandrea/lookUp/blob/main/.github/CONTRIBUTING.md).

## Installation

### Prerequisites

There are some Python modules that need to be installed in order to compile and use **lookUp**.

* pyinstaller: compilation of **lookUp**.

As a one-liner:

	python3 -m pip install --upgrade pyinstaller

### Compiling and installing from source

**lookUp** can be compiled[^1] by:

	make PLATFORM

where PLATFORM must be replaced by:

* windows
* unix (Linux and macOS)

based on the platform on which **lookUp** will be compiled.  
**lookUp** can be then installed[^2] by:

	./lookUp install

or

	.\lookUp.exe install

on Windows.

[^1]: The Makefile for the Windows version is written for [NMAKE](https://learn.microsoft.com/en-gb/cpp/build/reference/nmake-reference?view=msvc-170).
[^2]: This is the only way to install **lookUp**.