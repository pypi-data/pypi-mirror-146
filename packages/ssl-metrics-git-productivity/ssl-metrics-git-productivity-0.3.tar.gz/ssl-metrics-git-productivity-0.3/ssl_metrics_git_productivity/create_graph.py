from argparse import ArgumentParser, Namespace
from operator import itemgetter
from os import path

import matplotlib.pyplot as plt
import numpy as np
import pandas
from matplotlib.figure import Figure
from pandas import DataFrame
from sklearn.metrics import r2_score

from args import get_graph_args, check_args
from graph_util import Graph, appendID

def main():

    args: Namespace = get_graph_args()
    check_args(args)

    xlabel = f"Every {args.stepper} Days"
    ylabels = ["", "", "d/dx", "d^2/dx^2"]

    df: DataFrame = pandas.read_json(args.input)
    prod = df['productivity']

    name: str = "Productivity"

    xwindow = lambda maximum: [i for i in range(len(df["productivity"]))][
        args.x_min : maximum : args.stepper
    ]
    ywindow = lambda column, maximum: df[column].tolist()[
        args.x_min : maximum : args.stepper
    ]

    y_vars = ["LOC", "KLOC", "DLOC"]
    columns = ["loc_sum", "kloc", "delta_loc"]

    if args.x_max <= -1:
        x: list = xwindow(-1)
        prod = ywindow('productivity', -1)
    else:
        x: list = xwindow(args.x_max + 1)
        prod = ywindow('productivity', args.x_max + 1)


    jobs = ["data", "best_fit", "velocity", "acceleration"]
    graph_types = [args.data, args.best_fit, args.velocity, args.acceleration]
    subtitles = {job:job.replace("_", " ").capitalize() for job in jobs}


    for arg, job, i in zip(graph_types, jobs, [0, 1, 2, 3]):

        if arg:

            prefix = f"""{subtitles[job]+" of " if job not in ["data", "all"] else ""}"""
            title = f"{prefix}{args.repository_name} {name} / {xlabel}"
            filename = appendID(filename=args.output, id=f"{name.lower()}_{job}")

            ylabel = f"{ylabels[i]} {name}"  # i should never be 4
            g = Graph(
                job=job,
                x=x,
                y=prod,
                title=title,
                xlabel=xlabel,
                ylabel=ylabel,
                maxdeg=args.maximum_polynomial_degree,
                filename=filename,
            )
            g.build(save=True)




if __name__ == "__main__":
    main()
