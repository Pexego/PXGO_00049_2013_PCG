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

class Producto(osv.osv):
    _inherit = 'product.product'
    def stock_multicompany(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if not ids:
            return []
        company_ids = self.pool.get("res.company").search(cr, uid, [], offset=0, limit=None, order=None, context=context, count=False)
        if company_ids is None:
            company_ids = []
        total = []
        for company_id in company_ids:
            warehouse_id = self.pool.get("stock.warehouse").search(cr, uid, [('company_id', '=', company_id)], offset=0, limit=None, order=None, context=context, count=False)
            if warehouse_id:
                warehouse = self.pool.get("stock.warehouse").browse(cr, uid, warehouse_id[0], context)
                location_id = warehouse.lot_stock_id.id
                total_movimientos_desde = 0
                total_movimientos_a = 0
                movimientos_a_almacen_ids = self.pool.get("stock.move").search(cr, uid, [('product_id', 'in', ids), ('company_id', '=', company_id), ('location_dest_id', '=', location_id)], offset=0, limit=None, order=None, context=context, count=False)
                for movimiento_a in self.pool.get("stock.move").browse(cr, uid, movimientos_a_almacen_ids, context):
                    total_movimientos_a += movimiento_a.product_qty * movimiento_a.product_uom.factor_inv
        
                movimientos_desde_almacen_ids = self.pool.get("stock.move").search(cr, uid, [('product_id', 'in', ids), ('company_id', '=', company_id), ('location_id', '=', location_id)], offset=0, limit=None, order=None, context=context, count=False)
                for movimiento_desde in self.pool.get("stock.move").browse(cr, uid, movimientos_desde_almacen_ids, context):
                    total_movimientos_desde += movimiento_desde.product_qty * movimiento_desde.product_uom.factor_inv
                stock_actual_company = total_movimientos_a - total_movimientos_desde
                total.append((company_id, stock_actual_company))
        lineas = []
        wizard_id = self.pool.get("stock.multicompany.wizard").create(cr, uid, {}, context=context)
        for tupla in total:
            lineas.append(self.pool.get("stock.multicompany.wizard.lineas").create(cr, uid, {'cantidad':tupla[1], 'wizard_id':wizard_id, 'company_id':tupla[0]}, context))
            
        return {
            'name': ("Stock multicompany"),
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'stock.multicompany.wizard',
            'res_id':wizard_id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
            'context': context
        }
        
Producto()
