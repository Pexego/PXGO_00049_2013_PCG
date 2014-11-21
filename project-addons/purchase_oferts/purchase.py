# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2004-2014 Pexego Sistemas Informáticos All Rights Reserved
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

from openerp.osv import fields, orm
import datetime
import openerp.addons.decimal_precision as dp

class purchase_order_line(orm.Model):


    def _amount_line(self, cr, uid, ids, prop, arg=None, context=None):
        return super(purchase_order_line, self)._amount_line(cr, uid, ids, prop, arg, context)

    _inherit = 'purchase.order.line'

    def _calculate_delivery_time(self, cr, uid, ids, prop, arg=None, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            date_planned = datetime.datetime.strptime(line.date_planned, '%Y-%m-%d').date()
            date_order = datetime.datetime.strptime(line.date_order, '%Y-%m-%d').date()
            dif = date_planned - date_order
            res[line.id] = dif.days
        return res

    _columns = {
            'requisition_id': fields.related('order_id', 'requisition_id', type='many2one', relation='purchase.requisition', string='Solicitud de presupuesto', store=True),
            'date_requisition': fields.related('requisition_id', 'ordering_date', type='date', string='Fecha de solicitud'),
            'department_id': fields.related('order_id', 'department_id', type='many2one', relation='hr.department', string='Departamento'),
            'date_order': fields.related('order_id', 'date_order', type='date', string='Fecha de presupuesto'),
            'notes': fields.related('order_id', 'notes', type='text', string='Observaciones'),
            'fabricante_id': fields.related('product_id', 'manufacturer', type='many2one', relation='res.partner', string='Fabricante'),
            'fab_ref': fields.related('product_id', 'manufacturer_pref', type='char', size=64, string='Ref. de fabricante'),
            'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute=dp.get_precision('Account'), group_operator="sum", type="float",
                                            store={
                'purchase.order.line': (lambda self, cr, uid, ids, c={}: ids, ['product_qty','price_unit','taxes_id'], 10),
            }),
            'plazo' : fields.function(_calculate_delivery_time, string='Plazo de entrega',  group_operator="avg", type="float", digits=(16,2),
                                      store = {
                                               'purchase.order.line': (lambda self, cr, uid, ids, c={}: ids, ['date_planned','date_order'], 10),
                                               }),

            }


purchase_order_line()
