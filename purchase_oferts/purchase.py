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
from osv import fields, osv
import datetime
import openerp.addons.decimal_precision as dp
class purchase_order_line(osv.osv):
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
            'requisition_id': fields.related('order_id', 'requisition_id', type='many2one', relation='purchase.requisition', string='solicitud de presupuesto', store=True),
            'date_requisition': fields.related('requisition_id', 'date_start', type='date', string='fecha de solicitud'),
            'department_id': fields.related('order_id', 'department_id', type='many2one', relation='hr.department', string='departamento'),
            'date_order': fields.related('order_id', 'date_order', type='date', string='fecha de presupuesto'),
            'notes': fields.related('order_id', 'notes', type='text', string='Observaciones'),
            'fabricante_producto_id': fields.related('product_id', 'fabricante_id', type='many2one', relation='fabricante_producto', string='Fabricante_producto'),
            'fabricante_id': fields.related('fabricante_producto_id', 'fabricante_id', type='many2one', relation='fabricante', string='Fabricante'),
            'fab_ref': fields.related('fabricante_producto_id', 'ref', type='char', size=64, string='ref. de fabricante'),
            'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute=dp.get_precision('Account'), group_operator="sum",
                                            store={
                'purchase.order.line': (_amount_line, ['product_qty','price_unit','taxes_id'], 10),
            }),
            'plazo' : fields.function(_calculate_delivery_time, string='Plazo de entrega',  group_operator="avg",
                                      store = {
                                               'purchase.order.line': (_calculate_delivery_time, ['date_planned','date_order'], 10),
                                               }),
            
            }
    
    
purchase_order_line()
