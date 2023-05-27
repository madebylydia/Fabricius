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
       # See below for explanations.
       run(template)

API
---

The following functions are available as part of the little API you can use to generate :py:class:`fabricius.models.template.Template` objects from a CookieCutter repo.

The ``setup`` function will:

1. Get the template path
2. Create the Template object and add the extensions, if the project templates specify any others, add them too.
3. Add ``_template``, ``_repo_dir`` and ``_output_dir`` to the context
4. Obtain the questions in the project template and begin to ask to the users those questions.
5. Once all answered, add the extra context the user's default context, then add the answers to the final context.
6. Obtain all the files that must be rendered/copied, and add them to the Template object, and push the data to the Template object.
7. Connect the hooks to the ``before_template_commit`` and ``after_template_commit`` signals, then return the Template object.

While you can just simply do :py:meth:`Template.commit() <fabricius.models.template.Template.commit>`, there is a few things to considerate first since you're rendering a CookieCutter project, and not a Fabricius one.
Thus, we have made the ``run`` function to handle a few edge cases that could happens with CookieCutter.

The ``run`` function will:

1. First attempt to commit the project
2. If fail, due to a file that already exist, ask the user if overwriting files should be used.
3. If fail, due to a hook failing, see if the exception gives an exit code, if it does, exit using the exit code, if not, print the exception and exit.
4. Return the list of file commit result.


.. automodule:: fabricius.readers.cookiecutter.setup
   :members: setup, run
   :noindex:
