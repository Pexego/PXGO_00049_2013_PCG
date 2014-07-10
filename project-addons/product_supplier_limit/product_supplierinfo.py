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
from osv import osv, fields

class product_supplierinfo(osv.osv):
    _inherit = 'product.supplierinfo'
    _columns = {
            'principal_supplier':fields.boolean('proveedor principal', required=False),
                    }
    _defaults = {  
        'principal_supplier': False,
        }
    
    def write(self, cr, uid, ids, vals, context=None):
        if not context:
            context = {}
        if vals['principal_supplier']:
            if len(ids) > 2:
                raise osv.except_osv('Error', 'solo puede haber 3 proveedores principales')
            product_ids = self.pool.get('product.product').search(cr, uid, [('seller_ids', 'in', ids)], offset=0, limit=None, order=None, context=context, count=False)
            principal_ids = self.pool.get('product.supplierinfo').search(cr, uid, [('principal_supplier', '=', 'True'), ('product_id', 'in', product_ids)], offset=0, limit=None, order=None, context=context, count=False)
            if len(principal_ids) > 2 or (len(principal_ids) + len(ids)) > 3:
                raise osv.except_osv('Error', 'solo puede haber 3 proveedores principales')
        return super(product_supplierinfo, self).write(cr, uid, ids, vals, context)
        
    def create(self, cr, uid, vals, context=None):
        if not context:
            context = {}
        if vals['principal_supplier'] == True:
            principal_ids = self.pool.get('product.supplierinfo').search(cr, uid, [('principal_supplier', '=', 'True'), ('product_id', '=', vals['product_id'])], offset=0, limit=None, order=None, context=context, count=False)
            if len(principal_ids) > 2:
                raise osv.except_osv('Error', 'solo puede haber 3 proveedores principales')

        return super(product_supplierinfo, self).create(cr, uid, vals, context)
            
    
product_supplierinfo()
