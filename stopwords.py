from ja_stopword_remover.remover import StopwordRemover
import pprint

# 多田なの(@ohta_nano)さんの詩です。
text_list = [[ "僕", "たち", "は", "プラネタリウム", "に", "立て籠もり", "夜明け", "の", "シーン", "だけ", "繰り返す",],
    [ "桜", "って", "「", "さくら", "」", "って", "読む", "って", "あなた", "から", "教えて", "もらう", "人", "に", "なりたい",],]

stopwordRemover = StopwordRemover()

stopwordRemover.choose_parts(
    demonstrative=True,
    symbol=True,
    verb=False,
    one_character=True,
    postpositional_particle=True,
    slothlib=True,
    auxiliary_verb=True,
    adjective=False
)

text_list_result = stopwordRemover.remove(text_list)
pprint.pprint(text_list_result)

