#!/usr/bin/env python
"""Simulation Bootstrapper"""

#from runs.flowrate import run
#from runs.singlehub.benchmark import run
#from runs.calibrate import run

#from runs.visual_feedback.timing import run
#from runs.visual_feedback.popup import run
#from runs.visual_feedback.calibrate import run
#from runs.visual_feedback.europe import run
#from runs.visual_feedback.usa import run
#from runs.visual_feedback.usa import run

#from runs.multihub.pmin_phi import run

#from runs.multihub_line.alpha_s import run
#from runs.multihub_line.n_alpha import run
#from runs.multihub_line.n_dt import run
#from runs.multihub_line.n_phi import run
#from runs.multihub_line.n_pmin import run
#from runs.multihub_line.n_s import run
#from runs.multihub_line.n_z import run
#from runs.multihub_line.n_z_zoomed import run

if __name__ == '__main__':
    run.execute()

def plot():
    run.plot()