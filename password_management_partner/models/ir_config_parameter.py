# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
_logger = logging.getLogger(__name__)

class ChangePasswordEncryptionKeyWizard(models.TransientModel):
    _name = 'ir_config_parameter.change_encryption_key_wizard'
    _description = 'Wizard to change password encryption key'

    old_key = fields.Char('Old key', required=True)
    new_key = fields.Char('New key', required=True)
    new_key_confirm = fields.Char('New key (confirm)', required=True)

    @api.multi
    def save_password(self):
        Param = self.env['ir.config_parameter'].sudo()
        original_key = Param.get_param('password.encryption_key','')
        old_key = self.old_key
        new_key = self.new_key
        new_key_confirm = self.new_key_confirm

        if old_key != original_key:
            raise ValidationError(_("Old key is wrong"))

        if new_key != new_key_confirm:
            raise ValidationError(_("New key and it's confirmation don't match"))

        try:
            for p in self.env['res.partner.password'].search([]):
                p.reencrypt_password(original_key, new_key)
            Param.set_param('password.encryption_key', new_key)
        except Exception as e:
            raise ValidationError(_("Since we could not reencrypt the passwords \
                                    the key was not changed"))
