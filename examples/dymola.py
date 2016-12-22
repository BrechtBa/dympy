import dympy
import matplotlib.pyplot as plt


# create a dymola object
dymola = dympy.Dymola()

# clear all open models in the dymola instance
dymola.clear()

# open and compile a model
dymola.openModel('models//example.mo')
dymola.compile('example')

# write input signals and set parameters 
dymola.write_dsu({'time':[0,43200,86400],'Q_flow_hp':[1000,5000,2000],'Q_flow_sol':[500,600,700],'T_amb':[273.15,278.15,273.15]})
dymola.set_parameters({'C_in.C':5e6,'C_em.C':10e6,'UA_em_in.G':1600,'UA_in_amb.G':200})
dymola.set_parameters({'C_em.T':300})

# simulate
dymola.simulate(StopTime=86400)

# retrieve the result
res = dymola.get_result()

# find all results starting with ...
children = dympy.util.get_children(res,'UA_em_in')
print( '\n'.join(children) )

# plot the results
plt.figure()
ax = plt.subplot(211)
ax.plot(res['time']/3600,res['Q_flow_hp'],'r',label='hp')
ax.plot(res['time']/3600,res['Q_flow_sol'],'g',label='sol')
ax.set_ylabel('$\dot{Q}$ (W)')
plt.legend()

ax = plt.subplot(212)
ax.plot(res['time']/3600,res['C_in.T'],'r',label='in')
ax.plot(res['time']/3600,res['C_em.T'],'b',label='em')
ax.plot(res['time']/3600,res['T_amb'],'g',label='amb')
ax.set_ylabel('$T$ ($^\circ$C)')
ax.set_xlabel('time (h)')
plt.legend()



# use simulation outputs as new inputs, simulate and retrieve the results
dymola.dsfinal2dsin()
dymola.simulate(StartTime=86400,StopTime=2*86400)
res2 = dymola.get_result()

# plot the new results
plt.figure()
ax = plt.subplot(211)
ax.plot(res2['time']/3600,res2['Q_flow_hp'],'r',label='hp')
ax.plot(res2['time']/3600,res2['Q_flow_sol'],'g',label='sol')
ax.set_ylabel('$\dot{Q}$ (W)')
plt.legend()

ax = plt.subplot(212)
ax.plot(res2['time']/3600,res2['C_in.T'],'r',label='in')
ax.plot(res2['time']/3600,res2['C_em.T'],'b',label='em')
ax.plot(res2['time']/3600,res2['T_amb'],'g',label='amb')
ax.set_ylabel('$T$ ($^\circ$C)')
ax.set_xlabel('time (h)')
plt.legend()


# disconnect from dymola
dymola.disconnect()

# show plots
plt.show()

# python continues but does not exit after closing the figures
# this is related to the win32ui package