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

class stock_move(osv.osv):

    _inherit = "stock.move"

    def _get_company_select(self, cr, uid, context=None):
        res = []
        warehouse_obj = self.pool.get('stock.warehouse')
        all_warehouse_ids = warehouse_obj.search(cr, 1, [])
        for warehouse in warehouse_obj.browse(cr, 1, all_warehouse_ids, context=context):
            res.append((str(warehouse.id), warehouse.name))
        return res


    _columns = {
        'resupply_company_id': fields.selection(_get_company_select, string="Resupply company")
    }

    def check_availability_multicompany(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0])
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.available.multicompany',
            'target': 'new',
            'context': "{'active_model': 'product.product', 'active_ids': [" + str(obj.product_id.id) + "]}"
        }

    def create(self, cr, uid, vals, context=None):
        if vals.get('resupply_company_id', False) and vals.get('picking_type_id', False):
            picking_type = self.pool.get('stock.picking.type').browse(cr, 1, vals['picking_type_id'])
            warehouse = picking_type.warehouse_id
            vals['company_id'] = warehouse.company_id.id
            for route in warehouse.resupply_route_ids:
                if route.supplier_wh_id and  int(vals['resupply_company_id']) == route.supplier_wh_id.company_id.id:
                    vals['route_ids'] = [(6,0,[route.id])]
                    break

        return super(stock_move, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        if isinstance(ids, (int,long)):
            ids = [ids]
        for move in self.browse(cr, uid, ids):
            if vals.get('resupply_company_id') and vals['resupply_company_id'] != move.resupply_company_id:
                picking_type_id = vals.get('picking_type_id', False) and vals['picking_type_id'] or move.picking_type_id.id
                warehouse = self.pool.get('stock.picking.type').browse(cr, 1, picking_type_id).warehouse_id
                vals['company_id'] = warehouse.company_id.id
                for route in warehouse.resupply_route_ids:
                    if route.supplier_wh_id and  int(vals['resupply_company_id']) == route.supplier_wh_id.company_id.id:
                        vals['route_ids'] = [(6,0,[route.id])]
                        break

        return super(stock_move, self).write(cr, uid, ids, vals, context=context)

    def action_done(self, cr, uid, ids, context=None):
        if context is None: context = {}
        res = super(stock_move, self).action_done(cr, uid, ids, context=context)
        procurement_ids = []
        ctx = dict(context)
        for move in self.browse(cr, 1, ids, context=context):
            if move.move_dest_id and move.move_dest_id.state in ('waiting', 'confirmed'):
                ctx['force_company'] = move.company_id.id
                self.action_assign(cr, 1, [move.move_dest_id.id], context=ctx)
            if move.procurement_id:
                procurement_ids.append(move.procurement_id.id)

        self.pool.get('procurement.order').check(cr, uid, procurement_ids, context=context)

        return res
