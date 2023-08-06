

# Cell
from functools import cached_property

import matplotlib.pyplot as plt
import numpy as np
import param
from tqdm.auto import tqdm, trange

import holoviews as hv
import hvplot.xarray  # noqa
import pandas as pd
import xarray as xr
from nbverbose.showdoc import show_doc
from planetarypy.utils import iso_to_nasa_date
from .calib.greg import filter_spica_for_date
from .io import UVPDS, UVISObs
from .pds import CatalogFilter

hv.extension("bokeh")