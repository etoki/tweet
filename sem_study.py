import semopy as sem
from semopy import Model
from semopy.examples import political_democracy
import pandas as pd

data = pd.read_csv("csv/dt_all.csv")
data = data.drop("ID", axis=1) 
data.columns = ['y1', 'y2', 'y3', 'y4', 'y5', 'x1', 'x2', 'x3', 'x4', 'x5']

mod = """
        f1 =~ y1 + y2 + y3 + y4 + y5
        f2 =~ x1 + x2 + x3 + x4 + x5
        f2 ~ f1
      """
mod = sem.Model(mod)
res = mod.fit(data=data, obj='MLW')

# inspect = mod.inspect()
inspect = sem.Model.inspect(mod, std_est=True)
# print(inspect)

stats = sem.calc_stats(mod)
# print(stats.T)

g = sem.semplot(mod, "sem_studysapuri.png", plot_covs=True, std_ests=True, show=True)

