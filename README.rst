Onboarding POC
==============

Simple Django application proof of concept for a minimal, reusable user onboarding service using `phone number` and `email`
as the primary identifers.

How To Run The Project
======================

This assumes that you are running on any `*nix` environment and have `Python 3.10+` and `git` installed
in your local machine.

1. Clone the repository

.. code-block:: bash

    $ git clone git@github.com:ageeknamedslickback/onboardingServicePOC.git
    $ cd onboardingServicePOC

2. Create and activate a virtual environment to run your code

.. code-block:: bash

    $ python3 -m venv <name of your venv>
    $ source <name of your venv>/bin/activate

3. Install dependancies

.. code-block:: bash

    $ pip3 install -r requirements.txt

4. Create an `env.sh` file and add the following

.. code-block:: bash

    export SECRET_KEY="<your secret key>"
    export DEBUG="true"
    export ENVIRONMENT="local"
    export PORT=8000
    export SENTRY_DSN=""

5. Remember to source your environment variables

.. code-block:: bash

    $ source env.sh


6. Run `migrations` (code uses SQLite thus no further configs), `collectstatic` and the `runserver`

.. code-block:: bash

    $ python3 manage.py migrate
    $ python3 manage.py collectstatic
    $ python3 manage.py runserver

    Watching for file changes with StatReloader
    Performing system checks...

    System check identified no issues (0 silenced).
    May 18, 2023 - 21:47:51
    Django version 4.2.1, using settings 'config.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

How To Test The Project
=======================

.. code-block:: bash

    $ tox -r

How To Run the Project Using Docker
===================================

This assumes that you have `Docker Desktop` installed locally in your `*nix` local machine

1. Build the image

.. code-block:: bash

    $ make build

2. Run the docker container

.. code-block:: bash

    $ make run
