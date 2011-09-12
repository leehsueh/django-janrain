##############
leehsueh/django-janrain
##############

Forked from spuriousdata/django-janrain.

Janrain integration into Django using built-in django.contrib.auth package. On first login, it tries to associate with an existing django User object by first and last name and verified email. If one does not exist, a new User object is created and associated with the profile identifier provided by Janrain. Mappings from Janrain profile identifiers to django User objects are stored using the JanrainUser model.

============
Installation
============
Add the janrain app to your project ``myproject``

Add a url entry in your project's top level ``urls.py``::

	urlpatterns += patterns('',
		(r'^janrain/', include('myproject.janrain.urls')),
	)

Open janrain/urls.py and change ``myproject`` to your project name.

Open janrain/backends.py and change ``myproject`` (in the JanrainUser import statement) to your project name.

Add ``janrain`` to your ``INSTALLED_APPS``::

	INSTALLED_APPS = (
		'django.contrib.admin',
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'myproject.janrain',
	)

Add ``myproject.janrain.backends.JanrainBackend`` to ``AUTHENTICATION_BACKENDS``::

	# put janrain.backends.JanrainBackend first
	AUTHENTICATION_BACKENDS = (
		'myproject.janrain.backends.JanrainBackend',
		'django.contrib.auth.backends.ModelBackend',
	)

Add your janrain api key to ``settings``::

	JANRAIN_API_KEY = "0123456789abcdef0123456789abcdef0123456789abcdef"

Run manage.py syncdb to create the database table for JanrainUser.

=====
Usage
=====

Configure your ``token_url`` in janrain to be http://yoursite.com/janrain/login/

Modify the janrain/templates/janrain_login.html template to include your janrain widget (replace instances of ``__REPLACE WITH YOUR JANRAIN APP__`` with your janrain app url name). Optionally append the ``next`` query parameter in the token URL to redirect after login. (Alternatively, modify your existing login template to include the janrain widget, following the instructions from the Janrain widget setup wizard. Note that the django-janrain login view will pass Django's built-in authentication form as a ``form`` context variable, in addition to the ``next`` query parameter).

Create a button to hit ``/janrain/logout/`` to log out.