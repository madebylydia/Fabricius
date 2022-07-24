from abc import ABC, abstractmethod

from fabricius.const import Data


class RendererContract(ABC):
    """
    A class with purpose to render a string with data given on initialization.

    .. property:: data

       A dictionary that contains data that has been passed to the renderer.
       Useful to render in a file.

       :type: :py:data:`.Data`
    """

    data: Data

    def __init__(self, data: Data) -> None:
        self.data = data

    @abstractmethod
    def render(self, content: str) -> str:
        """
        Render a string.

        Example:

        .. code-block:: python

           class MyRenderer(RendererContract):

               def render(self, content: str) -> str:
                   return content.format(self.data)

           content = MyRenderer({"thing": "world"}).render('Please render the {thing}!')
           print(content)
           # Please render the world!
        """
        raise NotImplementedError()
