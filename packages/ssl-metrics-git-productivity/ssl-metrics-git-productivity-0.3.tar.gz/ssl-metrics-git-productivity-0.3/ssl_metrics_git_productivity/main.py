import pandas
from pandas import DataFrame, Series

from ssl_metrics_git_productivity.args import mainArgs


def calculateProductivity(df: DataFrame) -> DataFrame:
    divedend: int = df["author_days_since_0"].max()
    daysSince0: Series = df["author_days_since_0"].unique()

    data: list = []

    day: int
    for day in range(daysSince0.max() + 1):
        temp: dict = {}

        productivity: float = (
            df[df["author_days_since_0"] == day]["delta_lines_of_code"].abs().sum()
            / divedend
        )

        temp["days_since_0"] = day
        temp["productivity"] = productivity

        data.append(temp)

    return DataFrame(data)


def main():
    args = mainArgs()

    df: DataFrame = pandas.read_json(args.input).T
    calculateProductivity(df).to_json(args.output)


if __name__ == "__main__":
    main()
