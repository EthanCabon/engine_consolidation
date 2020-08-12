import pdb

class Heat_Transfer:
        
    def __init__(self,meshing_layer):
        
        self.meshing_layer = meshing_layer
        
        
    # Idealy it should be Q=np.zeros(T.shape)
    # Maybe do something with self.deck.dimension
        
    def do_time_step(self,T):
        
        if len(T.shape) == 1:
            
            T[1:-1] = T[1:-1] + self.meshing_layer.MDx[1:-1] * self.meshing_layer.dt * ((T[2:] - 2*T[1:-1] + T[:-2]) / self.meshing_layer.Mdx[1:-1]**2) + self.meshing_layer.Q[1:-1] * self.meshing_layer.dt / (self.meshing_layer.Mrho[1:-1]*self.meshing_layer.MCp[1:-1])

        elif len(T.shape) == 2:
            
            T[1:-1, 1:-1] = T[1:-1, 1:-1] + self.meshing_layer.Dx * self.meshing_layer.dt * ((T[2:, 1:-1] - 2*T[1:-1, 1:-1] + T[:-2, 1:-1]) / self.dx**2) + self.meshing_layer.Dy * self.meshing_layer.dt * ((T[1:-1, 2:] - 2*T[1:-1, 1:-1] + T[1:-1, :-2]) / self.dy**2) + self.meshing_layer.Q[1:-1,1:-1] * self.meshing_layer.dt / (self.rho*self.Cp)

        elif len(T.shape) == 3:
            
            T[1:-1, 1:-1, 1:-1] = T[1:-1, 1:-1, 1:-1] + self.meshing_layer.Dx * self.meshing_layer.dt * ((T[2:, 1:-1, 1:-1] - 2*T[1:-1, 1:-1, 1:-1] + T[:-2, 1:-1, 1:-1]) / self.dx**2) + self.meshing_layer.Dy * self.meshing_layer.dt * ((T[1:-1, 2:, 1:-1] - 2*T[1:-1, 1:-1, 1:-1] + T[1:-1, :-2, 1:-1]) / self.dy**2) + self.meshing_layer.Dz * self.meshing_layer.dt * ((T[1:-1, 1:-1, 2:] - 2*T[1:-1, 1:-1, 1:-1] + T[1:-1, 1:-1, :-2]) / self.dz**2) + self.meshing_layer.Q[1:-1,1:-1,1:-1] * self.meshing_layer.dt / (self.rho*self.Cp) 
            
        else:
            
            return ('Wrong dimension')
        
    def do_one_point(self, dt, T, Tx0, Tx1, dx, Dx, Ty0=0, Ty1=0, Tz0=0, Tz1=0, dy=1, dz=1, Dy=0, Dz=0, Q=0, rho=1, Cp=1):
        
        T = T + Dx * dt * ((Tx0 - 2*T + Tx1) / dx**2) + Dy * dt * ((Ty0 - 2*T + Ty1) / dy**2) + Dz * dt * ((Tz0 - 2*T + Tz1) / dz**2) + Q * dt / (rho*Cp)
        
    def do_one_point_1D(self, T, Tx0, Tx1, Dx, Q=0, rho=1, Cp=1):
        
        Tnew = T + Dx * self.meshing_layer.dt * ((Tx0 - 2*T + Tx1) / self.meshing_layer.dx**2) + Q * self.meshing_layer.dt / (rho*Cp)
        
        return (Tnew)

    def do_one_point_2D(self, T, Tx0, Tx1, Ty0, Ty1, dt, dx, dy, Dx, Dy, Q=0, rho=1, Cp=1):
        
        T = T + Dx * dt * ((Tx0 - 2*T + Tx1) / dx**2) + Dy * dt * ((Ty0 - 2*T + Ty1) / dy**2) + Q * dt / (rho*Cp)
        
    def do_one_point_3D(self, T, Tx0, Tx1, Ty0, Ty1, Tz0, Tz1, dt, dx, dy, dz, Dx, Dy, Dz, Q=0, rho=1, Cp=1):
        
        T = T + Dx * dt * ((Tx0 - 2*T + Tx1) / dx**2) + Dy * dt * ((Ty0 - 2*T + Ty1) / dy**2) + Dz * dt * ((Tz0 - 2*T + Tz1) / dz**2) + Q * dt / (rho*Cp)        