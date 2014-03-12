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
#############################################################################
from osv import osv, fields
from collections import deque

class maintenance_element(osv.osv):
    
    def _get_planta(self,cr ,uid, ids, field_name, args=None, context=None):
        result = {}
        elements = self.pool.get('maintenance.element').browse(cr, uid, ids, context)
        for element in elements:
            result[element.id]  = element.name
            elemento_aux = element
            while elemento_aux.padre_id:
                result[element.id] = elemento_aux.padre_id.name
                elemento_aux = elemento_aux.padre_id
        return result
    
    def _nombre_sin_planta(self, cr, uid, ids, name, args=None, context=None):
        result = {}
        elements = self.pool.get('maintenance.element').browse(cr, uid, ids, context)
        for element in elements:
            result[element.id] = ""
            if element.padre_id:
                arbol = deque()
                element_aux = element
                while element_aux.padre_id:
                    arbol.appendleft(element_aux)
                    element_aux = element_aux.padre_id
                for elemento in arbol:
                    result[element.id] += elemento.name + "/"
                result[element.id]=result[element.id][:-1]
            else:
                result[element.id] = element.name
        return result
    
    def _complete_name(self, cr, uid, ids, name, args=None, context=None):
        res = {}
        for m in self.browse(cr, uid, ids, context=context):
            names = [m.name]
            parent = m.padre_id
            while parent:
                names.append(parent.name)
                parent = parent.padre_id
            res[m.id] = ' / '.join(reversed(names))
        return res
    
    _name = 'maintenance.element' 
    _columns = {
            'name':fields.char('Nombre', size=60, required=True, readonly=False),
            'description': fields.text('Descripcion'),
            'type':fields.selection([
                ('estacion', 'Estacion'),
                ('subestacion', 'Subestacion'),
                ('bloque', 'bloque'),
                ('sistema', 'sistema'),
                ('equipos', 'equipos'),
                 ], 'Tipo', select=True),
            'padre_id':fields.many2one('maintenance.element', 'Padre', required=False),
            'hijo_ids':fields.one2many('maintenance.element', 'padre_id', 'Hijos', required=False),
            'complete_name': fields.function(_complete_name, type='char', size=256, string="Nombre completo",
                            store={'maintenance.element': (_complete_name, ['name', 'padre_id'], 10)}),
            'product_id':fields.many2one('product.product', 'Producto asociado', required=False),
            'asset_id':fields.many2one('account.asset.asset', 'Activo', required=False),
            'analytic_account_id':fields.many2one('account.analytic.account', 'Cuenta analitica', required=True),
            'codigo':fields.char('codigo', size=64, required=False, readonly=False),
            'maintenance_type_ids':fields.many2many('maintenance.type', 'maintenanceelement_maintenancetype_rel', 'element_id', 'type_id', 'Tipos de mantenimiento'),
            'planta':fields.function(_get_planta, method=True, type='char', string='Planta', store=False),
            'nombre_sin_planta':fields.function(_nombre_sin_planta, method=True, type='char', string='Nombre sin planta',
                                                  store = {
                                               'maintenance.element': (_nombre_sin_planta, ['name','padre_id'], 10),
                                               }),
            'order_ids':fields.many2many('maintenance.element', 'maintenanceelement_workorder_rel', 'element_id', 'order_id', 'Ordenes de trabajo', required=False),
              
                    }
maintenance_element()