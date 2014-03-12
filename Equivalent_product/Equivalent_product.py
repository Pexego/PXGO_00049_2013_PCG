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
    
    def _save_equivalent_product(self, cr, uid, ids, field_name, field_value, args=None, context=None):
        product_obj = self.pool.get('product.product')
        if type(ids) is not list:
            ids = [ids]
        for id in ids:
            write_values = (field_value[ids.index(id)][0],field_value[ids.index(id)][1])
            product = product_obj.browse(cr, uid, id, context)
            final_field_value = [equivalent.id for equivalent in product.equivalent_product_ids]
            #add
            for equivalent_in in field_value[ids.index(id)][2]:
                if equivalent_in not in [equivalent.id for equivalent in product.equivalent_product_function]:
                    final_field_value+=[equivalent_in]
            product_obj.write(cr, uid, id, {'equivalent_product_ids': [write_values+(final_field_value,)]}, context)
            product = product_obj.browse(cr, uid, id, context)
            #delete
            equivalent_product_id = [equivalent.id for equivalent in product.equivalent_product_ids]
            for equivalent_f in [equivalent.id for equivalent in product.equivalent_product_function]:
                if equivalent_f not in field_value[ids.index(id)][2]:
                    if equivalent_f in equivalent_product_id:
                        equivalent_product_id.pop(equivalent_product_id.index(equivalent_f))
                    else:
                        product_foreign = product_obj.browse(cr, uid, equivalent_f, context)
                        product_foreign_equivalent_ids = [equivalent.id for equivalent in product_foreign.equivalent_product_ids]
                        product_foreign_equivalent_ids.pop(product_foreign_equivalent_ids.index(id))
                        product_obj.write(cr, uid, product_foreign.id,{\
                        'equivalent_product_ids':[write_values+(product_foreign_equivalent_ids,)]}, context)
            product_obj.write(cr, uid, id,{'equivalent_product_ids': [write_values+(equivalent_product_id,)]}, context)

    
    def _get_equivalent_products(self, cr, uid, ids, field_name, args=None, context=None):
        if context is None:
            context = {}
        product_obj = self.pool.get('product.product')
        result = {}
        for id in ids:
            #productos equivalentes
            product = product_obj.browse(cr, uid, id, context)
            result[id] = [equivalent.id for equivalent in product.equivalent_product_ids]
            #busqueda de productos a los que es equivalente
            equivalent_ids = product_obj.search(cr, uid, \
                            [('equivalent_product_ids','in',[id])], context=context)
            result[id]+=equivalent_ids
        return result
    
    _columns = {
            'equivalent_product_ids':fields.many2many('product.product', \
                                    'equivalent_products', 'product_id', \
                                    'equivalent_id', 'Productos equivalentes'),
            'equivalent_product_function': fields.function(_get_equivalent_products,\
                                      type='many2many',relation='product.product'\
                                      , string='Productos equivalentes',\
                                      fnct_inv=_save_equivalent_product),
            }         
Producto()