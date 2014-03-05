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

class Generate_product_name(osv.osv):
    _inherit = 'product.product'

    def generate_name(self, cr, uid, ids, context=None):
        nombre = ""
        if not context:
            context = {}
        products = self.pool.get('product.product').browse(cr, uid, ids, context)
        for product in products:
            nombres_atributos = []
            categorias=[product.categ_id]
            for cat in product.categ_ids:
                categorias.append(cat)
            for categoria in categorias:
                for att_group in categoria.attribute_group_ids:
                    for atributo in att_group.attribute_ids:
                        nombres_atributos.append(atributo.name)
            for atributo in nombres_atributos:
                if product[atributo]:
                    nombre += str(product[atributo])+" "
            if not nombre:
                nombre = product.name
            self.pool.get('product.product').write(cr, uid, ids, {'name':nombre},context)
        return