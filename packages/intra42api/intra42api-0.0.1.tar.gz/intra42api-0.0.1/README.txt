Intra42Api
=============

|Banner|

Intra42Api is an API wrapper.
Supports searches for Users, Campuses and Projects.

|Github| |License| |Package|

Installation
------------

**NOTE**: Python 3.6 or higher is required.

.. code:: python

   # Windows
   py -3.6 -m pip install intra42api

   # Linux
   python3.6 -m pip install intra42api

Example
-------

.. code:: python

	import intra42api

	intra = intra42api.Intra42()


	intra.setToken('MY_AWESOME_UID', 'MY_AWESOME_SECRET')


	user = intra.getUser('ID_OR_LOGIN')

	print(f"""
		Login: {user['login']}
		Email: {user['email']}
		Full Name: {user['displayname']}
		Correction Points: {user['correction_point']}
		url: {user['url']}
	""")

.. |Banner| image:: https://raw.githubusercontent.com/NorsHiden/Intra42Api-wrapper_module/master/apiwrapper.png
   :target: https://github.com/NorsHiden/Intra42Api-wrapper_module
.. |Github| image:: https://img.shields.io/github/forks/NorsHiden/Intra42Api-wrapper_module?style=plastic
   :target: https://github.com/NorsHiden/Intra42Api-wrapper_module
.. |License| image:: https://img.shields.io/github/license/NorsHiden/Intra42Api-wrapper_module
   :target: https://github.com/NorsHiden/Intra42Api-wrapper_module/blob/master/LICENCE.txt
.. |Package| image:: https://img.shields.io/pypi/pyversions/31?style=flat-square
   :target: https://pypi.org/project/intra42api