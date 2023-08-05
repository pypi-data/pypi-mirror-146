**************
 nutratracker
**************

.. image:: https://badgen.net/pypi/v/nutra
    :target: https://pypi.org/project/nutra/
    :alt: Latest version unknown|
.. image:: https://api.travis-ci.com/nutratech/cli.svg?branch=master
    :target: https://travis-ci.com/nutratech/cli
    :alt: Build status unknown|
.. image:: https://pepy.tech/badge/nutra/month
    :target: https://pepy.tech/project/nutra
    :alt: Monthly downloads unknown|
.. image:: https://img.shields.io/pypi/pyversions/nutra.svg
    :alt: Python3 (3.4 - 3.10)|
.. image:: https://badgen.net/badge/code%20style/black/000
    :target: https://github.com/ambv/black
    :alt: Code style: black|
.. image:: https://badgen.net/pypi/license/nutra
    :target: https://www.gnu.org/licenses/gpl-3.0.en.html
    :alt: License GPL-3

Extensible command-line tools for nutrient analysis.

*Requires:*

- Python 3.4.0 or later (lzma, ssl & sqlite3 modules) [works on winXP]
- Packages: see `setup.py` or `requirements.txt` (and `config/requirements-\*.txt`)
- Internet connection, to download food database & package dependencies


See nt database:   https://github.com/nutratech/nt-sqlite

See usda database: https://github.com/nutratech/usda-sqlite

Notes
=====

On macOS and Linux, you may need to add the following line to
your ``.profile`` or ``.bashrc`` file:

.. code-block:: bash

    export $PATH=$PATH:/usr/local/bin

On Windows you should check the box during the Python installer
to include ``Scripts`` directory in your ``$PATH``.  This can be done
manually after installation too.

Windows users may manually attempt to install search enhancing
library ``python-Levenshtein`` via running:

.. code-block:: bash

    pip3 install python-Levenshtein

    or

    pip3 install -r config/requirements-optional.txt

Install PyPi release (from pip)
===============================
``pip3 install nutra``

(**Note:** use ``pip3`` on Linux/macOS)

**Update to latest**

``pip3 install -U nutra``

**Subscribe to the development release**

``pip3 install --pre -U nutra``

Using the source-code directly
##############################
.. code-block:: bash

    git clone git@github.com:nutratech/cli.git
    cd cli
    git submodule update --init

    pip3 install -r requirements.txt
    ./nutra init

or install from source,

.. code-block:: bash

    git clone git@github.com:nutratech/cli.git
    cd cli
    git submodule update --init

    make install  # python3 setup.py --quiet install
    nutra init

If installed or inside ``cli`` folder, can also run with ``python3 -m ntclient``

When building the PyPi release use the commands:

.. code-block:: bash

    make build  # python3 setup.py --quiet sdist
    twine upload dist/nutra-X.X.X.tar.gz

Running tests
==============

You will need the test dependencies.  (Similarly, you will need the lint dependencies to run ``make lint``)

For recent versions of Linux, macOS, and Windows:

.. code-block:: bash

    pip3 install -r config/requirements-test.txt

For Windows XP (Python 3.4) use:

.. code-block:: bash

    pip3 install -r config/requirements-win_xp-test.txt

To run the tests, run this in the cloned folder:

.. code-block:: bash

    make test  # python3 test.py

Argcomplete (tab completion on Linux/macOS)
===========================================

After installing nutra, argcomplete package should also be installed,

Simply run the following out of a bash terminal:

.. code-block:: bash

    activate-global-python-argcomplete

Then you can press tab to fill in or complete subcommands and to list argument flags.

Currently Supported Data
========================

**USDA Stock database**

- Standard reference database (SR28)  `[7794 foods]`


**Relative USDA Extensions**

- Flavonoid, Isoflavonoids, and Proanthocyanidins  `[1352 foods]`

Usage
=====

Requires internet connection to download initial datasets.  Run ``nutra init`` for this step.

Run the ``nutra`` script to output usage.

Usage: ``nutra [options] <command>``


Commands
########

::

    usage: nutra [-h] [-v] [-d] [--no-pager]
                 {init,nt,search,sort,anl,day,recipe,bio} ...

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -d, --debug           enable detailed error messages
      --no-pager            disable paging (print full output)

    nutra subcommands:
      {init,nt,search,sort,anl,day,recipe,bio}
        init                setup profiles, USDA and NT database
        nt                  list out nutrients and their info
        search              search foods by name, list overview info
        sort                sort foods by nutrient ID
        anl                 analyze food(s)
        day                 analyze a DAY.csv file, RDAs optional
        recipe              list and analyze recipes
        bio                 view, add, remove biometric logs
