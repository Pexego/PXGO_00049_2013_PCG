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
class history_product_code(osv.osv):
    _inherit = 'product.product'
    _columns = {
        'history_code_ids': fields.one2many('historial.product.code','product_id','Code history')
    }
    
    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}
        if 'default_code' in vals:
            for id in ids:
                product = self.pool.get("product.product").browse(cr, uid, id, context)
                if product.default_code:
                    self.pool.get("historial.product.code").create(cr, uid, {'product_id':product.id, 'code':product.default_code}, context)
        return super(history_product_code,self).write(cr, uid, ids, vals, context)
    
    def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        vals = super(history_product_code, self).name_search(cr, user, name=name, args=args, operator=operator, context=context, limit=limit)
        if not vals:
            vals = []
        historial_ids = self.pool.get("historial.product.code").search(cr, user, [('code', '=', name)], offset=0, limit=limit-len(vals), order=None, context=context, count=False)
        if not historial_ids:
            historial_ids = self.pool.get("historial.product.code").search(cr, user, [('code', operator, name)], offset=0, limit=limit-len(vals), order=None, context=context, count=False)
            if not historial_ids:
                return vals
        historials = self.pool.get("historial.product.code").browse(cr, user, historial_ids, context)
        product_ids = []
        for historial in historials:
            product_ids.append(historial.product_id.id)
        product_ids = self.search(cr, user, [('id', 'in', product_ids)] + args, offset=0, limit=limit-len(vals), order=None, context=context, count=False)
        results = self.name_get(cr, user, product_ids, context)
        for result in results:
            if not result in vals:
                vals.append(result)
        return vals
history_product_code()
    

class historial_product_code(osv.osv):
    _name = 'historial.product.code'
    _columns = {
            'code':fields.char('Codigo', size=64, required=True, readonly=True),
            'product_id':fields.many2one('product.product', 'Product', required=False),
                    }
historial_product_code()
