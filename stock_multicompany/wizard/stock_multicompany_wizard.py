# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from osv import fields, osv

class stock_multicompany_wizard(osv.osv_memory):
    _name = 'stock.multicompany.wizard'
    _columns = {
            'lineas_ids':fields.one2many('stock.multicompany.wizard.lineas', 'wizard_id', 'Stock',required=False, readonly=True),
                    }
    
    
stock_multicompany_wizard()

class stock_multicompany_wizard_lineas(osv.osv_memory):
    _name = 'stock.multicompany.wizard.lineas'
    _columns = {
            'cantidad': fields.integer('Quantity'),
            'wizard_id':fields.many2one('stock.multicompany.wizard', 'wizard', required=False),
            'company_id':fields.many2one('res.company', 'Company', required=False), 
                }
