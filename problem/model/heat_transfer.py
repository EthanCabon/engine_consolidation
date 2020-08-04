import numpy as np

class HeatTransfer:
    
    def do_timestep(self, T, Dx, Dy=None, Dz=None, Q=np.zeros((1,1,1))):
        
        if len(T.shape) == 1:
            
            T[1:-1] = T[1:-1] + Dx * self.dt * ((T[2:] - 2*T[1:-1] + T[:-2]) / self.dx**2) + Q[1:-1] * self.dt / (self.rho*self.Cp)
            
        elif len(T.shape) == 2:
            
            T[1:-1, 1:-1] = T[1:-1, 1:-1] + Dx * self.dt * ((T[2:, 1:-1] - 2*T[1:-1, 1:-1] + T[:-2, 1:-1]) / self.dx**2) + Dy * self.dt * ((T[1:-1, 2:] - 2*T[1:-1, 1:-1] + T[1:-1, :-2]) / self.dy**2) + Q[1:-1,1:-1] * self.dt / (self.rho*self.Cp)
            
        elif len(T.shape) == 3:
            
            T[1:-1, 1:-1, 1:-1] = T[1:-1, 1:-1, 1:-1] + Dx * self.dt * ((T[2:, 1:-1, 1:-1] - 2*T[1:-1, 1:-1, 1:-1] + T[:-2, 1:-1, 1:-1]) / self.dx**2) + Dy * self.dt * ((T[1:-1, 2:, 1:-1] - 2*T[1:-1, 1:-1, 1:-1] + T[1:-1, :-2, 1:-1]) / self.dy**2) + Dz * self.dt * ((T[1:-1, 1:-1, 2:] - 2*T[1:-1, 1:-1, 1:-1] + T[1:-1, 1:-1, :-2]) / self.dz**2) + Q[1:-1,1:-1,1:-1] * self.dt / (self.rho*self.Cp) 
            
        else:
            
            return ('Wrong dimension')
        
        return T
    
    def convection(self, h, k, T, Tout, sign):
        
        # sign = 1 if position (T) > position (Tout)
        # sign = -1 if position (T) < position (Tout)
        
        return (sign*h*(T-Tout)/k)
        