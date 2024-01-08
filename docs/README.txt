Python module documentation guide:

Code-level API documentation is typically derived from code level docstrings, as documented here:
https://www.python.org/dev/peps/pep-0257/

These docs are accessible via help(function_name) or function_name.__doc__.

You can also compile them into API level documentation that includes the docstring and much more using Sphinx.

To install:
$ pip install Sphinx

To setup Sphinx, run the quickstart and 
http://www.sphinx-doc.org/en/stable/invocation.html

(1) From energyPATHWAYS/doc run initial config, with the following interactive config choices.
Note that you do **not** need to do this if you are using the conf.py that is already set up in the source/ directory.

doc$ sphinx-quickstart

> Root path for the documentation [.]:
> Separate source and build directories (y/n) [n]: y
> Name prefix for templates and static dir [_]:
> Project name: energyPATHWAYS
> Author name(s): Evolved Energy Research
> Project version: 0.0.1
> Project release [0.0.1]:
> Project language [en]:
> Source file suffix [.rst]:
> Name of your master document (without suffix) [index]:
> Do you want to use the epub builder (y/n) [n]:
> autodoc: automatically insert docstrings from modules (y/n) [n]: y
> doctest: automatically test code snippets in doctest blocks (y/n) [n]: n
> intersphinx: link between Sphinx documentation of different projects (y/n) [n]: n
> todo: write "todo" entries that can be shown or hidden on build (y/n) [n]: y
> coverage: checks for documentation coverage (y/n) [n]:
> imgmath: include math, rendered as PNG or SVG images (y/n) [n]:
> mathjax: include math, rendered in the browser by MathJax (y/n) [n]:
> ifconfig: conditional inclusion of content based on config values (y/n) [n]: y
> viewcode: include links to the source code of documented Python objects (y/n) [n]:
> githubpages: create .nojekyll file to publish the document on GitHub pages (y/n) [n]:
> Create Makefile? (y/n) [y]:
> Create Windows command file? (y/n) [y]:

(2) Then auto=generate the Sphinx *.rst files based on the contents of energyPATHWAYS (module dir)
doc$ sphinx-apidoc -o source ../energyPATHWAYS

(3) Render these docs into html
(a) With a make target
doc$ make html
(b) Or with a direct command
doc$ sphinx-build -b html -d build/doctrees source build/html

See results in web browser from: doc/build/html/index.html

(4) to update the automatically generated docs, repeat steps 2 and 3. For convenience, this can be accomplished by running update.sh or update.bat.