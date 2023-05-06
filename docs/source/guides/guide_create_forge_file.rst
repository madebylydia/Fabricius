Guide: Create your Forge file
=============================

The Forge file is a file created in either your repo or in a template that allows you to define what Fabricius will do. Basically, it's a configuration file, like the `cookiecutter.json` for CookieCutter.
The difference with other tools is that we use a Python file to allows you more customization, with this approach, you can not only define how you want to create your template(s), but also:

1. Run some code you've made yourself instead of launching Fabricius (It's up to you to create files! Perfect for use with the :py:class:`Generator <fabricius.generator.Generator>`!)
2. Add plugins when running Fabricius
3. Have a fully type-hinted/type-safe config file


