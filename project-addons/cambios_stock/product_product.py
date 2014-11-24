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
#############################################################################

from openerp.osv import orm, fields

class product_template(orm.Model):

    _inherit = "product.template"

    _columns = {
        'fixed_location_id': fields.many2one('stock.location', 'Stock location', required=True, domain=[('usage', '=', 'internal')])
    }

    _defaults = {
        'fixed_location_id': lambda self, cr, uid, context: self.pool.get('stock.warehouse').browse(cr, uid, self.pool.get('stock.warehouse').search(cr, uid, [])[0]).lot_stock_id.id
    }


class product_putaway_strategy(orm.Model):

    _inherit = "product.putaway"

    def _get_putaway_options(self, cr, uid, context=None):
        res = [('fixed', 'Fixed Location'), ('product_location', 'Product location')]

        return res

    _columns = {
        'method': fields.selection(_get_putaway_options, "Method", required=True)
    }

    def putaway_apply(self, cr, uid, putaway_strat, product, context=None):
        if putaway_strat.method == 'product_location':
            return product.fixed_location_id.id
        else:
            return super(product_putaway_strategy, self).putaway_apply(cr, uid, putaway_strat, product, context=context)
