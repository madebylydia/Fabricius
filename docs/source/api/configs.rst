Configs
=======

This page will present you the configs object you can use in Fabricius to have a fully typed template.
By using these objects, you make sure your project can be rendered as expect without even running it.

Fabricius expect you to create a new file to tell him what you want. This file is called `forge.py`.
Using a Python file has different advantages:

1. You can have a typed environment.
2. You can be dynamic.
3. You can run your own code.

This might also sound scary, but fear not! Fabricius will try its best to protect you from unexpected behavior.

.. warning::
   As Fabricius is still a WIP, security functionalities are not yet implemented.


.. autoclass:: fabricius.configs.setup.SetupV1
   :members:


.. autoclass:: fabricius.configs.setup.QuestionV1
   :members:
