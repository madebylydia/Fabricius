Renderers
=========

The "Renderer" is a class that is created in order to generate the content of a template.

Fabricius ships many by default, you can use them, or create your own if you feel the need to.

.. code-block:: py

   from fabricius.renderers import Renderer

   class MyRenderer(Renderer):

       # You must implement the "render" method, this will be called by Fabricius.
       def render(self, content: str):
           # Inside of the Renderer class, the "data" property is available.
           # This is where the data is stored.

           final_content = render_content(content=content, data=self.data)

           return final_content

   renderer = MyRenderer({"name": "John"})
   final_content = renderer.render("Hello {{ name }}")
   print(final_content)
   # Hello John

The following is the list of the available renderer packaged with Fabricius. It contains Python's str.format, string template, Mustache & Jinja.

.. hint::

   If you're using the :py:class:`File <fabricius.models.file.File>` object, you can use methods :py:meth:`File.use_jinja() <fabricius.models.file.File.use_jinja>` to set the renderer to one of Fabricius's available.
   To use your own Renderer, use :py:meth:`File.with_renderer() <fabricius.models.file.File.with_renderer>`.

.. automodule:: fabricius.renderers
   :members:
   :imported-members:
