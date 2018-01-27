django-groucho
=================

A django application providing a simple login page which fakes the existance of users through bad error messages such as *Unknown user* or *Password incorrect*.  This type of deception can be used for logging and alerting by feeding this data to other systems.

Requirements
-----------------
* Python 3.6
* Django 1.11

Getting Started
-----------------
**Build and Install**

At the moment, it's recommended to build and install the application locally with setuptools.  Therefore, run the following commands from the root of this project after cloning.

.. code-block::

    python setup.py sdist
    pip install ./dist/django-groucho-0.1.tar.gz


**Adding to your django application**

Now go ahead and add groucho to your list of applications in settings...

.. code-block:: python

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',

        'groucho', 
    ]
    
and add it to your application's urls...

.. code-block:: python

    from groucho import urls as groucho_urls

    urlpatterns = [
        url(r'^login/', include(groucho_urls)),

    ]

and lastly, run database migrations

.. code-block::

    python manage.py migrate groucho


Templates
----------------
The idea behind groucho's login page is that it can be customized to look like whatever you're wanting.  If the default login page isn't your thing, which it probably isn't, then just overwrite it in your application.

**Login Template**

.. code-block::

    ./groucho/templates/groucho/login.html

Django Admin
----------------
Groucho has been setup to work with django's admin site when it has been configured in your application.  In addition, some reporting can be accessed by going to the **Source Summary** model page.

Configuration
----------------
There are a few things that can be configured through the Configuration model that groucho provides.

**Configuration Model Fields**

*invalid_user_message*

This will be the message displayed by the application when it has decided that the user does not exist within the system.

*invalid_password_message*

This will be the message displayed by the application when the system has decided that the user exists.  They will always have an invalid password.

*new_user_exists_rate*

Since it probably doesn't make sense to have users exist 50% of the time, this lets you decide how often a new user will mimic an existing user.
