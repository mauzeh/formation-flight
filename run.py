#!/usr/bin/env python
"""Simulation Bootstrapper"""

#from runs.multihub.n_phi import run
#from runs.multihub.n_s import run
#from runs.multihub.n_pmin import run
#from runs.multihub.n_z import run
#from runs.multihub.n_dt import run
#from runs.multihub.pmin_phi import run
#from runs.multihub.L_Z_3hubs import run
#from runs.multihub.L_Z_1hub import run
#from runs.multihub.n_alpha import run

#from runs.calibrate import run
#from runs.visual_feedback import run

#from runs.multihub_line.n_s import run
#from runs.multihub_line.n_phi import run
from runs.multihub_line.n_pmin import run

if __name__ == '__main__':
    run.execute()

def plot():
    run.plot()