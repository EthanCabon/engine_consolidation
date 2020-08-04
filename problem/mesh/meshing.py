import numpy as np

# this class creates a mesh for both layer and two_plates problems

class Meshing:
    
    def __init__(self,deck):
        
        self.deck = deck
        self.dimension = self.doc["Problem Type"]["Dimension"]
        self.nmaterials = self.doc["Problem Type"]["Number of Materials"]
    
    def do_meshing(self):
        
        if self.dimension != 1 or 2 or 3:
            
            return ('Wrong dimension')
        
        elif self.dimension >= 1:
            
            self.nxobj = self.doc["Dimensions"]["Number of objects"]["Height"]
            self.ndx = self.doc["Simulation"]["Number of intervals per object"]["Thickness"]
            self.nxtot = self.nxobj*self.ndx+1
            self.X = np.arange(0,self.nxtot)
            self.meshing = np.ones(self.nxtot)
            
        elif self.dimension >= 2:
            
            self.nyobj = self.doc["Dimensions"]["Number of objects"]["Width"]
            self.ndy = self.doc["Simulation"]["Number of intervals per object"]["Width"]
            self.nytot = self.nyobj*self.ndy+1
            self.Y = np.arange(0,self.nytot)
            self.meshing = np.ones((self.nxtot,self.nytot))
            
        elif self.dimension >= 3:
            
            self.nzobj = self.doc["Dimensions"]["Number of objects"]["Length"]
            self.ndz = self.doc["Simulation"]["Number of intervals per object"]["Length"]
            self.nztot = self.nzobj*self.ndz+1
            self.Z = np.arange(0,self.nztot)
            self.meshing = np.ones((self.nxtot,self.nytot,self.nztot))
            
        return (self.meshing)