Guide: Rendering programmatically
=================================

Fabricius was based on the idea to be able to programmatically create your files.
As such, it uses Python code to tell how a file should be renderer, where to go, from what template, etc.
You can manually create a :py:class:`.FileGenerator` object, or you can also uses :py:class:`.Generator` to create multiple files at one time and get a feedback on your terminal.

Let's create a simple template that can be renderer by Python's :py:attr:`str.format`:

.. code-block::
   :caption: template/source.txt

   Hello! I am template!
   Let's render the date of today: {date}

   I use {renderer} for rendering!

Now that we have our template, we need to *actually* render the file.

.. code-block:: python
   :caption: source/conf.py

   from fabricius import FileGenerator
   from datetime import datetime

   def run_me():
       file = FileGenerator("my_file", "txt")

       # Define the template file - You can also use .from_content
       file.from_file("template/source.txt")

       # Define the destination
       file.to_directory("destination/")

       # Include the data to pass for rendering
       file.with_data({date: datetime.now(), renderer: "Python's .format"})

       # And finally, save the file!
       file.commit()

       # If you wish to simply generate the file's content without saving it, you can use .generate
       final_content = file.generate()

   run_me()
