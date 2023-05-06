Guide: Rendering using Python
=============================

Fabricius was based on the idea to be able to programmatically create your files.
As such, it uses Python code to tell how a file should render, where to go, from what template, etc.

Let's create a simple template that can be renderer by Python's :py:attr:`str.format`:

.. code-block::
   :caption: template/source.txt

   Hello! I am template!
   Let's render the date of today: {date}

   I use {renderer} for rendering!

Now that we have our template, we need to *actually* render the file.

.. code-block:: python
   :caption: source/conf.py

   from fabricius.file import File
   from datetime import datetime

   def run_me():
       # Create a file object - This won't create the file yet!
       file = File("my_file", "txt")

       # Define the template file - You can also use ".from_content" for string inputs
       file.from_file("template/source.txt")

       # Indicates where the file should go
       file.to_directory("destination/")

       # This is the data that will be sent inside the template
       file.with_data({date: datetime.now(), renderer: "Python's .format"})

       # And finally, save the file!
       file.commit()

       # Alternatively, if you wish to simply generate the file's final content without saving it
       # to the disk, you can use ".generate" which will
       final_content = file.generate()

       >>> print(final_content)
       # Hello! I am template!
       # Let's render the date of today: 2023-02-23 17:39:09.938789

       # I use Python's .format for rendering!

That's it! You have created a file
