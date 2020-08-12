import numpy as np
class HeatTransfer:

    def __init__(self, deck,meshes,BC):
        self.dt = float(deck.doc["Simulation"]["Time Step"])
        self.dx2 = meshes.dx*meshes.dx
        self.dy2 = meshes.dy*meshes.dy
        self.rho=meshes.RhoTotal
        self.cp=meshes.CpTotal
        self.k=meshes.KtotalX
        self.dx2 = meshes.Mdx*meshes.Mdx
        self.dy2 = meshes.Mdy*meshes.Mdy
        self.BC=BC
        self.Mdy=meshes.Mdy
        self.Mdx=meshes.Mdx
        self.h= float(deck.doc["Boundary Condition"]["Convective Coefficient"])


# -------------- BEGIN HEAT TRANSFER CALCULATION---------- 




    def do_convection(self, u0, u, Diffx, Diffy,Q):
        # Propagate with forward-difference in time, central-difference in space



        Q=np.zeros(np.shape(self.BC.T))
        Q[0,:] =self.h*(float(self.BC.Troom) - u[0,:])
        Q[-1,:]=self.h*(float(self.BC.Troom) - u[-1,:])
        Q[:,-1]=self.h*(float(self.BC.Troom) - u[:,-1])     
        Q[:,0] =self.h*(float(self.BC.Troom) - u[:,0])    
        self.Q=Q


        valuex=np.zeros(np.shape(self.BC.T))
        valuey=np.zeros(np.shape(self.BC.T))    
        valuey[0,:] = -Q[0,:]/ self.BC.Ky[0,:]
        valuey[-1,:]= -Q[-1,:]/self.BC.Ky[-1,:]
        valuex[:,-1]= -Q[:,-1]/self.BC.Kx[:,-1]
        valuex[:,0 ]= -Q[:,0]/ self.BC.Kx[:,0]
        self.valuex=valuex
        self.valuey=valuey


        Uoutx=np.zeros(np.shape(self.BC.T))
        Uouty=np.zeros(np.shape(self.BC.T))
        Uouty[0,:] =u[1,:] -2*self.Mdy[0,:] *valuey[0,:]        
        Uouty[-1,:]=u[-2,:]-2*self.Mdy[-1,:]*valuey[-1,:]        
        Uoutx[:,-1]=u[:,-2]-2*self.Mdx[:,-1]*valuex[:,-1]
        Uoutx[:,0]= u[:,1] -2*self.Mdx[:,0] *valuex[:,0]


        self.Uoutx=Uoutx
        self.Uouty=Uouty



        u[0,1:-1]     = u0[0,1:-1]     + Diffy[0,1:-1] *self.dt*      ((u0[1,1:-1]    -2*u[0,1:-1]      + Uouty[0,1:-1]) /self.dy2[0,1:-1])      + Diffx[0,1:-1] *self.dt*       ((u0[0, 2:]    -2*u0[0,1:-1]     +u0[0,:-2])/self.dx2[0,1:-1]) 
        u[-1,1:-1]    = u0[-1,1:-1]    + Diffy[-1,1:-1]*self.dt*      ((u0[-2,1:-1]   -2*u[-1,1:-1]     + Uouty[-1,1:-1])/self.dy2[-1,1:-1])     + Diffx[-1,1:-1]*self.dt*       ((u0[-1, 2:]   -2*u0[-1,1:-1]    +u0[-1,:-2])/self.dx2[-1,1:-1]) 
        # u[1:-1, 1:-1] = u0[1:-1, 1:-1] + Diffy[1:-1, 1:-1]* self.dt * ((u0[2:, 1:-1] - 2*u0[1:-1, 1:-1] + u0[:-2, 1:-1])/self.dy2[1:-1, 1:-1] ) + Diffx[1:-1, 1:-1]* self.dt *  ((u0[1:-1, 2:] -2*u0[1:-1, 1:-1] +u0[1:-1, :-2])/self.dx2[1:-1, 1:-1] )

        u[1:-1,0]     = u0[1:-1,0]     + Diffy[1:-1,0] *self.dt*      ((u0[2:,0 ]     -2*u[1:-1,0]      + u0[0:-2,0]) /self.dy2[1:-1,0])       + Diffx[1:-1, 0]*self.dt*       ((u0[1:-1, 1 ] -2*u0[1:-1,0]     +Uoutx[1:-1,0])/self.dx2[1:-1,0])        
        u[1:-1,-1]    = u0[1:-1,-1]    + Diffy[1:-1,-1]*self.dt*      ((u0[2:,-1]     -2*u[1:-1,-1]     + u0[0:-2,-1])/self.dy2[1:-1,-1])      + Diffx[1:-1,-1]*self.dt*       ((u0[1:-1, -2 ]-2*u0[1:-1,-1]    +Uoutx[1:-1,-1])/self.dx2[1:-1,-1]) 
        # u[1:-1, 1:-1] = u0[1:-1, 1:-1] + Diffy[1:-1, 1:-1]* self.dt * ((u0[2:, 1:-1] - 2*u0[1:-1, 1:-1] + u0[:-2, 1:-1])/self.dy2[1:-1, 1:-1] ) + Diffx[1:-1, 1:-1]* self.dt *  ((u0[1:-1, 2:] -2*u0[1:-1, 1:-1] +u0[1:-1, :-2])/self.dx2[1:-1, 1:-1] )

        u[0,0]   = u0[0,0]      +Diffy[0,0]      *self.dt*((u0[1,0]   -2*u[0,0]    + Uouty[0,0])/self.dy2[0,0])         +Diffx[0,0]     *self.dt*((u0[0, 1]     -2*u0[0,0]    +Uoutx[0,0])/self.dx2[0,0])
        u[-1,0]  = u0[-1,0]     +Diffy[-1,0]     *self.dt*((u0[-2,0]  -2*u[-1,0]   + Uouty[-1,0])/self.dy2[-1,0])       +Diffx[-1,0]    *self.dt*((u0[-1, 1]    -2*u0[-1,0]   +Uoutx[-1,0])/self.dx2[-1,0])  
        u[0,-1]  = u0[0,-1]     +Diffy[0,-1]     *self.dt*((u0[1,-1]  -2*u[0,-1]   + Uouty[0,-1])/self.dy2[0,-1])       +Diffx[0,-1]    *self.dt*((u0[0, -2]    -2*u0[0,-1]   +Uoutx[0,-1])/self.dx2[0,-1])
        u[-1,-1] = u0[-1,-1]    +Diffy[-1,-1]    *self.dt*((u0[-2,-1] -2*u[-1,-1]  + Uouty[-1,-1])/self.dy2[-1,-1])     +Diffx[-1,-1]   *self.dt*((u0[-1,-2]    -2*u0[-1,-1] +Uoutx[-1,-1])/self.dx2[-1,-1])


        u0=u.copy()

        return u0,u
    
    def do_timestep(self, u0, u, Diffx, Diffy,Q):
        
        # Propagate with forward-difference in time, central-difference in space
        u[1:-1, 1:-1] = u0[1:-1, 1:-1] + Diffy[1:-1, 1:-1]* self.dt * ((u0[2:, 1:-1] - 2*u0[1:-1, 1:-1] + u0[:-2, 1:-1])/self.dy2 ) + Diffx[1:-1, 1:-1]* self.dt * ( (u0[1:-1, 2:] - 2*u0[1:-1, 1:-1] + u0[1:-1, :-2])/self.dx2 ) + self.dt*Q[1:-1,1:-1]/(self.cp[1:-1,1:-1]*self.rho[1:-1,1:-1])
        u[1:-1, 1:-1] = u0[1:-1, 1:-1] + Diffy[1:-1, 1:-1]* self.dt * ((u0[2:, 1:-1] - 2*u0[1:-1, 1:-1] + u0[:-2, 1:-1])/self.dy2[1:-1, 1:-1] ) + Diffx[1:-1, 1:-1]* self.dt * ( (u0[1:-1, 2:] - 2*u0[1:-1, 1:-1] + u0[1:-1, :-2])/self.dx2[1:-1, 1:-1] ) + self.dt*Q[1:-1,1:-1]/(self.BC.Cp[1:-1,1:-1]*self.BC.Rho[1:-1,1:-1])

        u0 = u.copy()

        return u0, u

# -------------- END HEAT TRANSFER CALCULATION---------- 