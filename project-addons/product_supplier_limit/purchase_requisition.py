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

class purchase_requisition(orm.Model):
    _inherit = 'purchase.requisition'

    def create(self, cr , uid, vals, context=None):
        id_created = super(purchase_requisition, self).create(cr, uid, vals, context)
        if not context:
            context = {}
        requisition = self.browse(cr, uid, id_created, context)
        for line in requisition.line_ids:
            principal_supplierinfo_ids = self.pool.get('product.supplierinfo').search(cr, uid, [('product_tmpl_id', '=', line.product_id.product_tmpl_id.id), ('principal_supplier', '=', True)], offset=0, limit=None, order=None, context=context, count=False)
            principal_supplierinfos = self.pool.get('product.supplierinfo').browse(cr, uid, principal_supplierinfo_ids, context)
            count_purchases_maked = 0
            for supplierinfo in principal_supplierinfos:
                self.make_purchase_order(cr, uid, [requisition.id], supplierinfo.name.id, context=context)
                count_purchases_maked += 1
        return id_created
