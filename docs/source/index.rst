Fabricius: The Documentation
============================

**Fabricius: Python modular render of template engine & project scaffolding.**

Thank for reading the Fabricius's documentation! We hope you will enjoy reading it and hope you will use our tool!



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

Rendering with Python
^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   guides/guide_rendering

Rendering from a template project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   guides/guide_project_rendering

Fabricius API
^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   api/fabricius
   api/fabricius.generator
   api/fabricius.plugins

..    api/modules
