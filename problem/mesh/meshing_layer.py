import numpy as np

class Meshing_Layer:
    
    def __init__(self, deck, geometry_printing3D):
        
        self.deck = deck
        self.geometry_printing3D = geometry_printing3D
        self.do_meshing()
        self.position_filament()
        self.variables()        
        
    def do_meshing(self):
    
# =============================================================================
# # Number of filaments
#         
#         self.nxfil = self.deck.doc["Dimensions"]["Number of filaments"]["Height"]
#         self.nyfil = self.deck.doc["Dimensions"]["Number of filaments"]["Width"]
#         self.nzfil = self.deck.doc["Dimensions"]["Number of filaments"]["Length"]
#         
# # Number of intervals per filament
#         
#         self.ndx = self.deck.doc["Simulation"]["Number of intervals per filament"]["Thickness"]
#         self.ndy = self.deck.doc["Simulation"]["Number of intervals per filament"]["Width"]
#         self.ndz = self.deck.doc["Simulation"]["Number of intervals per filament"]["Length"]
#         
# # Number of elements
#         
#         self.nxtot = self.nxob*self.ndx+1
#         self.nytot = self.nyob*self.ndy+1
#         self.nztot = self.nzob*self.ndz+1
#         
# =============================================================================

        
        self.nxfil = int(self.deck.doc["Dimensions"]["Number of filaments"]["Height"])
        self.ndx = int(self.deck.doc["Simulation"]["Number of intervals per filament"]["Thickness"])
        self.nxtot = self.nxfil*self.ndx+1
        self.meshing = np.ones(self.nxtot)
        self.x = np.linspace(0,self.geometry_printing3D.lenXtot,self.nxtot)
            
        if self.deck.dimension >= 2:
            
            self.nyfil = int(self.deck.doc["Dimensions"]["Number of filaments"]["Width"])
            self.ndy = int(self.deck.doc["Simulation"]["Number of intervals per filament"]["Width"])
            self.nytot = self.nyfil*self.ndy+1
            self.meshing = np.ones((self.nxtot,self.nytot))
            self.y = np.linspace(0,self.geometry_printing3D.lenYtot,self.nytot)
            # self.Y,self.X = np.meshgrid(self.y,self.x)
            
        elif self.deck.dimension >= 3:
            
            self.nzfil = int(self.deck.doc["Dimensions"]["Number of filaments"]["Length"])
            self.ndz = int(self.deck.doc["Simulation"]["Number of intervals per filament"]["Length"])
            self.nztot = self.nzfil*self.ndz+1
            self.meshing = np.ones((self.nxtot,self.nytot,self.nztot))
            self.z = np.linspace(0,self.geometry_printing3D.lenZtot,self.nztot)
            # self.Y,self.X,self.Z = np.meshgrid(self.y,self.x,self.z)


# With the position of the filament in the matrix of filaments, you have access to the coordinates of the elements in the matrix of elements

    def position_filament(self):
        
        filament = dict()
        
        if self.deck.dimension ==1:
            for i in range (self.nxfil):
                filament[i+1]={'xstart': i*self.ndx,'xend': (i+1)*self.ndx}
        elif self.deck.dimension == 2:
            for i in range (self.nxfil):
                for j in range (self.nyfil):
                    filament[(i+1,j+1)]={'xstart': i*self.ndx,'xend': (i+1)*self.ndx,'ystart': j*self.ndy,'yend': (j+1)*self.ndy}
        elif self.deck.dimension == 3:   
            for i in range (self.nxfil):
                for j in range (self.nyfil):
                    for k in range (self.nzfil):
                        filament[(i+1,j+1,k+1)]={'xstart': i*self.ndx,'xend': (i+1)*self.ndx,'ystart': j*self.ndy,'yend': (j+1)*self.ndy,'zstart': k*self.ndz,'zend': (k+1)*self.ndz}

        self.filament = filament



    def variables(self):
        
        self.dx = self.geometry_printing3D.lenXfil/self.ndx
        self.kx =  float(self.deck.doc["Material1"]["Thermal"]["Thermal Conductivity [W.m-1.K-1]"]["x"])
        self.rho = float(self.deck.doc["Material1"]["Mechanical"]["Density [kg.m-3]"])
        self.Cp = float(self.deck.doc["Material1"]["Thermal"]["Specific Heat [J.kg-1.K-1]"])
        self.Dx = self.kx/(self.rho*self.Cp)
        self.h = float(self.deck.doc["Material1"]["Thermal"]["Convection Coefficient [W.m-2.K-1]"] )        
        
        self.dt = float(self.deck.doc["Simulation"]["Time step [s]"])
        self.Troom = float(self.deck.doc["Experimental Conditions"]["Room Temperature [K]"])
        self.Tbed = float(self.deck.doc["Experimental Conditions"]["Bed Temperature [K]"])

    def meshing_variables(self,nfildeposited):
        
        self.Mdx = self.meshing[:nfildeposited*self.ndx+1] * self.dx
        self.Mkx = self.meshing[:nfildeposited*self.ndx+1] * self.kx
        self.Mrho =  self.meshing[:nfildeposited*self.ndx+1] * self.rho
        self.MCp =  self.meshing[:nfildeposited*self.ndx+1] * self.Cp
        self.MDx = self.meshing[:nfildeposited*self.ndx+1] * self.Dx
        self.Q = self.meshing[:nfildeposited*self.ndx+1] * 0
        
# =============================================================================
#     def structure_filament(self,filament):
#         
#         if len(filament.shape) == 1:
#             
#             self.structure1 = filament[1:-1]
#             self.structure0 = np.array((filament[0],filament[-1]))
#             
#         elif len(filament.shape) == 2:
#         
#             self.structure2 = filament[1:-1,1:-1]
#             self.structure1 = np.array((filament[0,1:-1],filament[-1,1:-1],filament[1:-1,0],filament[1:-1,-1]))
#             self.structure0 = np.array(())
#         
#         elif len(filament.shape) == 3:
#             
#             self.structure3 = filament[1:-1,1:-1,1:-1]
#             self.structure2 = np.array((filament[0,1:-1,1:-1],filament[-1,1:-1,1:-1],filament[1:-1,0,1:-1],filament[1:-1,-1,1:-1],filament[1:-1,1:-1,0],filament[1:-1,1:-1,-1]))
#             self.structure1 = np.array((filament[0,0,1:-1],filament[0,-1,1:-1],filament[0,1:-1,0],filament[0,1:-1,-1],filament[-1,0,1:-1],filament[-1,-1,1:-1],filament[-1,1:-1,0],filament[-1,1:-1,-1],filament[1:-1,0,0],filament[1:-1,0,-1],filament[1:-1,-1,0],filament[1:-1,-1,-1]))
#             self.structure0 = np.array ((filament[0,0,0],filament[0,0,-1],filament[0,-1,0],filament[0,-1,-1],filament[-1,0,0],filament[-1,0,-1],filament[-1,-1,0],filament[-1,-1,-1]))
#         
# # =============================================================================
# #             self.volume = 
# #             self.surface = 
# #             self.edge = 
# #             self.corner = 
# # 
# # =============================================================================
# 
# =============================================================================

    
        
            
            
            