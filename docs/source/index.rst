Fabricius: The Documentation
============================

.. module:: fabricius

**Fabricius: Python templates renderer**

Fabricius is a tool that allows you to render files template & projects template.

Key features of Fabricius:

- (Will) Ship with its own project templating solution
- Supports CookieCutter templates
- Extendable with `observers <https://refactoring.guru/design-patterns/observer>`_ (AKA signals)
- User-friendly API

Installation
------------

The primary requirement of Fabricius is `Python <https://python.org>`_.
It must be a version equal to or greater to Python ``3.10``.

You can install Fabricius using ``pip``, the Python's package manager (It comes bundled with Python). Install Fabricius using the following command:

.. code-block::

   pip install Fabricius

.. note::

   Typically, Fabricius should be installed globally on your system (As you shouldn't need it in a specific project, it's a tool).
   As such, Windows might tell you to add the ``--user`` option, if so, try doing ``pip install fabricius --user``!

Guides
------

.. important::
   Guides are not ready yet!

   Fabricius need more time to get ready! While we're working on the documentation too, Fabricius is **not ready**!
   Guides (for now) are here to show you how Fabricius can work  and how you should expect things to work out.

.. toctree::
   :caption: Guides
   :maxdepth: 1

   guides/guide_create_forge_file
   guides/guide_rendering
   guides/guide_cookiecutter_templates


API
---

.. topic:: Careful here, commander!

   This section is reserved for the peoples that are interested to use more complex tools in order to better understand how Fabricius works behind the scene & use it themselves.

   If you believe your use case is easy to tackle down, then you probably don't need to dig into the Fabricius's API.


.. toctree::
   :caption: API
   :maxdepth: 2

   api/models
   api/renderers
   api/types
   api/signals
   api/configs
   api/exceptions
