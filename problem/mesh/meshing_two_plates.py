class Meshing_Two_Plates:
    
    def __init__(self,deck):
        
        self.deck = deck
        self.dimension = self.doc["Problem Type"]["Dimension"]
        self.nmaterials = self.doc["Problem Type"]["Number of Materials"]
    
    def do_meshing(self):
        
# Number of plates
        
        self.nxplate = self.doc["Dimensions"]["Number of plates"]["Height"]
        self.nyplate = self.doc["Dimensions"]["Number of plates"]["Width"]
        self.nplate = self.nxplate*self.nyplate
        
# Number of intervals per plate
        
        self.ndx = self.doc["Simulation"]["Number of intervals per plate"]["Thickness"]
        self.ndy = self.doc["Simulation"]["Number of intervals per plate"]["Width"]
        
# Number of elements
        
        self.nxtot = self.nxplate*self.ndx+1
        self.nytot = self.nyplate*self.ndy+1
        
        
        self.meshing = np.zeros((self.nxtot, self.nytot))
        self.X = np.arange(0,self.nxtot)
        self.Y = np.arange(0,self.nytot)
        
    def apply_parameters(self):
        
        T = self.meshing
                
        T[:,:self.ndy] = self.deck.doc["Materials"]["Material1"]["Domain Initial Temperature"] # Set array size and set the interior value with Tini
        T[:,self.ndy+1:] = self.deck.doc["Materials"]["Material2"]["Domain Initial Temperature"] # Set array size and set the interior value with Tini
        T[:,self.ndy] = self.deck.doc["Processing Parameters"]["Temperature"]
        self.T = T.copy()
        
        DiffTotalX = self.meshing
        DiffTotalX[0:self.ny1, 0:self.nx1] = self.deck.doc["Materials"]["Material1"]["Thermal Diffusivity X"]
        DiffTotalX[self.ny1:self.ny2, 0:self.nx2] = self.deck.doc["Materials"]["Material2"]["Thermal Diffusivity X"]

        DiffTotalY = np.zeros((self.ny, self.nx)) 
        DiffTotalY[0:self.ny1, 0:self.nx1] = self.deck.doc["Materials"]["Material1"]["Thermal Diffusivity Y"]
        DiffTotalY[self.ny1:self.ny2, 0:self.nx2] = self.deck.doc["Materials"]["Material2"]["Thermal Diffusivity Y"]
        self.DiffTotalX = DiffTotalX.copy()
        self.DiffTotalY = DiffTotalY.copy()

        
        self.Visc = 1.14*10**(-12)*np.exp(26300/self.T)
        
        Dic = np.ones((self.nxtot, self.nytot))
        self.dic = 1/(1+0.45)
        Dic[:,self.ndy]=self.dic
        self.Dic=Dic.copy()   
        