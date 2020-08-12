import numpy as np

class Deposition:
    
    def __init__(self,meshing_layer):
        
        self.meshing_layer = meshing_layer
        
    def matrix_deposition(self):
        
        # An element of the matrix =0 if it has not been deposited yet and =1 if it has been deposited
        
        self.matrix_filament_deposited = np.zeros(self.meshing_layer.shape)
        
    def adjust_matrix(self,T,coordinates):
        
        xstart = self.meshing_layer.filament[coordinates]['xstart']
        xend = self.meshing_layer.filament[coordinates]['xend']        
        # ystart = self.meshing_layer.filament[coordinates]['ystart']
        # yend = self.meshing_layer.filament[coordinates]['yend']
        # zstart = self.meshing_layer.filament[coordinates]['zstart']
        # zend = self.meshing_layer.filament[coordinates]['zend']
        
        # self.matrix_filament_deposited[xstart:xend+1,ystart:yend+1,zstart:zend+1] = 1
        
        self.matrix_filament_deposited[xstart+1:xend+1] = 1
        
        self.Textrusion = float(self.deck.doc["Experimental Conditions"]["Extrusion Temperature [K]"])
        
        # T[xstart+1:xend+1,ystart+1:yend+1,zstart+1:zend+1] = self.Textrusion
        
        T[xstart+1:xend+1] = self.Textrusion
        