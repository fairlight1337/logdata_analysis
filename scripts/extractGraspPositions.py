#!/usr/bin/python

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


import sys

from tools.OwlReader import OwlReader
from tools.DesignatorReader import DesignatorReader
from tools.TFReader import TFReader
from tools.Log import Log


class Processor(object):
    def __init__(self):
        self.rdrOwl = OwlReader()
        self.rdrDesig = DesignatorReader()
        self.rdrTF = TFReader()
    
    def readDirectory(self, directory):
        self.owl = self.rdrOwl.loadOwl(directory + "/cram_log.owl")
        self.desig = self.rdrDesig.loadDesignators(directory + "/logged_designators.json")
        self.tf = self.rdrTF.loadTransformations(directory + "/tf.json", [["odom_combined", "base_footprint"]])
    
    def transformAtTime(self, frame_from, frame_to, time):
        closest_low = self.tf[0]
        closest_high = self.tf[-1]
        
        for transform in self.tf:
            if transform["time"] <= time and transform["time"] > closest_low["time"]:
                closest_low = transform
            elif transform["time"] > time and transform["time"] < closest_high["time"]:
                closest_high = transform
        
        if time - closest_low["time"] < closest_high["time"] - time:
            return closest_low
        else:
            return closest_high
    
    def taskOfType(self, task_type):
        entries = []
        
        for ind in self.owl["task-tree-individuals"]:
            owl_ind = self.owl["task-tree-individuals"][ind]
            
            if owl_ind.type() == task_type:
                entries.append(owl_ind)
        
        return entries


if __name__=="__main__":
    p = Processor()
    
    p.readDirectory(sys.argv[1])
    
    for task in p.taskOfType("PickingUpAnObject"):
        subactions = task.subActions()
        
        for sa in subactions:
            owl_sa = p.owl["task-tree-individuals"][sa]
            
            if owl_sa.type() == "WithFailureHandling":
                pick_time = float(task.timeSpan()[0])
                transform = p.transformAtTime("odom_combined", "base_footprint", pick_time * 1000)
                
                translation = transform["transform"]["translation"]
                print "[\"" + str(owl_sa.taskSuccess()) + "\", " + str(translation["x"]) + ", " + str(translation["y"]) + ", " + str(translation["z"]) + "]"
                
                break;
