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

class fabricante_producto(osv.osv):
    _name = 'fabricante_producto'
    _columns = {
                'fabricante_id':fields.many2one('fabricante', 'Fabricante'),
                'ref':fields.char('Referencia', size=64, required=False, readonly=False),
                }
    def name_get(self, cr, uid, ids, context=None):
        res = []
        if context is None:
            context = {}
        if not ids:
            return []
        for fabricante_producto in self.browse(cr, uid, ids, context):
            res.append((fabricante_producto.id, str(fabricante_producto.fabricante_id.Nombre)+", "+str(fabricante_producto.ref)))
        return res
fabricante_producto()

class Fabricante(osv.osv):
    _name = 'fabricante'
    _columns = {
            'Nombre': fields.text('Nombre'),
            'product_ids':fields.one2many('fabricante_producto', 'fabricante_id', 'Productos', required=False),
                                }
    def name_get(self, cr, uid, ids, context=None):
        res = []
        if context is None:
            context = {}
        if not ids:
            return []
        for fabricante in self.browse(cr, uid, ids, context):
            res.append((fabricante.id, fabricante.Nombre))
        return res
Fabricante()

class Producto(osv.osv):
    _inherit = 'product.product'
    _columns = {
            'fabricante_id':fields.many2one('fabricante_producto', 'Fabricante', required=False),
            }
    _sql_constraints = [('codigo_unico', 'unique (default_code)', 'El codigo de producto debe ser unico!'), ]

Producto()
