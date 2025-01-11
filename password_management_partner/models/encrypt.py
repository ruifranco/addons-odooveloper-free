#! -*- encoding: utf-8 -*-
import logging
import base64
from odoo import models, fields, api, _
try:
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
except ImportError as e:
    pass
_logger = logging.getLogger(__name__)

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class PassWordManagementEncrypt(models.Model):
    _name = 'password.management.encrypt'
    _description = 'Tools for encrypting passwords'

    def set_default_key(self):
        Param = self.env['ir.config_parameter'].sudo()
        key = Param.get_param('password.encryption_key','')
        if not key:
            key = Param.get_param('database.secret').replace('-','')[:BS]
            try:
                Param.create({
                            'key': 'password.encryption_key',
                            'value': key
                            })
            except Exception as e:
                _logger.info('Password Management (param creation ERROR): %s' % e)
        return key

    def _get_key(self):
        key = self.set_default_key()
        try:
            if self._context.get('force_key'):
                key = self._context['force_key']
            key += (BS - len(key)) * '0'
            return bytes(key, 'utf-8')
        except Exception as e:
            _logger.info(e)
            return ''

    def encrypt(self, raw):
        try:
            key = self._get_key()
            raw = pad(raw)
            iv = get_random_bytes(BS)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            raw = base64.b64encode(iv + cipher.encrypt(bytes(raw, 'utf-8')))
        except Exception as e:
            _logger.info('Password Management (Encrypt ERROR): %s' % e)
            pass
        return raw

    def decrypt(self, enc):
        try:
            key = self._get_key()
            enc = base64.b64decode(enc)
            iv = enc[:BS]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            enc = unpad(cipher.decrypt(enc[BS:]))
        except Exception as e:
            _logger.info('Password Management (Decrypt ERROR): %s' % e)
            enc = 'DECRYPT ERROR'
            pass
        return enc
