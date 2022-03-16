import dask.dataframe as dd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

books = dd.read_csv("data\\BX-Book-Ratings.txt", encoding="latin1", delimiter=";", dtype={"ISBN": "string"})
print(type(books))
means = books["Book-Rating"].value_counts(normalize=True).rename("Percentage").compute()
print(type(means))
#means = means.mul(100).rename("Percent").reset_index()
#means = means["Book-Rating"].value_counts(normalize=True).reset_index().compute()
x=pd.DataFrame(means).reset_index(level=0)
x.rename(columns={"index": "Ratings"}, inplace=True)
print(x)
#
sns.catplot(x="Ratings", y="Percentage", kind="bar", data=x)
plt.show()