from django.http.response import Http404
from django.shortcuts import render
from django.http import HttpResponse

from sklearn import svm
from sklearn.model_selection import train_test_split
import pandas as pd
import pandas_datareader.data as pdr
from pandas_datareader.stooq import StooqDailyReader
from datetime import datetime, timedelta


def get_predict_data(request):
  try:
    #株価取得範囲を設定
    td = timedelta(days=100)
    start = datetime.now() - td
    end = datetime.now()
    #銘柄コード
    code = request.GET['code']
    stock = f'{code}.jp'
    #株価取得
    df = StooqDailyReader(stock, start=start, end=end)
    price_df = df.read().sort_index()
    price_df.index = price_df.index.strftime('%Y/%m/%d')

    stock_data = price_df.copy()
    stock_data = stock_data['Close']
    # 前日までのN日連続の株価のデータ
    successive_data = []
    N_BATCH = 4 # 一まとまりのデータ数
    for i in range(N_BATCH, len(stock_data)):
        ratio_batch = []
        for j in range(N_BATCH, 1, -1):
          ratio_batch.append(stock_data[i-j])
        successive_data.append(ratio_batch)
    answers = list(stock_data[N_BATCH:])

    x_train, x_test, t_train, t_test = \
      train_test_split(successive_data, answers, shuffle=False)  # シャッフルしない
    clf = svm.SVR()  # サポートベクターマシーン
    clf.fit(x_train, t_train)  # 訓練
    y_pred = clf.predict(x_test)  # テスト用データで予測
    return HttpResponse(int(y_pred[-1]))
  except Exception as e:
    return HttpResponse(e)


  return stock_data


def get_stock_data(request):
  try:
    #株価取得範囲を設定
    td = timedelta(days=365)
    start = datetime.now() - td
    end = datetime.now()
    #銘柄コード
    code = request.GET['code']
    stock = f'{code}.jp'
    #株価取得
    df = StooqDailyReader(stock, start=start, end=end)
    price_df = df.read().sort_index()
    price_df.index = price_df.index.strftime('%Y/%m/%d')
    price_json = price_df.to_json()
    return HttpResponse(price_json)
  except Exception as e:
    return HttpResponse(e)
