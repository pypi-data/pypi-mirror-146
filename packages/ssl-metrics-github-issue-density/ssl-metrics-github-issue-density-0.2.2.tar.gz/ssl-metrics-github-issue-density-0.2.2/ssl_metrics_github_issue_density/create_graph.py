'''creates a graph given arguments'''

from argparse import ArgumentParser, Namespace

import pandas as pd
from matplotlib.figure import Figure
from pandas import DataFrame

from args import check_args, get_graph_args
from graph_util import SSLGraph, appendID, window


def main() -> None:

    # get args, check, proceed
    args: Namespace = get_graph_args()
    check_args(args)

    df: DataFrame = pd.read_json(args.input)

    job_args = [args.data, args.best_fit, args.velocity, args.acceleration]
    job_names = ["data", "best_fit", "velocity", "acceleration"]
    jobs = [j for j, i in zip(job_names, job_args) if i]

    x, y = window(
        df=df,
        column="defect_density",
        xmin=args.x_min,
        xmax=args.x_max,
        stepper=args.stepper,
    )

    for job in jobs:

        g = SSLGraph(job=job, x=x, y=y, maxdeg=args.maximum_polynomial_degree)

        g.set(
            column="defect_density",
            repo=args.repo,
            stepper=args.stepper,
            output=args.output,
        )

        g.build()


if __name__ == "__main__":
    main()
