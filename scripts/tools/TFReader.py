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

class TFReader:
    def __init__(self):
        pass
    
    def transformOK(self, frame, child):
        if frame in self.transformations:
            return child in self.transformations[frame]
        
        return False
    
    def loadTransformations(self, strFile, transformations):
        self.transformations = {}
        for transformation in transformations:
            if not transformation[0] in self.transformations:
                self.transformations[transformation[0]] = []
            
            self.transformations[transformation[0]].append(transformation[1])
        
        entries = []
        
        with open(strFile) as f:
            for line in f:
                parsed = json.loads(line)
                
                if "transforms" in parsed:
                    transforms = parsed["transforms"]
                    
                    for transform in transforms:
                        frame_id = transform["header"]["frame_id"]
                        child_frame_id = transform["child_frame_id"]
                        
                        if self.transformOK(frame_id, child_frame_id):
                            entries.append({"from" : frame_id,
                                            "to" : child_frame_id,
                                            "transform" : transform["transform"],
                                            "time" : transform["header"]["stamp"]["$date"]})
        
        return entries
