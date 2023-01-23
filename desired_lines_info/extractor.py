import pandas as pd


def extract():
    file_name = "ClusterToLine.csv"
    cluster_array = pd.read_csv(file_name, encoding='utf8')
    pd.options.display.max_columns = 15
    filtered_clusters = cluster_array.query('ClusterSubDesc == "מודיעין" and LineTypeDesc == "עירוני"')
    filtered_clusters.to_csv("filtered_routes.csv")


extract()
