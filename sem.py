import semopy as sem
from semopy import Model
from semopy.examples import political_democracy

data = political_democracy.get_data()
# print(data)

desc = political_democracy.get_model()
# print(desc)

# 学習器を用意
mod = Model(desc)

# 学習結果をresに代入する
res = mod.fit(data)
# print(res)

# 学習結果のパラメータ一覧を表示する
inspect = mod.inspect()
# print(inspect)

# 適合度を表示する
stats = sem.calc_stats(mod)
# print(stats.T)

g = sem.semplot(mod, "sample.png")

