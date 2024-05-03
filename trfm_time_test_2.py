import pandas as pd
import numpy as np
import torch
from iTransformer import iTransformer
import optuna

# データの読み込みと前処理
def load_and_preprocess_data():
    # 機械受注データの読み込み
    df_machinary_order = pd.read_csv('csv/machinary_order_data.csv')
    df_stock = pd.read_csv('csv/stockdata.csv')

    # 対数変換後の階差を取る
    df_machinary_order['産業用ロボット対数化'] = np.log10(df_machinary_order['産業用ロボット']).diff().fillna(0)
    df_stock['日経平均株価対数化'] = np.log10(df_stock['日経平均株価']).diff().fillna(0)

    return df_machinary_order, df_stock

# データをモデルに適合する形に変換
def format_data_for_model(df1, df2, lookback=12):
    combined = pd.concat([df1, df2], axis=1).dropna()
    output = []
    for i in range(len(combined) - lookback):
        output.append(combined.iloc[i:i+lookback].values)
    return np.array(output)

# モデルの訓練
def train_model(data):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # print(device)

    model = iTransformer(
        num_variates=2, lookback_len=12, dim=128, depth=6, heads=8, dim_head=32,
        pred_length=1, num_tokens_per_variate=2
    ).to(device)
    # print(model)

    # データをテンソルに変換
    data_tensor = torch.tensor(data, dtype=torch.float32).to(device)
    # print(data_tensor)

    # ダミーの訓練プロセスを示します
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = torch.nn.MSELoss()
    # print(optimizer)
    # print(criterion)

    model.train()

    for epoch in range(100):  # エポック数は調整可能
        optimizer.zero_grad()
        output = model(data_tensor[:, :-1, :])  # 最後の時点を除外
        print(output)
        loss = criterion(output, data_tensor[:, -1, :])  # 最後の時点を予測値と比較
        print(loss)
        loss.backward()
        optimizer.step()
        print(f'Epoch {epoch+1}, Loss: {loss.item()}')

    # return model

# モデルを用いた予測
def make_predictions(model, data):
    model.eval()
    data_tensor = torch.tensor(data, dtype=torch.float32)
    with torch.no_grad():
        predictions = model(data_tensor)
    return predictions.numpy()

# メイン実行部
df_machinary_order, df_stock = load_and_preprocess_data()
formatted_data = format_data_for_model(df_machinary_order['産業用ロボット対数化'], df_stock['日経平均株価対数化'])
model = train_model(formatted_data)

# predictions = make_predictions(model, formatted_data)

# print(predictions)

"""
PS C:\Users\USER\Desktop\python> python .\trfm_time_test_2.py
0      0.000000
1     -0.053338
2      0.061319
3     -0.081040
4     -0.056338
         ...
216   -0.019662
217   -0.082794
218    0.004572
219   -0.043979
220   -0.005308
Name: 産業用ロボット対数化, Length: 221, dtype: float64
0      0.000000
1      0.010434
2      0.011681
3      0.011673
4      0.018365
         ...
216    0.012442
217    0.029545
218    0.031207
219   -0.000220
220   -0.007299
Name: 日経平均株価対数化, Length: 221, dtype: float64
PS C:\Users\USER\Desktop\python> 
PS C:\Users\USER\Desktop\python>
PS C:\Users\USER\Desktop\python> python .\trfm_time_test_2.py
     産業用ロボット対数化  日経平均株価対数化
0      0.000000   0.000000
1     -0.053338   0.010434
2      0.061319   0.011681
3     -0.081040   0.011673
4     -0.056338   0.018365
..          ...        ...
216   -0.019662   0.012442
217   -0.082794   0.029545
218    0.004572   0.031207
219   -0.043979  -0.000220
220   -0.005308  -0.007299

[221 rows x 2 columns]
PS C:\Users\USER\Desktop\python> 
PS C:\Users\USER\Desktop\python> 
PS C:\Users\USER\Desktop\python> python .\trfm_time_test_2.py
[[[ 0.          0.        ]
  [-0.05333808  0.01043386]
  [ 0.06131929  0.01168113]
  ...
  [ 0.03164656  0.01427545]
  [ 0.00158949 -0.01174898]
  [ 0.02164185  0.02230981]]

 [[-0.05333808  0.01043386]
  [ 0.06131929  0.01168113]
  [-0.08104021  0.01167344]
  ...
  [ 0.00158949 -0.01174898]
  [ 0.02164185  0.02230981]
  [ 0.06567657 -0.0039236 ]]

 [[ 0.06131929  0.01168113]
  [-0.08104021  0.01167344]
  [-0.05633774  0.01836538]
  ...
  [ 0.02164185  0.02230981]
  [ 0.06567657 -0.0039236 ]
  [-0.00680238 -0.03863142]]

 ...

 [[ 0.05759959 -0.01435177]
  [-0.01132623  0.022581  ]
  [-0.0080983   0.00450498]
  ...
  [ 0.00995695  0.00932883]
  [-0.01966242  0.01244182]
  [-0.08279448  0.02954535]]

 [[-0.01132623  0.022581  ]
  [-0.0080983   0.00450498]
  [ 0.0236504  -0.03465214]
  ...
  [-0.01966242  0.01244182]
  [-0.08279448  0.02954535]
  [ 0.00457161  0.03120659]]

 [[-0.0080983   0.00450498]
  [ 0.0236504  -0.03465214]
  [-0.07864821  0.02678846]
  ...
  [-0.08279448  0.02954535]
  [ 0.00457161  0.03120659]
  [-0.04397942 -0.00022015]]]
PS C:\Users\USER\Desktop\python> 
PS C:\Users\USER\Desktop\python> 
PS C:\Users\USER\Desktop\python> python .\trfm_time_test_2.py
cpu
PS C:\Users\USER\Desktop\python> 
PS C:\Users\USER\Desktop\python>
PS C:\Users\USER\Desktop\python> python .\trfm_time_test_2.py
cpu
iTransformer(
  (layers): ModuleList(
    (0-5): 6 x ModuleList(
      (0): Attention(
        (to_qkv): Sequential(
          (0): Linear(in_features=128, out_features=768, bias=False)
          (1): Rearrange('b n (qkv h d) -> qkv b h n d', qkv=3, h=8)
        )
        (to_v_gates): Sequential(
          (0): Linear(in_features=128, out_features=256, bias=False)
          (1): SiLU()
          (2): Rearrange('b n (h d) -> b h n d', h=8)
        )
        (attend): Attend(
          (attn_dropout): Dropout(p=0.0, inplace=False)
        )
        (to_out): Sequential(
          (0): Rearrange('b h n d -> b n (h d)')
          (1): Linear(in_features=256, out_features=128, bias=False)
          (2): Dropout(p=0.0, inplace=False)
        )
      )
      (1): LayerNorm((128,), eps=1e-05, elementwise_affine=True)
      (2): Sequential(
        (0): Linear(in_features=128, out_features=682, bias=True)
        (1): GEGLU()
        (2): Dropout(p=0.0, inplace=False)
        (3): Linear(in_features=341, out_features=128, bias=True)
      )
      (3): LayerNorm((128,), eps=1e-05, elementwise_affine=True)
    )
  )
  (mlp_in): Sequential(
    (0): Linear(in_features=12, out_features=256, bias=True)
    (1): Rearrange('b v (n d) -> b (v n) d', n=2)
    (2): LayerNorm((128,), eps=1e-05, elementwise_affine=True)
  )
  (pred_heads): ModuleList(
    (0): Sequential(
      (0): Rearrange('b (v n) d -> b v (n d)', n=2)
      (1): Linear(in_features=256, out_features=1, bias=True)
      (2): Rearrange('b v n -> b n v')
    )
  )
)
PS C:\Users\USER\Desktop\python> 
PS C:\Users\USER\Desktop\python>
PS C:\Users\USER\Desktop\python> python .\trfm_time_test_2.py
tensor([[[ 0.0000,  0.0000],
         [-0.0533,  0.0104],
         [ 0.0613,  0.0117],
         ...,
         [ 0.0316,  0.0143],
         [ 0.0016, -0.0117],
         [ 0.0216,  0.0223]],

        [[-0.0533,  0.0104],
         [ 0.0613,  0.0117],
         [-0.0810,  0.0117],
         ...,
         [ 0.0016, -0.0117],
         [ 0.0216,  0.0223],
         [ 0.0657, -0.0039]],

        [[ 0.0613,  0.0117],
         [-0.0810,  0.0117],
         [-0.0563,  0.0184],
         ...,
         [ 0.0216,  0.0223],
         [ 0.0657, -0.0039],
         [-0.0068, -0.0386]],

        ...,

        [[ 0.0576, -0.0144],
         [-0.0113,  0.0226],
         [-0.0081,  0.0045],
         ...,
         [ 0.0100,  0.0093],
         [-0.0197,  0.0124],
         [-0.0828,  0.0295]],

        [[-0.0113,  0.0226],
         [-0.0081,  0.0045],
         [ 0.0237, -0.0347],
         ...,
         [-0.0197,  0.0124],
         [-0.0828,  0.0295],
         [ 0.0046,  0.0312]],

        [[-0.0081,  0.0045],
         [ 0.0237, -0.0347],
         [-0.0786,  0.0268],
         ...,
         [-0.0828,  0.0295],
         [ 0.0046,  0.0312],
         [-0.0440, -0.0002]]])
PS C:\Users\USER\Desktop\python> 
PS C:\Users\USER\Desktop\python> python .\trfm_time_test_2.py
Adam (
Parameter Group 0
    amsgrad: False
    betas: (0.9, 0.999)
    capturable: False
    differentiable: False
    eps: 1e-08
    foreach: None
    fused: None
    lr: 0.001
    maximize: False
    weight_decay: 0
)
MSELoss()
PS C:\Users\USER\Desktop\python> 
PS C:\Users\USER\Desktop\python> python .\trfm_time_test_2.py
PS C:\Users\USER\Desktop\python> 
PS C:\Users\USER\Desktop\python> python .\trfm_time_test_2.py
Traceback (most recent call last):
  File "C:\Users\USER\Desktop\python\trfm_time_test_2.py", line 73, in <module>
    model = train_model(formatted_data)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER\Desktop\python\trfm_time_test_2.py", line 52, in train_model
    output = model(data_tensor[:, :-1, :])  # 最後の時点を除外
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python312\Lib\site-packages\torch\nn\modules\module.py", line 1532, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python312\Lib\site-packages\torch\nn\modules\module.py", line 1541, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<@beartype(iTransformer.iTransformer.iTransformer.forward) at 0x17f5464aac0>", line 67, in forward
  File "C:\Python312\Lib\site-packages\iTransformer\iTransformer.py", line 165, in forward
    assert x.shape[1:] == (self.lookback_len, self.num_variates)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError
"""