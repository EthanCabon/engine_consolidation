import numpy as np
import sys

class Geometry_Printing3D:
    
    def __init__(self,deck):
        
        self.deck = deck
        self.dimension = self.deck.dimension
        self.geometry_filament()
        self.geometry_problem()
        
    def geometry_filament(self):
              
        if self.dimension not in {1, 2, 3}:

            print ('Wrong dimension')
            sys.exit()

        self.lenXfil = float(self.deck.doc["Dimensions"]["Filament"]["Thickness [m]"])
            
        if self.dimension >= 2:
            
            self.lenYfil = float(self.deck.doc["Dimensions"]["Filament"]["Width [m]"])
            
        elif self.dimension >= 3:
            
            self.lenZfil = float(self.deck.doc["Dimensions"]["Filament"]["Length [m]"])
         

    def geometry_problem(self):
            
        self.nxfil = int(self.deck.doc["Dimensions"]["Number of filaments"]["Height"])
        self.lenXtot = self.lenXfil * self.nxfil
        self.x = np.linspace(0,self.lenXtot,self.nxfil+1)
        #self.x = np.arange(self.nxfil+1)
            
        if self.dimension >= 2:
            
            self.nyfil = int(self.deck.doc["Dimensions"]["Number of filaments"]["Width"])
            self.lenYtot = self.lenYfil * self.nyfil
            self.y = np.linspace(0,self.lenYtot,self.nyfil+1)
            #self.y = np.arange(self.nyfil+1)
            self.Y,self.X = np.meshgrid(self.y,self.x)
            
        elif self.dimension >= 3:
            
            self.nzfil = int(self.deck.doc["Dimensions"]["Number of filaments"]["Length"])
            self.lenZtot = self.lenZfil * self.nzfil
            self.z = np.linspace(0,self.lenZtot,self.nzfil+1)
            #self.z = np.arange(self.nzfil+1)
            self.Y,self.X,self.Z = np.meshgrid(self.y,self.x,self.z)
        