# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2004-2014 Pexego Sistemas Informáticos All Rights Reserved
#    $Marta Vázquez Rodríguez$ <marta@pexego.es>
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

from openerp.osv import osv, fields
import time
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class product_stock_unsafety(osv.Model):
    _inherit = 'product.stock.unsafety'

    def create_or_write(self, cr, uid, vals, context=None):
        if context is None:
            context = {}

        ids = self.search(cr, uid, [('state', '=', vals['state']),
                                    ('product_id', '=', vals['product_id']),
                                    ('supplier_id', '=', vals['supplier_id'])],
                          context=context)
        if ids:
            self.write(cr, uid, ids, vals, context=context)
        else:
            self.create(cr, uid, vals, context=context)
