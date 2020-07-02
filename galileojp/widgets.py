import ipywidgets as widgets

from galileojp.frames import ExperimentFrameGateway


def experiment_dropdown(fgw: ExperimentFrameGateway):
    options = [(f'{row[1]}: {row[0]}', row[1]) for row in fgw.experiments()[['NAME', 'EXP_ID']].values]

    return widgets.Dropdown(
        options=options,
        description='Experiment:',
        disabled=False,
    )


def experiment_selector(fgw: ExperimentFrameGateway):
    options = [(f'{row[1]}: {row[0]}', row[1]) for row in fgw.experiments()[['NAME', 'EXP_ID']].values]
    exp_selector = widgets.SelectMultiple(options=options, description='Experiment:')
    return exp_selector
