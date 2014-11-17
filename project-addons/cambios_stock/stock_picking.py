# -*- coding: utf-8 -*-
###############################################################################
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
###############################################################################

from openerp.osv import osv, fields

class stock_picking(osv.osv):

    _inherit = "stock.picking"

    def _get_company_id(self, cr, uid, context=None):
        if context.get('default_picking_type_id', False):
            warehouse = self.pool.get('stock.picking.type').browse(cr, 1, context['default_picking_type_id']).warehouse_id
            return warehouse.company_id.id
        return self.pool.get('res.company')._company_default_get(cr, uid, 'stock.picking', context=context)

    _defaults = {
        'company_id': _get_company_id
    }

    def action_assign(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for pick in self.browse(cr, uid, ids, context=context):
            context['force_company'] = pick.company_id.id
            super(stock_picking, self).action_assign(cr, uid, [pick.id], context=context)
        return True
