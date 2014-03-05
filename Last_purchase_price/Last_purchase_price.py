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
        #import pdb;pdb.set_trace()
        if not context:
            context = {}
        res = {}
        for prod_id in ids:
            res[prod_id] = 0
            line_id = self.pool.get('purchase.order.line').search(cr, uid, [('product_id','=',prod_id)], offset=0, limit=1, order='date_planned DESC', context=context, count=False)
            if line_id:               
                line = self.pool.get('purchase.order.line').browse(cr, uid, line_id[0], context)
                for invoice_line in line.invoice_lines:
                    uom = invoice_line.uos_id
                    res[prod_id]=(invoice_line.price_unit*uom.factor)*(1-(invoice_line.discount/100))
                        
                        
                    
        return res
    _inherit = 'product.product'
    _columns = {
            'last_purchase_price': fields.function(_ultimo_precio, method=True, type='float',digits_compute= dp.get_precision('Product Price'), string='Ultimo precio de compra', store=False), 
                    }