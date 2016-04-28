dympy
=====

A tool to run Dymola commands from python
Check the below example for a quickstart or the docstrings for a more complete guide.

Installation
------------
requires:
- ``numpy``
- ``scipy``
- ``pywin32`` `available here <http://sourceforge.net/projects/pywin32/files/pywin32/>`_.

To install download the latest `release <https://github.com/BrechtBa/dympy/releases>`_., unpack, cd to the unpacked folder and run::

	python setup.py install


Example
-------

First initialize the Dymola connection. It is good practice to clear all open models from Dymola after initialization to avoid redefinition conflicts, however this is not necessary::

	dymola = dympy.Dymola()
	dymola.clear()

Next we'll open a model and compile it::

	dymola.openModel('example.mo')
	dymola.compile('example')

Parameters can be changed using the ``set_parameters`` method. The method takes a dictionary with name, value pairs as input.
Inputs can be written to a dsu.txt file  using the ``write_dsu`` method. The method again takes a dictionary with name, value pairs as input, ``time`` must always be one of the inputs::

	dymola.set_parameters({'C_in.C':5e6,'C_em.C':10e6,'UA_em_in.G':1600,'UA_in_amb.G':200})
	dymola.set_parameters({'C_em.T':300})
	dymola.write_dsu({'time':[0,43200,86400],'Q_flow_hp':[1000,5000,2000],'T_amb':[273.15,278.15,273.15]})


The simulation can now be started within a certain time range::

	dymola.simulate(StopTime=86400)


After the simulation is finished you can load the results as a dictionary using ``get_result()``.
The result is a dictionary with the variable names in dot notation as keys::

	res = dymola.get_result()
	print(res.keys())

There is also a ``get_res`` method implemented which will return all result keys which are children of the supplied argument key.
If the argument has no children it's value is returned::

	dymola.get_res('UA_em_in')


