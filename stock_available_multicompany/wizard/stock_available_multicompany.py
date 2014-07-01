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
from osv import osv, fields
import decimal_precision as dp

class stock_available_multicompany(osv.osv_memory):
    _name = 'stock.available.multicompany'
    _columns = {
        'stock_available_lines': fields.one2many('stock.available.multicompany.lines',
                                                 'wizard_id',
                                                 'Lines')
    }
    def default_get(self, cr, uid, fields, context=None):
        """ init the form's fields """
        if context is None:
            context = {}

        res = {}
        line_ids = []
        if uid:
            user_obj = self.pool.get('res.users').browse(cr, uid, uid)
            cr.execute("select cid from res_company_users_rel where user_id = '" + str(user_obj.id) + "'")
            company_ids = cr.fetchall()
            if company_ids:
                for company in company_ids:
                    if context.get('active_ids', False):
                        product = self.pool.get('product.product').browse(cr, uid, context['active_ids'][0])
                        cr.execute("select id, name from stock_warehouse")
                        warehouse = cr.fetchall()
                        if warehouse:
                            for war in warehouse:
                                line_ids.append({
                                                'qty': self.pool.get('product.product').browse(cr, 1, product.id, context={'warehouse': war[0]}).qty_available,
                                                'warehouse_name': war[1]
                                             })

        res.update({'stock_available_lines': line_ids})

        return res
stock_available_multicompany()

class stock_available_multicompany_lines(osv.osv_memory):
    _name = 'stock.available.multicompany.lines'
    _columns = {
        'wizard_id': fields.many2one('stock.available.multicompany',
                                                    'Stock available parent'),
        'warehouse_id': fields.many2one('stock.warehouse',
                                        'Warehouse'),
        'qty': fields.float('Qty available',
                            digits_compute=dp.get_precision('Product UoM')),
        'warehouse_name': fields.char('Warehouse', size=255)
    }

stock_available_multicompany_lines()
