##
## Copyright (c) 2016, Jan Winkler <jan.winkler.84@gmail.com>.
## All rights reserved.
## 
## This file is part of semrec_plugins.
##
## logdata_analysis is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 2 of the License, or
## (at your option) any later version.
## 
## logdata_analysis is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with logdata_analysis.  If not, see <http://www.gnu.org/licenses/>.
##

## \author Jan Winkler


import json

class DesignatorReader:
    def __init__(self):
        pass
    
    def loadDesignators(self, strFile):
        entries = []
        with open(strFile) as f:
            for line in f:
                entries.append(json.loads(line))
        
        return entries
