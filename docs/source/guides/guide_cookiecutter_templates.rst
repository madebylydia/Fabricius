Guide: Rendering CookieCutter templates
=======================================

Fabricius ships with the ability to process CookieCutter templates (Or so called, cookiecutters by themselves).
This mean that all of the work you've already done using CookieCutter **is 100% supported** in Fabricius! (yes! hooks work too!)

Using the CLI
-------------

TBD

Using the API
-------------

You can also use Fabricius's API to generate your CookieCutter template.

.. code-block:: python

   from fabricius.readers.cookiecutter.setup import setup, run

   def main():
       template_path = "path/to/template"
       output_path = "path/to/output"
       template = setup(template_path, output_path)

       # This method has been specially created for CookieCutter's solution.
       # It basically commits the template using template.commit(), but it handles some issues,
       # like hooks raising an error and exiting the application.
       run(template)

API
---

.. automodule:: fabricius.readers.cookiecutter.setup
   :members: setup, run
   :noindex:
