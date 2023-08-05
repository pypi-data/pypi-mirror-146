import pandas as pd


def search_single_column(
    df: pd.DataFrame,
    search_col: str,
    compare_col: str,
    compare_values: tuple,
    compare_metric: tuple = None,
):
    """
    search reason with single column
    """
    assert len(compare_values) == 2, "Length of compare_values should be 2. "
    target_col_val, compare_col_val = compare_values
    target_group = df[df[compare_col] == target_col_val].groupby(search_col)
    compare_group = df[df[compare_col] == compare_col_val].groupby(search_col)

    # support different compare_metric type
    if isinstance(compare_metric, tuple):
        target_df = target_group.agg(target_metric_value=compare_metric)
        compare_df = compare_group.agg(compare_metric_value=compare_metric)
    elif isinstance(compare_metric, dict):
        compare_metric_name = list(compare_metric.keys())[0]
        target_df = target_group.agg(compare_metric).rename(
            {compare_metric_name: "target_metric_value"}, axis=1
        )
        compare_df = compare_group.agg(compare_metric).rename(
            {compare_metric_name: "compare_metric_value"}, axis=1
        )
    else:
        target_df = target_group.agg(target_metric_value=(compare_col, "count"))
        compare_df = compare_group.agg(compare_metric_value=(compare_col, "count"))

    target_df.index.name = "target_column_value"
    compare_df.index.name = "compare_column_value"

    merged_df = pd.merge(
        target_df.reset_index(),
        compare_df.reset_index(),
        how="outer",
        left_on="target_column_value",
        right_on="compare_column_value",
    )
    FILL_NA_COLUMNS = ["target_metric_value", "compare_metric_value"]
    merged_df[FILL_NA_COLUMNS] = merged_df[FILL_NA_COLUMNS].fillna(0)
    sub_reason_data = merged_df.assign(
        search_column=search_col,
        metric_change=merged_df["target_metric_value"]
        - merged_df["compare_metric_value"],
    )
    return sub_reason_data
