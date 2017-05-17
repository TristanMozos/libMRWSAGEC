#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 27 dic. 2016

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
class Precio(object):
    
    def __init__(self, precio='', moneda=''):
        '''
        Constructor
        '''      
        'Precio'  
        self.precio = precio
        'Moneda'
        self.moneda = moneda