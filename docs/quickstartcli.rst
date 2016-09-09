.. _quickstartcli:

Getting Started
============

.. _installation:

Installation
+++++++

Install python dependencies: `emcee`, `corner`, `pandas`,
`matplotlib-1.5.1`, `cython (tested with 0.22)`, `astropy`,
`pdflatex` (installed and in your system's path):

.. code-block:: bash

    $ pip install emcee corner pandas matplotlib-1.5.1 cython astropy

Make sure that ``pdflatex`` is installed and in your system's
path. You can get ``pdflatex`` by installing the `TexLive package
<https://www.tug.org/texlive/>`_ or other LaTeX distributions.

If ``git`` is installed on your system then clone the repository:

.. code-block:: bash

    $ git clone https://github.com/California-Planet-Search/radvel.git

If ``git`` is not installed in your system then download ``radvel``
directly from github web interface: `RadVel on GitHub <https://github.com/California-Planet-Search/radvel>`_

Run the `setup.py` script from within the main repo directory:

.. code-block:: bash
		
    $ cd radvel
    $ python setup.py install



Example Fit
+++++++

Test your installation by running through one of the included
examples. We will use the ``radvel`` command line interface to execute a fit.

The ``radvel`` binary should have been automatically placed in your system's path by the
``python setup.py install`` command (see :ref:`installation`).

First lets look at ``radvel --help`` for the available options:

.. code-block:: bash
		
    $ radvel --help
    usage: radvel [-h] {fit,plot,mcmc,derive,bic,table,report} ...

    RadVel: The Radial Velocity Toolkit

    optional arguments:
        -h, --help            show this help message and exit

    subcommands:
    {fit,plot,mcmc,derive,bic,table,report}


Here is an example workflow to
run a simple fit using the included `HD164922.py` example
configuration file:

Perform a maximum-likelihood fit. You should almost always do this first:

.. code-block:: bash

    $ radvel fit -s /path/to/HD164922.py

   
By default the results will be placed in a directory with the same name as
your planet configuration file (without `.py`, e.g. `HD164922`). You
may also specify an output directory using the ``-o`` flag.

After the maximum-likelihood fit is complete the directory should have been created
and should contain one new file:
`HD164922/HD164922_post_obj.pkl`. This is a ``pickle`` binary file
that is not meant to be human-readable but lets make a plot of the
best-fit solution contained in that file:

.. code-block:: bash

    $ radvel plot -t rv -s /path/to/HD164922.py

This should produce a plot named
`HD164922_rv_multipanel.pdf` that looks something like this.

.. image:: plots/HD164922_rv_multipanel.png

Next lets perform the Markov-Chain Monte Carlo (MCMC) exploration to
assess parameter uncertainties.

.. code-block:: bash

    $ radvel mcmc -s /path/to/HD164922.py

Once the MCMC chains finish running there will be another new file
called `HD164922_mcmc_chains.csv.tar.bz2`. This is a compressed csv
file containing the parameter values and likelihood at each step in
the MCMC chains.

Now we can update the RV time series plot with the MCMC
results and generate the full suite of plots.

.. code-block:: bash

    $ radvel plot -t rv corner trend -s /path/to/HD164922.py

Then create a LaTeX document and corresponding PDF to summarize the
results.

.. code-block:: bash

    $ radvel report -s /path/to/HD164922.py

The report PDF will be saved as `HD164922_results.pdf`. It should
contain a table reporting the parameter values and uncertainties, a
table summarizing the priors, the RV time-series plot, and a corner
plot showing the posterior distributions for all free parameters.


Optional Features
+++++++++++

Combine the measured properties of the RV time-series with
the properties of the host star defined in the setup file to
derive physical parameters for the planetary system.

.. code-block:: bash

    $ radvel derive -s /path/to/HD164922.py

Generate a corner plot for the derived parameters. This plot will also be
included in the summary report if available.

.. code-block:: bash

    $ radvel plot -t derived -s /path/to/HD164922.py

Perform a model comparison testing models with progressively fewer
planets. If this is run a new table will be included in the summary report.

.. code-block:: bash

    $ radvel bic -t nplanets -s /path/to/HD164922.py

Generate and save only the TeX code for any/all of the tables.

.. code-block:: bash

    $ radvel table -t params priors nplanets -s /path/to/HD164922.py
