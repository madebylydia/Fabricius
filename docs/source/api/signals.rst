Signals
=======

Signals are `observers <https://refactoring.guru/design-patterns/observer>`_.
They permit you to run code when a specific action is happening.

There is a lot of signal that Fabricius raises so you can subscribe to any thing you'd like.
For example, before committing a file, you can add a suffix to its name before it get committed.

.. code-block:: py

   from fabricius.app.signals import before_file_commit
   from fabricius.models.file import File

   on_file_commit(file: File):
       file.name = f"{file.name}.template"

   before_file_commit.connect(on_file_commit)

Here is a list of the available signals raised in Fabricius.

.. automodule:: fabricius.app.signals
   :members:
