import pdb

class Temperature_Change:
    
    def __init__(self,deck,meshing_layer,boundary_conditions,heat_transfer):
        
        self.deck = deck
        self.meshing_layer = meshing_layer
        self.boundary_conditions = boundary_conditions
        self.heat_transfer = heat_transfer
        self.calculate_temperature()  
        
    def do_time_step(self,Tnew,T,t):

        self.Ttot['t'+str(self.ntot+t)] = T
        self.heat_transfer.do_time_step(Tnew)
        value = self.boundary_conditions.convection(T[self.xend])
        Tout = self.boundary_conditions.Neumann_one_point(T[self.xend-1],value)
        Tnew[self.xend] = self.heat_transfer.do_one_point_1D(T[self.xend],T[self.xend-1],Tout,self.meshing_layer.Dx)
        T[:len(Tnew)] = Tnew
        return (T)
    
    def filament_deposition(self,T,coordinates):
        
        xstart = self.meshing_layer.filament[coordinates]['xstart']
        self.xend = self.meshing_layer.filament[coordinates]['xend']        
        
        self.Textrusion = float(self.deck.doc["Experimental Conditions"]["Extrusion Temperature [K]"])
        
        T[xstart+1:self.xend+1] = self.Textrusion
        
        return T
    
    
    def calculate_temperature(self):
        
        T = self.meshing_layer.meshing * self.meshing_layer.Troom
        T[0] = self.meshing_layer.Tbed
        
        self.Ttot = {}
        
        self.tfilament = float(self.deck.doc["Experimental Conditions"]["Time between 2 filament depositions [s]"])
        nt = int(self.tfilament/self.meshing_layer.dt)
        self.ntot = 0
        
        for i in range (self.meshing_layer.nxfil):
            
            T = self.filament_deposition(T,i+1)
            Tnew = T[:(i+1)*self.meshing_layer.ndx+1]
            self.meshing_layer.meshing_variables(i+1)
            
            for t in range (nt):
                T = self.do_time_step(Tnew,T,t)
                
            self.ntot += nt
        print(self.Ttot)
        pdb.set_trace()
        
        self.nt1 = int(float(self.deck.doc["Experimental Conditions"]["Time before cooling [s]"])/self.meshing_layer.dt)
               
        for t in range (self.nt1):
            
            T = self.do_time_step(Tnew,T,t)

        self.ntot += self.nt1

        Vcooling = float(self.deck.doc["Experimental Conditions"]["Vcooling [K.s-1]"])
        timecooling = (self.meshing_layer.Tbed-self.meshing_layer.Troom)/Vcooling
        self.nt2 = int(timecooling/self.meshing_layer.dt)
        
        for t in range (self.nt2):
            
            T = self.do_time_step(Tnew,T,t)
            T[0] -= Vcooling*self.meshing_layer.dt

        self.ntot += self.nt2
        
        self.nt3 = int(float(self.deck.doc["Experimental Conditions"]["Time after cooling [s]"])/self.meshing_layer.dt)
        
        for t in range (self.nt3):

            T = self.do_time_step(Tnew,T,t)
        
        self.ntot += self.nt3


# =============================================================================
#     def do_calculation(self):
#         
#         self.Troom = float(self.deck.doc["Experimental Conditions"]["Room Temperature"] )
#         T = self.meshing_layer.meshing * self.Troom
#         self.Tbed = self.deck.doc["Experimental Conditions"]["Bed Temperature [K]"]
#         T[0] = self.Tbed
#                 
#         self.nt = int(self.tfilament/self.meshing_layer.dt)
#         
#         for i in range (self.meshing_layer.nxfil):
#             
#             self.deposition.adjust_matrix(T,1)
#             xend = self.meshing_layer.filament[i+1]['xend']
#             for t in range (self.nt):
#                 self.Ttot = {'t'+str(i*self.nt+t): T}
#                 Tnew = self.heat_transfer.do_time_step(T[:xend+1])
#                 Tout = self.boundary_conditions.Neumann_one_point(self.T[xend-1],self.boundary_conditions.convection(self.T[xend]),self.meshing_layer.dx)
#                 Tnew[xend] = self.heat_transfer.do_one_point_1D(T[xend],T[xend-1],Tout)
#                 T = Tnew
#         
#         self.nt1 = int(float(self.deck.doc["Simulation"]["Time before cooling [s]"])/self.meshing_layer.dt)
#         
#         ntot = self.meshing_layer.nxfil*self.nt
#         
#         for t in range (self.nt1):
#             
#             self.Ttot = {'t'+str(ntot+t): T}
#             Tnew = self.heat_transfer.do_time_step(T[:xend+1])
#             Tout = self.boundary_conditions.Neumann_one_point(self.T[xend-1],self.boundary_conditions.convection(self.T[xend]),self.meshing_layer.dx)
#             Tnew[xend] = self.heat_transfer.do_one_point_1D(T[xend],T[xend-1],Tout)
#             T = Tnew
# 
#         ntot += self.nt1
# 
#         Vcooling = float(self.deck.doc["Simulation"]["Vcooling [K.s-1]"])
#         timecooling = (self.Tbed-self.Troom)/Vcooling
#         self.nt2 = int(timecooling/self.meshing_layer.dt)
#         
#         for t in range (self.nt2):
#             
#             self.Ttot = {'t'+str(ntot+t): T}
#             Tnew = self.heat_transfer.do_time_step(T[:xend+1])
#             Tout = self.boundary_conditions.Neumann_one_point(self.T[xend-1],self.boundary_conditions.convection(self.T[xend]),self.meshing_layer.dx)
#             Tnew[xend] = self.heat_transfer.do_one_point_1D(T[xend],T[xend-1],Tout)
#             T = Tnew
#             T[0] -= Vcooling*self.meshing_layer.dt
# 
# 
#         ntot += self.nt2
#         
#         self.nt3 = int(float(self.deck.doc["Simulation"]["Time after cooling [s]"])/self.meshing_layer.dt)
#         
#         for t in range (self.nt3):
# 
#             self.Ttot = {'t'+str(ntot+t): T}
#             Tnew = self.heat_transfer.do_time_step(T[:xend+1])
#             Tout = self.boundary_conditions.Neumann_one_point(self.T[xend-1],self.boundary_conditions.convection(self.T[xend]),self.meshing_layer.dx)
#             Tnew[xend] = self.heat_transfer.do_one_point_1D(T[xend],T[xend-1],Tout)
#         
#         ntot += self.nt3
# =============================================================================
