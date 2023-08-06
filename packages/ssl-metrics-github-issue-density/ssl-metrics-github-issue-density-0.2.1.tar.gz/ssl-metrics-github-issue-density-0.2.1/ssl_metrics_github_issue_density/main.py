from argparse import Namespace
from datetime import datetime

import numpy as np
import pandas
from dateutil.parser import parse as dateParse
from intervaltree import IntervalTree
from pandas import DataFrame

from ssl_metrics_github_issue_density.args import mainArgs


def getIssueTimelineIntervals(day0: datetime, issues: DataFrame) -> list:
    intervals = []

    foo: str
    bar: str
    for foo, bar in zip(issues["created_at"], issues["closed_at"]):
        try:
            startDate: datetime = dateParse(foo)
        except TypeError:
            startDate: datetime = foo

        try:
            endDate: datetime = dateParse(bar)
        except TypeError:
            endDate: datetime = bar

        startDate.replace(tzinfo=None)
        endDate.replace(tzinfo=None)

        startDaySince0 = (startDate.replace(tzinfo=None) - day0).days
        endDaySince0 = (endDate.replace(tzinfo=None) - day0).days

        intervals.append((startDaySince0, endDaySince0))

    return intervals


def buildIntervalTree(intervals: list) -> IntervalTree:
    tree: IntervalTree = IntervalTree()

    interval: tuple
    for interval in intervals:
        tree.addi(interval[0], interval[1] + 1, 1)

    return tree


def getDailyDefects(intervals: IntervalTree, timeline: list) -> list:
    defects: list = []

    day: int
    for day in timeline:
        defects.append(len(intervals[day]))

    return defects


def getDailyKLOC(commits: DataFrame, timeline: list) -> list:
    dailyKLOC: list = []
    previousKLOC: float = 0

    day: int
    for day in timeline:
        klocSum: float = (
            commits[commits["author_days_since_0"] == day]["lines_of_code"].mean() / 1000
        )

        if klocSum is np.nan:
            klocSum = previousKLOC

        dailyKLOC.append(klocSum)
        previousKLOC = klocSum

    return dailyKLOC


def main() -> None:
    args: Namespace = mainArgs()

    defectDensity: list = []

    commits: DataFrame = pandas.read_json(args.commits).T
    issues: DataFrame = pandas.read_json(args.issues).T

    day0: datetime = dateParse(issues["created_at"][0]).replace(tzinfo=None)
    dayN: datetime = datetime.now().replace(tzinfo=None)
    timeline: list = [day for day in range((dayN - day0).days)]

    issues["created_at"] = issues["created_at"].fillna(day0)
    issues["closed_at"] = issues["closed_at"].fillna(dayN)

    intervals: list = getIssueTimelineIntervals(day0, issues)
    intervalTree: IntervalTree = buildIntervalTree(intervals)

    dailyDefects: list = getDailyDefects(intervalTree, timeline)
    dailyKLOC: list = getDailyKLOC(commits, timeline)

    pair: tuple
    for pair in zip(dailyDefects, dailyKLOC):
        if pair[1] == 0:
            defectDensity.append(0)
        else:
            defectDensity.append(pair[0] / pair[1])

    data: dict = {
        "days_since_0": timeline,
        "defect_density": defectDensity,
    }

    DataFrame(data).to_json(args.output)


if __name__ == "__main__":
    main()
