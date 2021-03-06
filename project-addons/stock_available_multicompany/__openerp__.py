# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2004-2012 Pexego Sistemas Informáticos All Rights Reserved
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
{
    "name" : "Stock Available Multicompany",
    "description": """
       Module that show for each sale order line the available stock of your
       respective product in the warehouses of all companies that have
       authorized the active user.
        """,
    "version" : "1.0",
    "author" : "Pexego",
    "depends" : ["base", "product","sale", "stock", "product_stock_unsafety"],
    "category" : "Crm",
    "init_xml" : [],
    "data" : ["wizard/stock_available_multicompany_wzd_view.xml",
              "product_view.xml"],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
