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

from openerp.osv import orm, fields

class history_product_code(orm.Model):
    _inherit = 'product.product'

    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}
        if vals.get('default_code', False):
            for id in ids:
                product = self.browse(cr, uid, id, context)
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

class historial_product_code(orm.Model):
    _name = 'historial.product.code'
    _columns = {
            'code':fields.char('Codigo', size=64, required=True, readonly=True),
            'product_id':fields.many2one('product.product', 'Product', required=False),
    }

class product_template(orm.Model):

    _inherit = "product.template"

    def action_view_history_code(self, cr, uid, ids, context=None):
        products = self._get_products(cr, uid, ids, context=context)
        result = self._get_act_window_dict(cr, uid, 'history_product_code.act_product_code_history_open', context=context)
        if len(ids) == 1 and len(products) == 1:
            ctx = "{'default_product_id': %s, 'search_default_product_id': %s}" \
                  % (products[0], products[0])
            result['context'] = ctx
        else:
            result['domain'] = "[('product_id','in',[" + ','.join(map(str, products)) + "])]"
        return result

