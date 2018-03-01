# -*- coding: utf-8 -*-

from openerp import models,fields,api
from openerp.tools.translate import _



class res_company(models.Model):
    _inherit = 'res.company'

    is_glpi_host   = fields.Char('Host GLPI')
    is_glpi_user   = fields.Char('User GLPI')
    is_glpi_passwd = fields.Char('Mot de passe GLPI')
    is_glpi_db     = fields.Char('Base GLPI')




