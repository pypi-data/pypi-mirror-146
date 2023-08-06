import os
import logging

import pandas as pd
from pkg_resources import resource_stream

from geofred.utils import build_map

state_fname = "state.csv"

# this_dir = os.path.dirname(os.path.realpath(__file__))
# state_fpath = os.path.join(this_dir, state_fname)
state_fpath = resource_stream("geofred.storage", f"{state_fname}")

logging.debug("reading from state file {state_fpath}.")
DF_STATE = pd.read_csv(state_fpath)
logging.debug("done.")


def build_state_map():
    return build_map(DF_STATE, ["State", "Abvr"])


STATE_MAP = build_state_map()
