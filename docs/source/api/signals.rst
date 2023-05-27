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


Create your own signals
-----------------------

You can create your own signal by creating a :py:class:`fabricius.models.signal.Signal` object and letting it available in your project.

.. code-block:: py

   from fabricius.models.signal import Signal

   my_signal = Signal()

While this is totally OK to go like this, you can also optionally type the :py:meth:`.send() <fabricius.models.signal.Signal.connect>`/:py:meth:`.connect() <fabricius.models.signal.Signal.connect>` methods by providing a function.
Fabricius will extract the function's signature and use it to transfer the arguments into the signal's methods.

.. code-block:: py

   from fabricius.models.file import File
   from fabricius.models.signal import Signal

   def my_signal_hint(file: File):
       ...

   my_signal = Signal(func_hint=my_signal_hint)

   my_signal.send(File("test.py"))  # This is OK
   my_signal.send()  # This is not! Your type checker will complain!

   # Good
   def signal_receiver(file: File):
       ...
   my_signal.connect(signal_receiver)

   # Bad
   def signal_receiver(receiving_file: File):
       ...
   my_signal.connect(signal_receiver)

   # This will raise a type error if the function's signature is altered
   # (New, removed, renamed arguments, etc...)
