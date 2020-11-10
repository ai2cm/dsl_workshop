import serialbox as ser
import numpy as np
import gt4py
import gt4py.gtscript as gtscript
import gt4py.storage as gt_storage

backend = "numpy"
F_TYPE = np.float32

@gtscript.stencil(backend=backend)
def heat_update(curr_T   : gtscript.Field[F_TYPE],
                future_T : gtscript.Field[F_TYPE],
                *,
                scale    : np.float32):
    with computation(PARALLEL), interval(...):
        future_T = curr_T + scale * (curr_T[-1,0,0] - 2.0*curr_T + curr_T[1,0,0]) \
                          + scale * (curr_T[0,-1,0] - 2.0*curr_T + curr_T[0,1,0]) \
                          + scale * (curr_T[0,0,-1] - 2.0*curr_T + curr_T[0,0,1])

        curr_T = future_T

serializer = ser.Serializer(ser.OpenModeKind.Read, './data', 'HEAT')

sp = serializer.get_savepoint('starting_heat')

curr_T = serializer.read('init_T', sp[0])
scale     = serializer.read('scale', sp[0])
t_steps   = serializer.read('t_steps', sp[0])

curr_T_gt = gt_storage.from_array(curr_T, 
                                  backend=backend, 
                                  default_origin=(1,1,1))

future_T_gt = gt_storage.zeros(backend=backend, 
                               dtype=F_TYPE, 
                               shape=(curr_T.shape[0], curr_T.shape[1], curr_T.shape[2]),
                               default_origin=(1,1,1))

for curr_step in range(t_steps[0]):
    heat_update(curr_T=curr_T_gt,
                future_T=future_T_gt,
                scale=scale[0],
                domain=(curr_T.shape[0]-2, curr_T.shape[1]-2, curr_T.shape[2]-2))

sp = serializer.get_savepoint('final_heat')
final_T = serializer.read('final_T', sp[0])

if np.allclose(final_T,curr_T_gt):
    print("Solution is valid!")

