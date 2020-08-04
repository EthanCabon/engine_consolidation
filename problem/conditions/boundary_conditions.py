import numpy as np

class Boundary_Conditions:
    
    def __init__(self, deck):
        
        self.deck = deck
        self.load_datas_layers(deck)
        
    def load_datas(self,deck):
        
        # creation of a dictionnary to save boundary conditions
        
        self.BD = {}
        
        for i in range (1,self.deck.doc["Boundary Conditions"]["Number of boundary conditions"]+1):
            
            self.BD['localisation'+str(i)] = self.deck.doc["Boundary Conditions"]["BD"+str(i)]["Localisation"]
            self.BD['model'+str(i)] = self.deck.doc["Boundary Conditions"]["BD"+str(i)]["Model"]
            self.BD['value'+str(i)] = self.deck.doc["Boundary Conditions"]["BD"+str(i)]["Value"]            
            
            
    def Dirichlet(self, position, value):
        
        position[:] = value

    def Neumann(self, U, position, direction, value, dx):
        
        # Neumann condition : (U[x+1]-U[x-1])/(2*dx) = value
        
        # "direction" is a vector which determines in what direction the Neumann condition is applied
        # "position" is the dictionnary below that indicates where the condition is applied
        # position = {'xstart': ,'xend': ,'ystart': ,'yend': 'zstart': ,'zend': }
        # value corresponds to "convection" in the 3D printing case
        # dx is the space interval between 2 elements of the vector "position
        
        u = 1*(direction!=0)
        
        v = 1*(direction<0)
        
        self.Uextend = np.zeros(len(U.shape[0])+u[0],len(U.shape[1])+u[1],len(U.shape[2])+u[2])
        # for the elements at the end of the problem, we can not apply heat transfer because U[x+1] or U[x-1] does not exist
        # so we extend the matrix to create an imaginary point whose value is defined by the Neumann condition
        
        self.Uextend[:position["xstart"]+v[0],:position["ystart"]+v[1],:position["zstart"]+v[2]] = U[:position["xstart"]+v[0],:position["ystart"]+v[1],:position["zstart"]+v[2]]
        self.Uextend[position["xend"]+v[0]:,position["yend"]+v[1]:,position["zend"]+v[2]:] = U[position["xstart"]+v[0]:,position["ystart"]+v[1]:,position["zstart"]+v[2]:]
        # the values of the matrix U are inserted in Uextend
        self.Uextend[position["xstart"]+v[0]:position["xend"]+v[0],position["ystart"]+v[1]:position["yend"]+v[1],position["zstart"]+v[2]:position["zend"]+v[2]] = \
            self.Uextend[position["xstart"]-v[0]:position["xend"]-v[0],position["ystart"]-v[1]:position["yend"]-v[1],position["zstart"]-v[2]:position["zend"]-v[2]]-2*dx*value
        # the values of the neumann conditions are added to Uextend
                
    def boundary_layers(self,deck,T):
        
        self.Tbed = float(self.deck.doc["Experimental Conditions"]["Bed Temperature"])
        
        if len(T.shape) == 1:
            
            T[0] = self.Tbed
                       
        elif len(T.shape) == 2:
            
            T[1:-1, 1:-1] = T[1:-1, 1:-1] + Dx * self.dt * ((T[2:, 1:-1] - 2*T[1:-1, 1:-1] + T[:-2, 1:-1]) / self.dx**2) + Dy * self.dt * ((T[1:-1, 2:] - 2*T[1:-1, 1:-1] + T[1:-1, :-2]) / self.dy**2) + Q[1:-1,1:-1] * self.dt / (self.rho*self.Cp)
            
        elif len(T.shape) == 3:
            
            T[1:-1, 1:-1, 1:-1] = T[1:-1, 1:-1, 1:-1] + Dx * self.dt * ((T[2:, 1:-1, 1:-1] - 2*T[1:-1, 1:-1, 1:-1] + T[:-2, 1:-1, 1:-1]) / self.dx**2) + Dy * self.dt * ((T[1:-1, 2:, 1:-1] - 2*T[1:-1, 1:-1, 1:-1] + T[1:-1, :-2, 1:-1]) / self.dy**2) + Dz * self.dt * ((T[1:-1, 1:-1, 2:] - 2*T[1:-1, 1:-1, 1:-1] + T[1:-1, 1:-1, :-2]) / self.dz**2) + Q[1:-1,1:-1,1:-1] * self.dt / (self.rho*self.Cp) 
            
        else:
            
            return ('Wrong dimension')
            