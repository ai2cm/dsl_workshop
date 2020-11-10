import serialbox as ser
import numpy as np

serializer = ser.Serializer(ser.OpenModeKind.Read, './data', 'HEAT')

sp = serializer.get_savepoint('starting_heat')

curr_T = serializer.read('init_T', sp[0])
scale     = serializer.read('scale', sp[0])
t_steps   = serializer.read('t_steps', sp[0])

future_T = np.zeros((curr_T.shape[0],
                        curr_T.shape[1],
                        curr_T.shape[2]),dtype='float32')

for curr_step in range(t_steps[0]):
    for ii in range(1,curr_T.shape[2]-1):
        for jj in range(1, curr_T.shape[1]-1):
            for kk in range(1, curr_T.shape[2]-1):
                future_T[ii,jj,kk] = curr_T[ii,jj,kk] \
                  + scale[0] * (curr_T[ii-1,jj,   kk]   - 2.0*curr_T[ii,jj,kk] + curr_T[ii+1,jj,  kk]) \
                  + scale[0] * (curr_T[ii,  jj-1, kk]   - 2.0*curr_T[ii,jj,kk] + curr_T[ii,  jj+1,kk]) \
                  + scale[0] * (curr_T[ii,  jj,   kk-1] - 2.0*curr_T[ii,jj,kk] + curr_T[ii,  jj,  kk+1])


    curr_T[:,:,:] = future_T[:,:,:]

sp = serializer.get_savepoint('final_heat')
final_T = serializer.read('final_T', sp[0])

if np.allclose(final_T,curr_T):
    print("Solution is valid!")

