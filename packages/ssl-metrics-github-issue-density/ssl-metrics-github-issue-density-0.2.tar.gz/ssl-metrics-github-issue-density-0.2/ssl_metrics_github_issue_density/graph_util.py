"""tools for graphing"""

from operator import itemgetter
from pathlib import Path
from textwrap import wrap

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from sklearn.metrics import r2_score


def window(*, df, column, xmin, xmax, stepper):
    """returns x,y formatted from args"""

    """TODO: ask nick why
    put in check_args() ?
    """
    xmax = -1 if xmax <= -1 else xmax + 1

    x = [i for i in range(len(df[column]))][xmin:xmax:stepper]
    y = df[column].tolist()[xmin:xmax:stepper]

    return x, y


def findBestFitLine(x: list, y: list, maximumDegree: int) -> tuple:
    """returns a best fit line given a maximum polynomial degree"""

    # https://www.w3schools.com/Python/python_ml_polynomial_regression.asp
    data: list = []

    degree: int
    for degree in range(maximumDegree):
        model: np.poly1d = np.poly1d(np.polyfit(x, y, degree))
        r2Score: np.float64 = r2_score(y, model(x))
        temp: tuple = (r2Score, model)
        data.append(temp)

    return max(data, key=itemgetter(0))


def to_title(str):
    """returns a string formatted as a title"""
    return str.replace("_", " ").capitalize()


def appendID(filename: str, id: str) -> str:
    """returns a string formatted as a filename"""
    # https://stackoverflow.com/a/37487898
    p = Path(filename)
    return f"{Path.joinpath(p.parent, p.stem)}_{id}{p.suffix}"


class SSLGraph:
    def __init__(self, *, job="data", x, y, maxdeg=1):

        self.x = x
        self.y = y
        self.maxdeg = maxdeg

        # for multiple graphs in future
        self.jobs = ["data", "best_fit", "velocity", "acceleration"]  # all
        # self.jobs = {k: int(job in k) for k in self.jobs}
        self.job = job
        self.filename = ""

    def set_filename(self, *, column, output):
        """sets a graph output filename"""

        self.output = output
        self.filename = appendID(filename=output, id=f"{column.lower()}_{self.job}")

    def set_labels(self, *, name, repo, stepper):
        """sets graph labels"""

        """TODO: ask nick ... commits vs days label
            commits
                loc
                kloc
                dloc
            days
                prod
                ddensity
                bus_factor
        """

        self.xlabel = f"Every {stepper} Commits"
        ylabels = ["", "", "d/dx", "d^2/dx^2"]
        self.ylabel = f"{ylabels[self.jobs.index(self.job)]} {name}"

        prefix = f"""{to_title(self.job) + " of " if self.job not in self.jobs[1:] else ""}"""
        self.title = f"{prefix}{repo} {name} / {self.xlabel}"

    def set(self, *, column, repo, stepper, output):
        """sets filename and labels"""

        # for multiple graphs in future
        # subtitles = [job.replace("_", " ").capitalize() for job in self.jobs]

        name = to_title(column)

        self.set_filename(column=column, output=output)
        self.set_labels(name=name, repo=repo, stepper=stepper)

    def build(self):
        "builds an axes"

        # https://towardsdatascience.com/clearing-the-confusion-once-and-for-all-fig-ax-plt-subplots-b122bb7783ca

        # if job == "all":
        # fig, axs = subplots(2,2)
        # axs[0].plot()
        # axs[1].plot()

        fig, ax = plt.subplots()
        ax.set(
            xlabel=self.xlabel,
            ylabel=self.ylabel,
            title="\n".join(wrap(self.title, width=60)),
        )

        if type(self.maxdeg) is int:
            data: tuple = findBestFitLine(x=self.x, y=self.y, maximumDegree=self.maxdeg)
            bfModel: np.poly1d = data[1]
            line: np.ndarray = np.linspace(0, max(self.x), 100)

        """TODO
        return line to overlay plots"""

        if self.job == "best_fit":
            ax.plot(line, bfModel(line))

        if self.job == "velocity":
            velocityModel = np.polyder(p=bfModel, m=1)
            ax.plot(line, velocityModel(line))

        if self.job == "acceleration":
            accelerationModel = np.polyder(p=bfModel, m=2)
            ax.plot(line, accelerationModel(line))

        if self.job == "data":
            ax.plot(self.x, self.y)

        fig.tight_layout()

        if self.filename:
            fig.savefig(self.filename)

        return fig, ax
