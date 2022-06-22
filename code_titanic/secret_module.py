import pandas as pd

def cross_tabulation (data, who_list):
    result = pd.DataFrame()
    for who in who_list:
        data_subset = data[data["who"]==who]
        result_subset = pd.crosstab(index = data_subset["class"],
                                    columns = data_subset["survived"],
                                    normalize = "index")
        result_subset["who"] = who
        result = result.append(result_subset)
    return result