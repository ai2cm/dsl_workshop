import numpy as np
import matplotlib.pyplot as plt
import gt4py
from gt4py.storage.storage import Storage

def get_ij_slice(storage: Storage, k=0):
    return np.asarray(storage[:, :, k])

def find_nice_min_max(data, data2=None, data3=None, decimal_places=1, vmin=None, vmax=None):
    data_min, data_max = data.min(), data.max()
    if data2 is not None:
        data_min = np.minimum(data_min, data2.min())
        data_max = np.maximum(data_max, data2.max())
    if data3 is not None:
        data_min = np.minimum(data_min, data3.min())
        data_max = np.maximum(data_max, data3.max())
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

def plot_two_ij_slices(in_storage: Storage, out_storage: Storage, k=0, vmin=None, vmax=None, titles=['input', 'output']):
    data_in = get_ij_slice(in_storage, k=k)
    data_out = get_ij_slice(out_storage, k=k)
    vmin, vmax = find_nice_min_max(data_in, data2=data_out, vmin=vmin, vmax=vmax)
    fig, ax = plt.subplots(figsize=(12,4), ncols=2)
    plot_ij_slice(data_in, ax[0], plt, title=titles[0], k=k, vmin=vmin, vmax=vmax)
    plot_ij_slice(data_out, ax[1], plt, title=titles[1], k=k, vmin=vmin, vmax=vmax)
    fig.tight_layout()

def plot_three_ij_slices(field1: Storage, field2: Storage, field3: Storage, k=0, vmin=None, vmax=None, titles=['field1', 'field2', 'field3']):
    data1 = get_ij_slice(field1, k=k)
    data2 = get_ij_slice(field2, k=k)
    data3 = get_ij_slice(field3, k=k)
    vmin, vmax = find_nice_min_max(data1, data2=data2, data3=data3, vmin=vmin, vmax=vmax)
    fig, ax = plt.subplots(figsize=(12,4), ncols=3)
    plot_ij_slice(data1, ax[0], plt, title=titles[0], k=k, vmin=vmin, vmax=vmax)
    plot_ij_slice(data2, ax[1], plt, title=titles[1], k=k, vmin=vmin, vmax=vmax)
    plot_ij_slice(data3, ax[2], plt, title=titles[2], k=k, vmin=vmin, vmax=vmax)
    fig.tight_layout()
