# -*- coding: utf-8 -*-

'''
Created on 22 dic. 2016

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
import os
import ConfigParser

class utComun(object):
    def __init__(self, params):
        '''
        Constructor
        '''   
        
    @staticmethod
    def absoluteFilePaths(directory):
        ficheros = []
        for dirpath, _, filenames in os.walk(directory):
            for f in filenames:
                ficheros.append(os.path.abspath(os.path.join(dirpath, f)))            
        return ficheros
    
    @staticmethod
    def recogeFileSiExisteEnWks(rutaCfg):
        import os.path
        
        pyPath = os.environ['PYTHONPATH'].split(':')
        
        if rutaCfg.find('/')!=0:
            rutaCfg = '/'+rutaCfg
        
        for fPath in pyPath:
            path = fPath+rutaCfg
            if os.path.isfile(path):
                return path
            
    @staticmethod
    def recogeDirSiExisteEnWks(rutaCfg):
        import os.path
        
        pyPath = os.environ['PYTHONPATH'].split(':')
        
        if rutaCfg.find('/')!=0:
            rutaCfg = '/'+rutaCfg
        
        for fPath in pyPath:
            path = fPath+rutaCfg
            if os.path.isdir(path):
                return path

class utConfig(object):
    '''
        
    '''    
    def __init__(self, rutaCfg):
        rutaCfg = utComun.recogeFileSiExisteEnWks(rutaCfg) 
        
        self.config = ConfigParser.ConfigParser()
        self.config.read(rutaCfg)        
        self.section=''
    
    def configMapOptions(self, section=''):
        self.section=section
        dict1 = {}
        options = self.config.options(self.section)   
        for option in options:
            try:
                dict1[option] = self.config.get(self.section, option)                
            except:
                dict1[option] = None                
        return dict1
    
    def configOption(self, option):
        try:
            return self.configMapOptions(section=self.section)[option]
        except:
            return None 

        