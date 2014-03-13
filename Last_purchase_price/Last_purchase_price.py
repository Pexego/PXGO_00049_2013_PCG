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
import openerp.addons.decimal_precision as dp

class Last_purchase_price(osv.osv):

    def _ultimo_precio(self, cr, uid, ids, name, arg, context=None):
        if not context:
            context = {}
        res = {}
        purchase_line_obj = self.pool.get('purchase.order.line')
        for prod_id in self.browse(cr, uid, ids, context=context):
            line_id = purchase_line_obj.search(cr, uid,
                                               [('product_id','=',prod_id.id),
                                                ('state', 'in', ['done',
                                                                 'confirmed']),
                                                ('invoice_lines', '!=', False)
                                               ],
                                               limit=1,
                                               order='date_planned desc, id desc',
                                               context=context)
            price_unit = 0.0
            if line_id:
                line = purchase_line_obj.browse(cr, uid, line_id[0], context)
                uom = line.invoice_lines[0].uos_id
                price_unit = line.invoice_lines[0].price_unit * \
                             (1-(line.invoice_lines[0].discount/100))
                if uom.id != prod_id.uom_id.id:
                    price_unit = (price_unit * uom.factor) / \
                                 prod_id.uom_id.factor

            res[prod_id.id] = price_unit

        return res

    _inherit = 'product.product'
    _columns = {
            'last_purchase_price': fields.function(_ultimo_precio, method=True, type='float',digits_compute= dp.get_precision('Product Price'), string='Last purchase price', store=False),
                    }
