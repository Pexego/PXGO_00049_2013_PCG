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
{
    "name": "historico de codigo de producto",
    "version": "1.0",
    "depends": ["product"],
    "author": "Pexego",
    "category": "Product",
    "description": """
    This module provide :
    -histórico de códigos de producto
    """,
    "init_xml": [],
    'update_xml': ['product_view.xml','security/ir.model.access.csv', ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}
