import nest.topology as tp
import matplotlib.pyplot as plt
import nest.raster_plot
import math
import nest

nest.ResetKernel()

# neurons count
kol23= 54
kol4 = 34
kol5 = 28
kol6 = 25
N = kol23 + kol4 + kol5 + kol6
# glutamat neurons %
l23_Glu = 0.78
l4_GLu = 0.80
l5_Glu = 0.82
l6_Glu = 0.95
bias_begin = 140. # minimal value for the bias current injection [pA]
bias_end = 200. # maximal value for the bias current injection [pA]
T = 600 # simulation time (ms)

nest.CopyModel('iaf_neuron', 'pyr')
nest.CopyModel('iaf_neuron', 'in')
nest.CopyModel('static_synapse','exc',{'weight': 2.0})
nest.CopyModel('static_synapse','inh',{'weight':  -8.0})

# Layer23
row23_Glu = int(math.ceil(kol23*l23_Glu)/2)
row23_Gaba = (kol23 - row23_Glu*2)/2
sl23_Glu = tp.CreateLayer({'rows': row23_Glu, 'columns': 2, 'layers': 1,
'elements': 'pyr',
'center': [0., 0., 4.]})
sl23_Gaba = tp.CreateLayer({'rows': row23_Gaba, 'columns': 2, 'layers': 1,
'elements': 'in',
'center': [0.,1.,4.]})
fig1 = tp.PlotLayer(sl23_Glu, nodesize=10, nodecolor='orange')
fig2 = tp.PlotLayer(sl23_Gaba, nodesize=10, fig=fig1)

# Layer4
row4_Glu = int(math.ceil(kol4*l4_GLu)/2)
row4_Gaba = (kol4 - row4_Glu*2)/2
sl4_Glu = tp.CreateLayer({'rows': row4_Glu, 'columns': 2, 'layers': 1,
'elements': 'pyr',
'center': [0., 0., 3.]})
sl4_Gaba = tp.CreateLayer({'rows': row4_Gaba, 'columns': 2, 'layers': 1,
'elements': 'in',
'center': [0., 1., 3.]})
fig2 = tp.PlotLayer(sl4_Glu, nodesize=10, nodecolor='orange', fig=fig1)
fig2 = tp.PlotLayer(sl4_Gaba, nodesize=10, fig=fig1)

# Layer5
row5_Glu = int(math.ceil(kol5*l5_Glu)/2)
row5_Gaba = (kol5 - row5_Glu*2)/2
sl5_Glu = tp.CreateLayer({'rows': row5_Glu, 'columns': 2, 'layers': 1,
'elements': 'pyr',
'center': [0., 0., 2.]})
sl5_Gaba = tp.CreateLayer({'rows': row5_Gaba, 'columns': 2, 'layers': 1,
'elements': 'in',
'center': [0., 1., 2.]})
fig2 = tp.PlotLayer(sl5_Glu, nodesize=10, nodecolor='orange', fig=fig1)
fig2 = tp.PlotLayer(sl5_Gaba, nodesize=10, fig=fig1)

# Layer6
row6_Glu = int(math.ceil(kol6*l6_Glu)/2)
row6_Gaba = (kol6 - row6_Glu)/2
sl6_Glu = tp.CreateLayer({'rows': row6_Glu, 'columns': 2, 'layers': 1,
'elements': 'pyr',
'center': [0., 0., 1.]})
sl6_Gaba = tp.CreateLayer({'rows': row6_Gaba, 'columns': 2, 'layers': 1,
'elements': 'in',
'center': [0., 1., 1.]})
fig2 = tp.PlotLayer(sl6_Glu, nodesize=10, nodecolor='orange', fig=fig1)
fig2 = tp.PlotLayer(sl6_Gaba, nodesize=10, fig=fig1)

conndict_inh = {'connection_type': 'divergent',
'synapse_model': 'inh'}
conndict_exc = {'connection_type': 'divergent',
'synapse_model': 'exc'}

# exc connect glu:
tp.ConnectLayers(sl23_Glu, sl23_Gaba,conndict_exc)
tp.ConnectLayers(sl23_Glu, sl5_Gaba, conndict_exc)
tp.ConnectLayers(sl4_Glu, sl4_Gaba, conndict_exc)
tp.ConnectLayers(sl4_Glu, sl23_Glu, conndict_exc)
tp.ConnectLayers(sl5_Glu, sl5_Gaba, conndict_exc)
tp.ConnectLayers(sl5_Glu, sl23_Gaba, conndict_exc)
tp.ConnectLayers(sl5_Glu, sl6_Glu, conndict_exc)
tp.ConnectLayers(sl6_Glu, sl4_Glu, conndict_exc)

# inh connect gaba
tp.ConnectLayers(sl23_Gaba, sl23_Glu,conndict_inh)
tp.ConnectLayers(sl4_Gaba, sl4_Glu, conndict_inh)
tp.ConnectLayers(sl5_Gaba, sl5_Glu, conndict_inh)

#Get neurons Id
in_neurons = nest.GetNodes(sl4_Glu)[0]
all_neurons = nest.GetNodes(sl23_Gaba)[0] + nest.GetNodes(sl23_Glu)[0] + nest.GetNodes(sl4_Gaba)[0] + nest.GetNodes(sl4_Glu)[0] + nest.GetNodes(sl5_Gaba)[0] + nest.GetNodes(sl5_Glu)[0] + nest.GetNodes(sl6_Gaba)[0] + nest.GetNodes(sl6_Glu)[0]
in_thalamus = nest.GetNodes(sl5_Glu)[0] + nest.GetNodes(sl6_Glu)[0]

driveparams = {'amplitude':50., 'frequency':35.} #parameters for the alternative-current generator
noiseparams = {'mean':1.0, 'std':100.} #parameters for the noise generator
neuronparams = { 'tau_m':20., #membrane time constant
'V_th':20., #threshold potential
'E_L':10., #membrane resting potential
't_ref':2., #refractory period
'V_reset':0., #reset potential
'C_m':200., #membrane capacitance
'V_m':0.} #initial membrane potential

sd = nest.Create('spike_detector')
noise = nest.Create('noise_generator')
drive = nest.Create('ac_generator')

nest.SetStatus(drive, driveparams)
nest.SetStatus(noise, noiseparams)

nest.SetStatus(all_neurons, neuronparams)
nest.SetStatus(all_neurons, [{'I_e': (n * (bias_end - bias_begin) / N + bias_begin)} for n in all_neurons])

nest.SetStatus(sd, {"withgid": True, "withtime": True})

nest.Connect(drive, in_neurons)
nest.Connect(noise, all_neurons)
nest.Connect(in_thalamus, sd)

nest.Simulate(T)

nest.raster_plot.from_device(sd, hist=True)

plt.show()
