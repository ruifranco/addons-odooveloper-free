=================
Password Manager (for partners)
=================

Installing the module
==========================

Before installing this module you need to install the following dependency:

* PyCryptodome

You can download the source `here <https://pycryptodome.readthedocs.io>`_.


Setting up the module
==========================

When the module is installed, the encryption key is set to the first 16 characters of the database secret, with all the special characters removed, first.
The database secret can be seen in 'Settings / Technical / Parameters'.

You should change the encryption key before you start using the module. In order to do this, go to 'Settings / Technical / Parameters / Encryption key'.

If you ever forget the key, you can take a look at it, directly in the ir_config_parameter table. You will need access to PostgreSQL for this.


Using the module
==========================

In each contact/partner form, there's a new tab called Passwords. You need to belong to one of two groups in order to gain access to this tab: `Password Management (for partners) - user` or `Password Management (for partners) - manager`.
Manager can associate Odoo users to passwords so that they will be able to see them. Instead, User cannot do this but is able add records and to fully change the records he is associated to.
