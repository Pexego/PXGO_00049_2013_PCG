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
from openerp import netsvc
class generate_purchases_wizard(orm.TransientModel):
    _name = 'generate.purchases.wizard'

    def generar(self, cr, uid, ids, context=None):
        wf_service = netsvc.LocalService("workflow")
        purchase_line_obj = self.pool.get('purchase.order.line')
        purchase_order_obj = self.pool.get('purchase.order')
        requisition_obj = self.pool.get('purchase.requisition')
        if not context:
            context = {}
        if not ids:
            return False
        wiz = self.browse(cr, uid, ids, context)
        solicitud = None
        proveedores = []
        lineas_compra_ids = []
        compras_a_borrar = []
        requisition_ids = []

        for linea in wiz[0].lineas_ids:
            if not solicitud:
                solicitud = linea.order_id.requisition_id
            else:
                if solicitud == linea.order_id.requisition_id:
                    raise orm.except_orm('Error', 'solo se puede seleccionar lineas de diferentes solicitudes')
            proveedores.append(linea.partner_id)
            lineas_compra_ids.append(linea.id)


        proveedores = list(set(proveedores))
        for proveedor in proveedores:
            lineas_proveedor_id = purchase_line_obj.search(cr, uid, [('id', 'in', lineas_compra_ids), ('partner_id', '=', proveedor.id)], offset=0, limit=None, order=None, context=context, count=False)
            lineas_proveedor = purchase_line_obj.browse(cr, uid, lineas_proveedor_id, context)
            for linea in lineas_proveedor:
                compras_a_borrar.append(linea.order_id.id)
                requisition_ids.append(linea.order_id.requisition_id.id)
            compra_antigua = lineas_proveedor[0].order_id
            nueva_compra_id= purchase_order_obj.copy(cr, uid, compra_antigua.id ,{'order_line':None}, context)
            purchase_line_obj.write(cr, uid, lineas_proveedor_id, {'order_id':nueva_compra_id}, context)
            wf_service.trg_validate(uid, 'purchase.order', nueva_compra_id, 'purchase_confirm', cr)
        for compra in compras_a_borrar:
            wf_service.trg_validate(uid, 'purchase.order', nueva_compra_id, 'act_cancel', cr)
        purchase_order_obj.unlink(cr, uid, compras_a_borrar, context)
        compras_a_cancelar = purchase_order_obj.search(cr, uid, [('requisition_id', 'in', requisition_ids), ('state', '=', 'draft')], offset=0, limit=None, order=None, context=context, count=False)
        lineas_a_cancelar = purchase_line_obj.search(cr, uid, [('order_id','in',compras_a_cancelar)], offset=0, limit=None, order=None, context=context, count=False)
        purchase_line_obj.write(cr, uid, lineas_a_cancelar,{'state':'cancel'}, context)
        requisition_obj.tender_done(cr, uid, requisition_ids, context)
        for compra in compras_a_cancelar:
            wf_service.trg_validate(uid, 'purchase.order', compra, 'purchase_cancel', cr)
        return True

    def _get_lineas(self, cr , uid , context=None):
        if not context or not context['active_ids']:
            return []
        return context['active_ids']

    _columns = {
            'lineas_ids':fields.many2many('purchase.order.line', 'purchase_order_generate_purchases_rel', 'line_id', 'wizard_id', 'Lines'),
                    }

    _defaults = {
        'lineas_ids': _get_lineas,
    }
generate_purchases_wizard()


