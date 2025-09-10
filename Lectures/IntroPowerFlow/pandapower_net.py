# Import PandaPower package and name it pp
import pandapower as pp

# Create an empty network object
net = pp.create_empty_network()

# Per unit bases (3-phase values)
Pbase = 100  # MVA
Vbase = 345 # kV

# Create buses (geodata are coordinates for graphical representation)
b1 = pp.create_bus(net, vn_kv=Vbase, name="Bus 1", geodata=(0,1))
b2 = pp.create_bus(net, vn_kv=Vbase, name="Bus 2", geodata=(2.5,0))
b3 = pp.create_bus(net, vn_kv=Vbase, name="Bus 3", geodata=(5,1))

# Create bus elements
pp.create_ext_grid(net, bus=b1, vm_pu=1.00, name="Grid Connection")
pp.create_load(net, bus=b3, p_mw=5*Pbase, q_mvar=1*Pbase, name="Load")
pp.create_gen(net, bus=b2, p_mw=2*Pbase, vm_pu=1.05, name="PV")

# Create branch elements. 
# Here I neglect shunct capacitances.
Zbase = Vbase**2 / Pbase
X_km = 0.376
R_km = 0.037
l12_km = 150
l23_km = 150
l31_km = 200

pp.create_line_from_parameters(net, name="line1", from_bus = b1, to_bus = b2,
        length_km=l12_km, r_ohm_per_km = R_km, x_ohm_per_km = X_km,
        c_nf_per_km = 0, max_i_ka = 0.2)
pp.create_line_from_parameters(net, name="line2", from_bus = b2, to_bus = b3,
        length_km=l23_km, r_ohm_per_km = R_km, x_ohm_per_km = X_km,
        c_nf_per_km = 0, max_i_ka = 0.2)
pp.create_line_from_parameters(net, name="line3", from_bus = b3, to_bus = b1,
        length_km=l31_km, r_ohm_per_km = R_km, x_ohm_per_km = X_km,
        c_nf_per_km = 0, max_i_ka = 0.2)

# Solve the model
pp.runpp(net)