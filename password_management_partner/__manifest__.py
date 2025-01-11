#! -*- encoding: utf-8 -*-
# Copyright 2019 Odooveloper (<http://www.odooveloper.com>)
{
    'name': 'Password Manager (for partners)',
    'version': '1.0',
    'license': 'OPL-1',
    'price': '20.00',
    'currency': 'EUR',
    'category': 'Extra Tools',
    'summary': 'Save passwords in a safe way',
    'description': """
Password Management (for partners) allows you to keep all information concerning passwords inside a contact's form,
thus ending the need to use third party programs for such purpose.

All sensitive data is saved in an encrypted way.

Two profiles are available: 'user' and 'manager'.

'Users' are able to see/edit/delete the passwords they've been associated to.
The 'manager' profile has all permissions on any existing password record as well as the
ability to add users to a password.

The manager can change the encryption key.
By default, the encryption key is the first 16 characters of the 'database secret' with all its '-' removed.
YOU SHOULD CHANGE THE ENCRYPTION KEY RIGHT AFTER INSTALLING THIS MODULE!
If you totally loose the encryption key you can find it in the ir_config_parameter table.

\n\n
WARNING!
Before installing this module, make sure you have Python's PyCryptodome library installed and its AES feature working properly.
PyCryptodome can be obtained here (for free): https://pycryptodome.readthedocs.io
    """,
    'author': 'Odooveloper',
    'website': 'http://www.odooveloper.com',
    'support': 'info@odooveloper.com',
    'depends': ['mail', 'contacts'],
    'data': [
            'security/security_data.xml',
            'security/ir.model.access.csv',
            'views/res_partner_view.xml',
            'views/ir_config_parameter_view.xml',
            ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
