import pandas as pd
from . import reason, weight

DISPLAY_COLS = [
    "search_column",
    "target_column_value",
    "compare_column_value",
    "target_metric_value",
    "compare_metric_value",
    "metric_change",
    "reason_coef",
]


def find_reason(
    df: pd.DataFrame,
    compare_col: str,
    compare_values: tuple,
    compare_metric: tuple = None,
    weight_metric: tuple = None,
    limit=20,
) -> pd.DataFrame:
    """
    find reason for diffrence
    """
    search_cols = [
        col for col in df.columns if df.dtypes[col].name in ["object", "bool"]
    ]
    if compare_col not in search_cols:
        search_cols.append(compare_col)
    reason_df_map = {}
    print("Search :" + ",".join(search_cols))
    for search_col in search_cols:
        reason_df_map[search_col] = reason.search_single_column(
            df,
            search_col,
            compare_col,
            compare_values,
            compare_metric,
        )

    if weight_metric is not None:
        weight_df = reason.search_single_column(
            df,
            search_col=compare_col,
            compare_col=compare_col,
            compare_values=compare_values,
            compare_metric=weight_metric,
        )
        weight.add_weight(weight_df, reason_df_map)

    total_diffrence_data = reason_df_map.pop(compare_col)
    total_diffrence = (
        total_diffrence_data["target_metric_value"].sum()
        - total_diffrence_data["compare_metric_value"].sum()
    )
    combined_reason_df = pd.concat(reason_df_map.values())
    combined_reason_df["reason_coef"] = (
        combined_reason_df["metric_change"] / total_diffrence
    )
    return (
        combined_reason_df[DISPLAY_COLS]
        .sort_values("reason_coef", ascending=False)
        .head(limit)
    )
