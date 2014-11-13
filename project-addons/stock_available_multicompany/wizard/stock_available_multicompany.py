# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2004-2012 Pexego Sistemas Informáticos All Rights Reserved
#    $Marta Vázquez Rodríguez$ <marta@pexego.es>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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
from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp

class stock_available_multicompany(osv.osv_memory):
    _name = 'stock.available.multicompany'
    _columns = {
        'stock_available_lines': fields.one2many('stock.available.multicompany.lines',
                                                 'wizard_id',
                                                 'Lines', readonly=True)
    }
    def default_get(self, cr, uid, fields, context=None):
        """ init the form's fields """
        if context is None:
            context = {}

        res = {}
        line_ids = []
        warehouse_obj = self.pool.get('stock.warehouse')
        if uid:
            user_obj = self.pool.get('res.users').browse(cr, uid, uid)
            if user_obj.company_ids:
                for company in user_obj.company_ids:
                    if context.get('active_ids', False):
                        product = self.pool.get(context['active_model']).browse(cr, uid, context['active_ids'][0])
                        warehouse_ids = warehouse_obj.search(cr, uid, [('company_id', '=', company.id)])
                        if warehouse_ids:
                            for war in warehouse_obj.browse(cr, uid, warehouse_ids):
                                line_ids.append({
                                                'qty': self.pool.get(context['active_model']).browse(cr, 1, product.id, context={'warehouse': war.id, 'force_company': company.id}).qty_available,
                                                'warehouse_name': war.name,
                                             })

        res.update({'stock_available_lines': line_ids})

        return res
stock_available_multicompany()

class stock_available_multicompany_lines(osv.osv_memory):
    _name = 'stock.available.multicompany.lines'
    _columns = {
        'wizard_id': fields.many2one('stock.available.multicompany',
                                                    'Stock available parent'),
        'qty': fields.float('Qty available',
                            digits_compute=dp.get_precision('Product UoM')),
        'warehouse_name': fields.char('Warehouse', size=255)
    }

stock_available_multicompany_lines()
