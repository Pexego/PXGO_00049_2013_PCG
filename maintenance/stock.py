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
from osv import osv, fields

class stock(osv.osv):
    def _work_done(self, cr, uid, ids, name, arg=None, context=None):
        res = {}
        for stock_move_id in ids:
            stock_move = self.pool.get('stock.move').browse(cr, uid, stock_move_id, context)
            if stock_move.work_order_id:
                work_order_state = stock_move.work_order_id.state
                if work_order_state == 'done':
                    res[stock_move_id] = True
            res[stock_move_id] = False
        return res    
    
    _inherit = 'stock.move' 
    _columns = {
            'element_id':fields.many2one('maintenance.element', 'Equipo', required=False),
            'work_order_id':fields.many2one('work.order', 'orden de trabajo', required=False),
            'work_done': fields.function(_work_done, method=True, type='boolean', string='orden finalizada', store=False),
                    }
stock()

class stock_picking(osv.osv):   
    
    _inherit = 'stock.picking'
    _columns = {
            'work_order_id':fields.many2one('work.order', 'orden de trabajo', required=False),
                    }
stock_picking()

class stock_picking_out(osv.osv):
    def _work_done(self, cr, uid, ids, name, arg=None, context=None):
        res = {}
        for stock_picking_out_id in ids:
            stock_picking_out = self.pool.get('stock.picking.out').browse(cr, uid, stock_picking_out_id, context)
            if stock_picking_out.work_order_id:
                work_order_state = stock_picking_out.work_order_id.state
                if work_order_state == 'done':
                    res[stock_picking_out_id] = True
            res[stock_picking_out_id] = False
        return res    
    
    _inherit = 'stock.picking.out'
    _columns = {
            'work_order_id':fields.many2one('work.order', 'orden de trabajo', required=True),
            'work_done': fields.function(_work_done, method=True, type='boolean', string='orden finalizada', store=False),
                    }
stock_picking_out()
    
