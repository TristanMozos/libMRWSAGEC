# -*- coding: utf-8 -*-
'''
Created on 11 may. 2017

@author:     Tristán Mozos Pérez

@copyright:  2017 Halltic eSolutions S.L. All rights reserved.

@license:    GPLv3 - http://www.gnu.org/copyleft/gpl.html

This file is part of libMRWSAGEC.

libMRWSAGEC is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

libMRWSAGEC is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with libMRWSAGEC.  If not, see <http://www.gnu.org/licenses/>.

@contact: tristan.mozos@halltic.com
'''
class Producto(object):
    
    def __init__(self, idExterno='', nombreExterno='', cantidadEncargada='', refInterna='', ean='', precioProducto=None, precioEnvio=None):
        '''
        Constructor
        '''
        'Identificador externo del pedido en Amazon, eBay u otras plataformas'
        self.idExterno=idExterno
        'Nombre externo del producto'
        self.nombreExterno = nombreExterno
        'Cantidad de productos encargados'
        self.cantidadEncargada = cantidadEncargada
        'Identificador interno para el producto'
        self.refInterna=refInterna
        'EAN13'
        self.ean=ean
        'Importe del producto'
        self.precioProducto = precioProducto
        'Precio del pedido'
        self.precioEnvio = precioEnvio