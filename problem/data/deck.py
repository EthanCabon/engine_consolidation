import yaml, sys
import os.path

class Deck(): 

    def __init__(self, inputhpath):
        
        if not os.path.exists(inputhpath):
            print("File " + inputhpath)
            sys.exit(1)
        else:
            with open(inputhpath,'r') as f:
                ## Container of the tags parsed from the yaml file
                self.doc = yaml.load(f, Loader=yaml.BaseLoader)
        self.create_folder_structure()
        self.initialise_variables()

    def create_folder_structure(self):
        
        plot_dir = "./output/"
        check_folder = os.path.isdir(plot_dir)
        if not check_folder:
              os.makedirs(plot_dir)

    def initialise_variables(self):
        
        self.type = self.doc["Problem Type"]["Type"]
        self.dimension = int(self.doc["Problem Type"]["Dimension"])
        self.nmaterials = int(self.doc["Problem Type"]["Number of Materials"])
        
# =============================================================================
# # Number of objects
#         
#         self.nxob = self.doc["Dimensions"]["Number of Objects"]["Height"]
#         self.nyob = self.doc["Dimensions"]["Number of Objects"]["Width"]
#         self.nzob = self.doc["Dimensions"]["Number of Objects"]["Length"]
#         
# # Number of intervals per object
#         
#         self.ndx = self.doc["Simulation"]["Number of intervals per object"]["Thickness"]
#         self.ndy = self.doc["Simulation"]["Number of intervals per object"]["Width"]
#         self.ndz = self.doc["Simulation"]["Number of intervals per object"]["Length"]
#         
# # Number of elements
#         
#         self.nxtot = self.nxob*self.ndx+1
#         self.nytot = self.nyob*self.ndy+1
#         self.nztot = self.nzob*self.ndz+1
#         
# # Dimension of object
#         
#         self.xob = self.doc["Dimensions"]["Object"]["Thickness"]
#         self.yob = self.doc["Dimensions"]["Object"]["Width"]
#         self.zob = self.doc["Dimensions"]["Object"]["Length"]
#         
# # Dimension of the problem
#         
#         self.xtot = self.xob*self.nxob
#         self.ytot = self.yob*self.nyob
#         self.ztot = self.zob*self.nzob
#         
# # Space step
#         
#         self.dx = self.xob/self.ndx
#         self.dy = self.yob/self.ndy
#         self.dz = self.zob/self.ndz
# 
# # Material properties
#         
#         self.rho = np.zeros(self.nmaterials)
#         self.Cp = np.zeros(self.nmaterials)
#         self.h = np.zeros(self.nmaterials)
#         
#         self.kx = np.zeros(self.nmaterials)
#         self.ky = np.zeros(self.nmaterials)
#         self.kz = np.zeros(self.nmaterials)
#         
#         self.Dx = np.zeros(self.nmaterials)
#         self.Dy = np.zeros(self.nmaterials)
#         self.Dz = np.zeros(self.nmaterials)
#         
#         for i in range (self.nmaterials):
#             
#             self.rho[i] = float(self.deck.doc["Material+str(i+1)"]["Mechanical"]["Density"])
#             self.Cp[i] = float(self.deck.doc["Material+str(i+1)"]["Thermal"]["Heat Capacity"])
#             self.h[i] = float(self.deck.doc["Material+str(i+1)"]["Thermal"]["Heat Transfer Coefficient"])        
#             
#             self.kx[i] =  float(self.deck.doc["Material+str(i+1)"]["Thermal"]["Thermal Conductivity"]["x"])
#             self.ky[i] =  float(self.deck.doc["Material+str(i+1)"]["Thermal"]["Thermal Conductivity"]["x"])
#             self.kz[i] =  float(self.deck.doc["Material+str(i+1)"]["Thermal"]["Thermal Conductivity"]["x"])
#             
#             self.Dx[i] = self.kx/(self.rho*self.Cp)
#             self.Dy[i] = self.ky/(self.rho*self.Cp)
#             self.Dz[i] = self.kz/(self.rho*self.Cp)
# 
# =============================================================================
        