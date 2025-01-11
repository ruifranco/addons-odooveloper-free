#! -*- encoding: utf-8 -*-
import logging
from odoo import models, fields, api, _
_logger = logging.getLogger(__name__)

class ResPartnerPassword(models.Model):
    _name = 'res.partner.password'
    _description = 'Partner passwords'

    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    name = fields.Char('Name', required=True)
    url = fields.Char('Address')
    field1 = fields.Char('Field A')
    field2 = fields.Char('Field B')
    field3 = fields.Char('Field C')

    @api.multi
    def _decrypt_fields(self):
        Encrypt = self.env['password.management.encrypt']
        for s in self:
            try:
                if s.field1:
                    s.field1_show = Encrypt.decrypt(s.field1)
                if s.field2:
                    s.field2_show = Encrypt.decrypt(s.field2)
                if s.field3:
                    s.field3_show = Encrypt.decrypt(s.field3)
            except Exception as e:
                _logger.info('Password Management (Decrypt ERROR): %s' % e)
                pass

    #the fiels that get shown
    field1_show = fields.Char('Field A',
                              help="Typically, this should be used for 'username'",
                              compute='_decrypt_fields')
    field2_show = fields.Char('Field B',
                              help="Typically, this should be used for 'password'",
                              compute='_decrypt_fields')
    field3_show = fields.Char('Field C',
                              help="Typically, this should be used for 'domain'",
                              compute='_decrypt_fields')

    note = fields.Text('Note')
    user_ids = fields.Many2many(comodel_name='res.users',
                                relation='res_partner_passwords_users_rel',
                                column1='password_id',
                                column2='user_id',
                                string='Allowed users',
                                help="Blank means everyone will be able \
                                        to see this.")

    @api.model
    def create(self, vals):
        if not 'user_ids' in vals:
            vals['user_ids'] = []
        #user gets added to the record permissions
        vals['user_ids'].append((4, self._uid))
        Encrypt = self.env['password.management.encrypt']
        for x in range(1, 4):
            field = 'field%s_show' % x
            if vals.get(field):
                vals[field.replace('_show', '')] = Encrypt.encrypt(vals[field])
        return super(ResPartnerPassword, self).create(vals)

    @api.multi
    def write(self, vals):
        self.ensure_one()
        Encrypt = self.env['password.management.encrypt']
        for x in range(1, 4):
            field = 'field%s_show' % x
            if field in vals:
                vals[field.replace('_show', '')] = Encrypt.encrypt(vals[field])
        return super(ResPartnerPassword, self).write(vals)

    @api.multi
    def reencrypt_password(self, original_password=False, new_password=False):
        self.ensure_one()
        Encrypt = self.env['password.management.encrypt']
        if original_password and new_password:
            self.with_context(force_key=original_password)._decrypt_fields()
            for x in range(1, 4):
                field = 'field%s_show' % x
                aux_val = eval('self.' + field)
                if aux_val:
                    self.write({field.replace('_show', ''):\
                                Encrypt\
                                    .with_context(force_key=new_password)\
                                    .encrypt(aux_val)
                                })


class ResPartner(models.Model):
    _inherit = 'res.partner'

    password_ids = fields.One2many('res.partner.password', 'partner_id',
                                    string='Passwords')
