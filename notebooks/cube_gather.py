import numpy as np
import fv3gfs.util

def gather(quantity: fv3gfs.util.Quantity, cube: fv3gfs.util.CubedSphereCommunicator):
    nx = None
    ny = None
    for dim, extent in zip(quantity.dims, quantity.extent):
        if dim in fv3gfs.util.X_DIMS:
            nx = extent
        elif dim in fv3gfs.util.Y_DIMS:
            ny = extent
    if nx != ny or (nx is None):
        raise NotImplementedError(
            f"Can only work with square domains that have x and y dimensions, "
            "received dims {quantity.dims} and interior shape {quantity.extent}"
        )
    obj = CubedSphere(f"c{nx}", cube.comm)
    return obj.gather(quantity)

class CubedSphere:

    def __init__(self, grid_name, comm, n_halo=3):

        # make sure this is a cubed-sphere grid
        assert grid_name[0] == 'c'

        # get number of gridpoints per tile edge
        self.ny_tile = self.nx_tile = int(grid_name[1:])
        assert str(self.ny_tile) == grid_name[1:]

        size = comm.Get_size()
        self.rank = comm.Get_rank()
        self.number_of_tiles = 6
        self.n_halo = n_halo

        ranks_per_tile = size // self.number_of_tiles
        assert ranks_per_tile * self.number_of_tiles == size

        ranks_per_tile_side = int( np.sqrt(ranks_per_tile) )
        assert ranks_per_tile == ranks_per_tile_side ** 2

        self.partitioner = fv3gfs.util.CubedSpherePartitioner(
            fv3gfs.util.TilePartitioner((ranks_per_tile_side, ranks_per_tile_side))
        )

        self.communicator = fv3gfs.util.CubedSphereCommunicator(comm, self.partitioner)

        self.tile = self.partitioner.tile_index(self.rank)

        self.ny, self.nx = self.ny_tile // ranks_per_tile_side, self.nx_tile // ranks_per_tile_side

    def get_rank(self):
        return self.rank

    def get_number_of_tiles(self):
        return self.number_of_tiles

    def get_tile(self):
        return self.partitioner.tile_index(self.rank)

    def get_shape(self):
        return (self.ny + 2*self.n_halo, self.nx + 2*self.n_halo)

    def get_num_halo(self):
        return self.n_halo

    def get_global_shape(self):
        return (self.number_of_tiles, self.ny_tile, self.nx_tile)

    def get_origin(self):
        return (self.n_halo, self.n_halo)

    def get_extent(self):
        return (self.ny, self.nx)

    def get_dims(self):
        return [fv3gfs.util.Y_DIM, fv3gfs.util.X_DIM]

    def get_j_range(self):
        return range(self.ny)

    def get_i_range(self):
        return range(self.nx)

    def local_to_global_index(self, ji_local):
        tile_partitioner = self.communicator.tile.partitioner
        j, i = ji_local
        tile_j, tile_i = tile_partitioner.subtile_index(self.rank)
        number_of_ranks_in_y, number_of_ranks_in_x = tile_partitioner.layout
        j_global = (self.ny_tile // number_of_ranks_in_y) * tile_j + j
        i_global = (self.nx_tile // number_of_ranks_in_x) * tile_i + i
        return (self.tile, j_global, i_global)

    def get_tile_root_rank(self, tile=None):
        if tile is None:
            tile = self.tile
        return tile * self.partitioner.tile.total_ranks

    def gather(self, field, field_global=None):
        field_tile = self.communicator.tile.gather(field, None)  # gather tiles onto the 6 root ranks of each tile
        if len(field.dims) == 2:
            # the root rank needs to have a global storage
            if self.rank == fv3gfs.util.constants.ROOT_RANK:
                if field_global is None:
                    field_global = fv3gfs.util.Quantity(np.zeros(self.get_global_shape()),
                                                    origin=(0, 0, 0), extent=self.get_global_shape(),
                                                    dims=['tile', fv3gfs.util.Y_DIM, fv3gfs.util.X_DIM], units="")
                field_global.view[0,:,:] = field_tile.view[:,:]
            for i in range(1, self.number_of_tiles):
                if self.rank == fv3gfs.util.constants.ROOT_RANK:
                    self.communicator.comm.Recv(field_global.view[i,:,:], source=self.get_tile_root_rank(tile=i), tag=i)
                if self.rank == self.get_tile_root_rank(tile=i):
                    self.communicator.comm.Send(field_tile.view[:,:], dest=fv3gfs.util.constants.ROOT_RANK, tag=i)
        elif len(field.dims) == 3:
            # the root rank needs to have a global storage
            if self.rank == fv3gfs.util.constants.ROOT_RANK:
                if field_global is None:
                    field_global = fv3gfs.util.Quantity(np.zeros(self.get_global_shape()),
                                                    origin=(0, 0, 0), extent=self.get_global_shape(),
                                                    dims=['tile', fv3gfs.util.Y_DIM, fv3gfs.util.X_DIM], units="")
                field_global.view[0,:,:] = field_tile.view[:,:, 0]
            for i in range(1, self.number_of_tiles):
                if self.rank == fv3gfs.util.constants.ROOT_RANK:
                    self.communicator.comm.Recv(field_global.view[i,:,:], source=self.get_tile_root_rank(tile=i), tag=i)
                if self.rank == self.get_tile_root_rank(tile=i):
                    self.communicator.comm.Send(field_tile.view[:,:, 0], dest=fv3gfs.util.constants.ROOT_RANK, tag=i)
        else:
            raise NotImplementedError("only written for 2D (x, y) or 3D (x, y, z) arrays")
        return field_global

