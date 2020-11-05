import numpy as np
import matplotlib.pyplot as plt
import gt4py
from gt4py.storage.storage import Storage

def get_ij_slice(storage: Storage, k=0):
    return np.asarray(storage[:, :, k])

def find_nice_min_max(data, data2=None, decimal_places=1, vmin=None, vmax=None):
    data_min, data_max = data.min(), data.max()
    if data2 is not None:
        data_min = np.minimum(data_min, data2.min())
        data_max = np.maximum(data_max, data2.max())
    multiplier = pow(10., decimal_places)
    vmin_default = np.floor(multiplier * data_min) / multiplier
    vmax_default = np.ceil(multiplier * data_max) / multiplier
    if vmin is None:
        vmin = vmin_default
    if vmax is None:
        vmax = vmax_default
    return vmin, vmax

def plot_ij_slice(data, ax, plt, title: str, k=0, vmin=None, vmax=None):
    vmin, vmax = find_nice_min_max(data, vmin=vmin, vmax=vmax)
    im = ax.imshow(data.transpose(), origin='lower', vmin=vmin, vmax=vmax)
    ax.set_xlabel('i-index')
    ax.set_ylabel('j-index')
    ax.title.set_text(title)
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

def plot_two_ij_slices(in_storage: Storage, out_storage: Storage, k=0, vmin=None, vmax=None):
    data_in = get_ij_slice(in_storage, k=k)
    data_out = get_ij_slice(out_storage, k=k)
    vmin, vmax = find_nice_min_max(data_in, data2=data_out, vmin=vmin, vmax=vmax)
    fig, ax = plt.subplots(figsize=(12,4), ncols=2)
    plot_ij_slice(data_in, ax[0], plt, title='input', k=k, vmin=vmin, vmax=vmax)
    plot_ij_slice(data_out, ax[1], plt, title='output', k=k, vmin=vmin, vmax=vmax)
    fig.tight_layout()
