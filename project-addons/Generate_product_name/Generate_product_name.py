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
from openerp import tools


class Generate_product_name(orm.Model):
    _inherit = 'product.template'

    def generate_name(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        products = self.pool.get('product.template').browse(cr, uid, ids, context)
        for product in products:
            nombre = product.name
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
                    nombre += u" " + (isinstance(product[atributo],type(product)) and product[atributo].name or tools.ustr(product[atributo]))

            if not nombres_atributos and product.attribute_ids:
                for attribute in product.attribute_ids:
                    nombre += (u" " + attribute.value)

            self.pool.get('product.template').write(cr, uid, ids, {'name':nombre.strip()},context)
        return
