.. Fabricius documentation master file, created by
   sphinx-quickstart on Tue Jun 28 17:27:26 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Fabricius - Documentation!
==========================

Fabricius: Python modular render of template engine & project scaffolding.

Example
-------

.. code-block:: python

   from fabricius import Generator

   def create_files():
       # Create the generator
       generator = Generator()

       # Add a file at "source/core.py"
       file = generator.add_file("core", "py")
       file.from_file("template-core.mustache").to_directory("source").with_data({"name": "My Module"}).use_mustache()

       # Add a file at "tests/test.py"
       file = generator.add_file("test", "py")
       file.from_file("template-test.txt").to_directory("tests").with_data({"name": "My Module"})

       # Create the files!
       generator.execute()

Links
-----

.. toctree::
   :maxdepth: 2
   :caption: Guides:

   guide_rendering

.. toctree::
   :maxdepth: 2
   :caption: Fabricius API

   api/objects
   api/constants
   api/contracts


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
