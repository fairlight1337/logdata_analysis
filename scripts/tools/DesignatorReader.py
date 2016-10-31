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
                transformed_line = self.transformLine(line)
                the_json = json.loads(transformed_line)
                transformed_json = self.transformJSON(the_json)
                
                entries.append(transformed_json)
        
        return entries
    
    def transformLine(self, line):
        # Default: No transformation
        return line
    
    def transformJSON(self, raw_json):
        # Default: No transformation
        return raw_json


class TransformingDesignatorReader(DesignatorReader):
    def transformLine(self, line):
        old_offset = 0
        offset = old_offset
        transformed_line = ""
        idx = 0
        
        while offset > -1:
            offset = line.find('"" : ', offset)
            
            if offset > -1:
                transformed_line += line[old_offset:offset]
                old_offset = offset + 5
                
                transformed_line += '"' + str(idx) + '" : '
                idx += 1
                offset += 5
            else:
                transformed_line += line[old_offset:]
        
        return transformed_line
    
    def representsInt(self, s):
        try: 
            int(s)
            return True
        except ValueError:
            return False

    def transformJSON(self, raw_json):
        if isinstance(raw_json, list):
            clean_list = []
            for item in raw_json:
                clean_list.append(self.transformJSON(item))
            
            return clean_list
        elif isinstance(raw_json, dict):
            clean_dict = {}
            keys = raw_json.keys()
            keys.sort()
            
            all_numeric = True
            for key in keys:
                #print key
                if not self.representsInt(key):
                    all_numeric = False
                    break
            
            if all_numeric: # This is actually a list
                # Transform
                clean_list = []
                
                for key in keys:
                    clean_list.append(self.transformJSON(raw_json[key]))
                #print clean_list
                return clean_list
            else:
                clean_dict = {}
                for key in keys:
                    clean_dict[key] = self.transformJSON(raw_json[key])
                
                return clean_dict
        
        return raw_json