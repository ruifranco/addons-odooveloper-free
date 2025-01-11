# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    password_manager_key = fields.Char('Password key',
                                    config_parameter='base.password_manager_key')
