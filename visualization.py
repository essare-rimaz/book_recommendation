import dask.dataframe as dd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

books = dd.read_csv("data\\BX-Book-Ratings.txt", encoding="latin1", delimiter=";", dtype={"ISBN": "string"})
means = books["Book-Rating"].value_counts(normalize=True).rename("Percentage").compute()
#means = means.mul(100).rename("Percent").reset_index()
#means = means["Book-Rating"].value_counts(normalize=True).reset_index().compute()
x = pd.DataFrame(means).reset_index(level=0)
x.rename(columns={"index": "Ratings"}, inplace=True)

sns.catplot(x="Ratings", y="Percentage", kind="bar", data=x)
plt.show()

# individual_means = books.groupby("ISBN")["Book-Rating"].mean().compute()
# individual_means = pd.DataFrame(individual_means).reset_index(level=0)
# #TODO tady je potreba ty means zaokouhlit
# individual_means = dd.from_pandas(individual_means, npartitions=3)
# print(individual_means)
#
# yy = individual_means["Book-Rating"].value_counts(normalize=True).rename("Percentage").compute()
# yy = pd.DataFrame(yy).reset_index(level=0)
#
# yy.rename(columns={"index": "Ratings"}, inplace=True)
# print(yy)
# sns.catplot(x="Ratings", y="Percentage", kind="bar", data=yy)
