import ipywidgets as widgets

from galileojp.frames import ExperimentFrameGateway


def experiment_dropdown(fgw: ExperimentFrameGateway):
    options = fgw.experiments()['EXP_ID']

    return widgets.Dropdown(
        options=options,
        description='Experiment:',
        disabled=False,
    )
