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
    "name": "Ofertas de proveedores",
    "version": "1.0",
    "depends": ["purchase"],
    "author": "Pexego",
    "category": "purchase",
    "description": """
    This module provide :
    """,
    "init_xml": [],
    'update_xml': ["wizard/generate_purchases_wizard_view.xml","purchase_oferts_view.xml"],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}
