from problem import *

# Nothing in the main yet

cwd = os.getcwd()

deck = Deck(cwd + "/deck_printing3D.yaml")

geometry = Geometry_Printing3D(deck)

meshing = Meshing_Layer(deck, geometry)

boundary_conditions = Boundary_Conditions(meshing)

heat_transfer = Heat_Transfer(meshing)

temperature_change = Temperature_Change(deck, meshing, boundary_conditions, heat_transfer)