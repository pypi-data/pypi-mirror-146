from . import reason


def add_weight(weight_df, reason_df_map):

    weights = weight_df[["target_metric_value", "compare_metric_value"]].values
    if weights.shape[0] > 1:
        weights = weights.sum(0)
    target_weight, compare_weight = weights

    for search_col in reason_df_map:
        sub_reason_df = reason_df_map.get(search_col)
        sub_reason_df["target_metric_value"] = (
            sub_reason_df["target_metric_value"] / target_weight
        )
        sub_reason_df["compare_metric_value"] = (
            sub_reason_df["compare_metric_value"] / compare_weight
        )
        sub_reason_df["metric_change"] = (
            sub_reason_df["target_metric_value"] - sub_reason_df["compare_metric_value"]
        )
