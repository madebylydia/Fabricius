Installation
============

Fabricius is available as a PyPi package.
You may not find Fabricius under any other form of distribution.

Install Python
--------------

Because Fabricius is a tool made using Python, it is required to have Python installed on your system.
Do note this is not to download Fabricius itself *yet*.

.. tab-set::

   .. tab-item:: Windows

      There is different method to install Python on your system.
      Feel free to use the method that is the most convenient for you, we'll showcase the most common ones.

      .. tab-set::

         .. tab-item:: Windows Store (Easiest)

            The easiest way to install Python on Windows is to use the Windows Store.

            This link will send you directly to the Microsoft Store page of Python 3.12.

            .. button-link:: ms-windows-store://pdp/?ProductId=9NCVDN91XZQP&mode=mini
               :color: primary
               :outline:

               Install Python 3.12

            Alternatively, you can run the following command in a PowerShell terminal:

            .. code:: powershell

               winget install -e --id Python.Python.3.12

         .. tab-item:: Official Installer

            The Python Software Foundation provides an official installer for Windows, which is like installing any other programs on your computer.

            .. note::

               Be sure to check the ``Add Python to PATH`` option during the installation.

            You can find Python 3.12 on the `Python.org website <https://www.python.org/>`_.

            .. button-link:: https://www.python.org/downloads/
               :color: primary
               :outline:

               Go to download page

         .. tab-item:: Chocolatey

            Chocolatey is a package manager for Windows, similar to ``apt``/``yum``/``pkg`` on Linux.

            You first need to install Chocolatey on your system, you can find the instructions on the `Chocolatey website <https://chocolatey.org/install>`_.

            To install Python using Chocolatey, you can use the following command:

            .. code-block:: bash

               choco install python

         .. tab-item:: Scoop

            Scoop is a similar tool to Chocolatey, they work differently but reach the same goal.

            You first need to install Scoop on your system, you can find the instructions on the `Scoop website <https://scoop.sh/>`_.

            To install Python using Scoop, you can use the following command:

            .. code-block:: bash

               scoop install python

            .. hint::

               Can't find pyton package? Try to update Scoop using ``scoop update``.
               You might also be missing the ``main`` bucket, you can add it using ``scoop bucket add main``.

   .. tab-item:: Linux

      To install Python on Linux, use your distribution's package manager.
      Packages managers like ``apt``, ``yum``, ``pkg``, ``pacman``, etc. are the recommended way to install Python on Linux.

      .. tab-set::

         .. tab-item:: apt (Debian, Ubuntu, etc.)

            To install the latest version of Python on your system, run the following commands:

            .. code-block:: bash

               sudo apt update
               sudo apt install software-properties-common -y
               sudo add-apt-repository ppa:deadsnakes/ppa
               sudo apt update
               sudo apt install python3

         .. tab-item:: yum (CentOS, Fedora, etc.)

            To install the latest version of Python on your system, run the following commands:

            .. code-block:: bash

               sudo yum install -y python3
               sudo yum install -y python3-pip

         .. tab-item:: Pacman (Arch Linux, Manjaro, etc.)

            To install the latest version of Python on your system, run the following commands:

            .. code-block:: bash

               sudo pacman -Syu python
               sudo pacman -Syu python-pip


   .. tab-item:: Mac

      To install Python 3.12 on Mac, there is multiple methods you can follow.
      Their installation method is similar to Windows.

      .. tab-set::

         .. tab-item:: Official Installer

            The Python Software Foundation provides an official installer for Mac, which is like installing any other programs on your computer.

            You can find Python 3.12 on the `Python.org website <https://www.python.org/>`_.

            .. button-link:: https://www.python.org/downloads/macos/
               :color: primary
               :outline:

               Go to download page

         .. tab-item:: Homebrew

            Homebrew is a package manager for Mac, similar to ``apt``/``yum``/``pkg`` on Linux.

            You first need to install Homebrew on your system, you can find the instructions on the `Homebrew website <https://brew.sh/>`_.

            Once installed, you can use the following command:

            .. code-block:: bash

               brew install python@3.12

            .. hint::

               If Python has not been added to your Path automatically, you can add it using the following command:

               .. code-block:: bash

                  echo 'export PATH="$(brew --prefix)/opt/python@3.12/bin:$PATH"' >> "$([ -n "$ZSH_VERSION" ] && echo ~/.zprofile || ([ -f ~/.bash_profile ] && echo ~/.bash_profile || echo ~/.profile))"
                  export PATH="$(brew --prefix)/opt/python@3.12/bin:$PATH"

Ensure Python is installed
^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you're done following the instructions above, please make sure you have Python installed by opening a new terminal on your system.
You can check if Python is installed by running the following command:

.. code-block:: bash

   python --version

Also make sure that ``pip`` is installed by running the following command:

.. code-block:: bash

   python -m pip --version

If one of this command fails, you should check your installation and try again.

Hint, Google's your friend

Installing Fabricius
--------------------

Once Python (and pip) is installed on your system, you can now download Fabricius.

We recommand to not install Fabricius in a virtual environment (As you usually would do) because it is a tool you're supposed to use globally.

You can install Fabricius using different tool, either with ``pip`` or ``pipx``. Feel free to choose whatever you'd prefer.

.. tab-set::

   .. tab-item:: Using pip

      To install Fabricius using ``pip``, you can run the following command:

      .. code-block:: bash

         python -m pip install fabricius

      This is the most straightforward way to install Fabricius.

   .. tab-item:: Using pipx

       More information about pipx can be found `here <https://github.com/pypa/pipx>_`.

       You first need to install pipx on your system using the following command:

       .. code-block:: bash

          python -m pip install pipx

       Once done, you can install Fabricius with the following command:

       .. code-block:: bash

          pipx install fabricius

Ensure Fabricius is installed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To check if Fabricius has been successfully installed on your system, open a new terminal and run the following command:

.. code-block:: bash

   fabricius --version

In case the command fail, it might probably just because the Fabricius's command has not been added to your Path.
Pip should warn you if this is the case, if so, you should follow the instruction given by pip to add Fabricius to your Path.

However, if the command worked just fine, congratulations, you're now ready to use Fabricius! ✨
