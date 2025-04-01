#coding:utf-8
__author__ = "ila"
import base64, copy, logging, os, sys, time, xlrd, json, datetime, configparser
from django.http import JsonResponse
from django.apps import apps
import numbers
from django.db.models.aggregates import Count,Sum
from django.db.models import Case, When, IntegerField, F
from django.forms import model_to_dict
import requests
from util.CustomJSONEncoder import CustomJsonEncoder
from .models import hangqinginfoforecast
from util.codes import *
from util.auth import Auth
from util.common import Common
import util.message as mes
from django.db import connection
import random
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from django.db.models import Q
from util.baidubce_api import BaiDuBce
from .config_model import config
import pandas as pd

import joblib
import pymysql
import numpy as np
import matplotlib
matplotlib.use('Agg')  # 在导入pyplot之前设置
from matplotlib import pyplot as plt
from util.configread import config_read
import os
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
pd.options.mode.chained_assignment = None  # default='warn'

#获取当前文件路径的根目录
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dbtype, host, port, user, passwd, dbName, charset,hasHadoop = config_read(os.path.join(parent_directory,"config.ini"))
#MySQL连接配置
mysql_config = {
    'host': host,
    'user':user,
    'password': passwd,
    'database': dbName,
    'port':port
}
# 定义函数创建时间序列数据集
def create_dataset(data, time_step=1):
    X, Y = [], []
    for i in range(len(data) - time_step - 1):
        a = data[i:(i + time_step), :]
        X.append(a)
        Y.append(data[i + time_step, :])
    return np.array(X), np.array(Y)
def hangqinginfoforecast_forecast(request):
    if request.method in ["POST", "GET"]:
        msg = {'code': normal_code, "msg": mes.normal_code}
        #1.获取数据集
        connection = pymysql.connect(**mysql_config)
        query = "SELECT shijian, jiage,product FROM hangqinginfo ORDER BY shijian ASC"
        #2.处理缺失值
        data = pd.read_sql(query, connection).dropna()
        #分组
        grouped = data.groupby(['product'])
        for groupType, group in grouped:
            # 转换日期格式为datetime
            date_format = group['shijian'].iloc[0]
            if isinstance(date_format, (datetime.date, datetime.datetime)):
                date_format=''
            elif "年" in date_format and "月" in date_format and "日" in date_format:
                date_format='%Y年%m月%d日'
            elif "年" in date_format and "月" in date_format:
                date_format='%Y年%m月'
            elif "年" in date_format:
                date_format='%Y年'
            else:
                date_format=''
            if date_format=="" or date_format==None:
                group['shijian'] = pd.to_datetime(group['shijian'])
            else:
                group['shijian'] = pd.to_datetime(group['shijian'], format=date_format)
            group.set_index('shijian', inplace=True)
            #只选择需要的列
            group = group[[
                'jiage',
            ]]
            #归一化处理（为了LSTM的训练）
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(group)
             #设置时间步长
            time_step = int(len(group)/10)# 使用过去30的数据
            if time_step>30:
                time_step=30
            if time_step<=0:
                time_step=1
            X, y = create_dataset(scaled_data, time_step)
            #划分训练集和测试集
            train_size = int(len(X) * 0.8)  # 80%的数据用于训练
            X_train, X_test = X[:train_size], X[train_size:]
            y_train, y_test = y[:train_size], y[train_size:]
            # 查看训练数据集的形状
            print(f'X_train shape: {X_train.shape}, y_train shape: {y_train.shape}')
            # 创建 LSTM 模型
            try:
                model = Sequential()
                model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
                model.add(Dropout(0.2))  # 防止过拟合
                model.add(LSTM(50, return_sequences=False))
                model.add(Dropout(0.2))
                model.add(Dense(len(group.columns), activation='relu'))  # 输出层，预测
                #编译模型
                model.compile(optimizer='adam', loss='mean_squared_error')
                #训练模型
                model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=1)
            except:
                continue
            #进行预测
            train_predict = model.predict(X_train)
            test_predict = model.predict(X_test)
            #将预测结果反归一化
            train_predict = scaler.inverse_transform(train_predict)
            test_predict = scaler.inverse_transform(test_predict)
            #绘制预测结果
            plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体 SimHei
            plt.rcParams['axes.unicode_minus'] = False  # 解决负号 '-' 显示为方块的问题
            plt.figure(figsize=(12, 6),dpi=80)
            plt.plot(group.index[:len(train_predict)], train_predict[:, 1 -1], label='训练jiage预测',
                     color='blue')
            plt.plot(group.index[len(train_predict) + time_step + 1:], test_predict[:, 1 -1],
                     label='测试jiage预测', color='red')
            plt.plot(group.index, group['jiage'], label='实际jiage', color='green')
            plt.title(f'{groupType}_jiage预测')
            plt.xlabel('Date')
            plt.ylabel('jiage')
            plt.legend()
            plt.savefig(f'{groupType}_jiage_prediction.png')
            plt.clf()
            #准备未来7的输入数据
            last_data_days = scaled_data[-time_step:] #取最后time_step的数据
            future_predictions = []

            for _ in range(7):  # 预测未来7
              last_data_days = last_data_days.reshape((1, time_step, len(group.columns)))  # 重塑数据
              prediction = model.predict(last_data_days)
              future_predictions.append(prediction[0])
              last_data_days = np.append(last_data_days[:, 1:, :], [prediction], axis=1)  # 更新输入数据

            #转换为原始数据
            future_predictions = scaler.inverse_transform(future_predictions)
            #获取当前日期
            last_date = group.index[-1]  # 数据集中最后一个日期
            future_dates = [last_date + datetime.timedelta(days=i) for i in range(1, 7+1)]  # 生成未来7日的日期
            df = pd.DataFrame(columns=[
                'shijian',
                'jiage',
            ])
            df['shijian'] = future_dates
            df['jiage'] = future_predictions[:, 1 -1]
            df['product']=groupType
            df['jiage'] = df['jiage'].astype(float)
            df['jiage']=np.round(df['jiage'], 2)
            #9.创建数据库连接,将DataFrame 插入数据库
            connection_string = f"mysql+pymysql://{mysql_config['user']}:{mysql_config['password']}@{mysql_config['host']}:{mysql_config['port']}/{mysql_config['database']}"
            engine = create_engine(connection_string)
            try:
                df.to_sql('hangqinginfoforecast', con=engine, if_exists='append', index=False)
                print("数据更新成功！")
            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                engine.dispose()  # 关闭数据库连接
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def hangqinginfoforecast_register(request):
    if request.method in ["POST", "GET"]:
        msg = {'code': normal_code, "msg": mes.normal_code}
        req_dict = request.session.get("req_dict")


        error = hangqinginfoforecast.createbyreq(hangqinginfoforecast, hangqinginfoforecast, req_dict)
        if error is Exception:
            msg['code'] = crud_error_code
            msg['msg'] = "用户已存在,请勿重复注册!"
        else:
            msg['data'] = error
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def hangqinginfoforecast_login(request):
    if request.method in ["POST", "GET"]:
        msg = {'code': normal_code, "msg": mes.normal_code}
        req_dict = request.session.get("req_dict")
        datas = hangqinginfoforecast.getbyparams(hangqinginfoforecast, hangqinginfoforecast, req_dict)
        if not datas:
            msg['code'] = password_error_code
            msg['msg'] = mes.password_error_code
            return JsonResponse(msg, encoder=CustomJsonEncoder)

        try:
            __sfsh__= hangqinginfoforecast.__sfsh__
        except:
            __sfsh__=None

        if  __sfsh__=='是':
            if datas[0].get('sfsh')!='是':
                msg['code']=other_code
                msg['msg'] = "账号已锁定，请联系管理员审核!"
                return JsonResponse(msg, encoder=CustomJsonEncoder)
                
        req_dict['id'] = datas[0].get('id')


        return Auth.authenticate(Auth, hangqinginfoforecast, req_dict)


def hangqinginfoforecast_logout(request):
    if request.method in ["POST", "GET"]:
        msg = {
            "msg": "登出成功",
            "code": 0
        }

        return JsonResponse(msg, encoder=CustomJsonEncoder)


def hangqinginfoforecast_resetPass(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code}

        req_dict = request.session.get("req_dict")

        columns=  hangqinginfoforecast.getallcolumn( hangqinginfoforecast, hangqinginfoforecast)

        try:
            __loginUserColumn__= hangqinginfoforecast.__loginUserColumn__
        except:
            __loginUserColumn__=None
        username=req_dict.get(list(req_dict.keys())[0])
        if __loginUserColumn__:
            username_str=__loginUserColumn__
        else:
            username_str=username
        if 'mima' in columns:
            password_str='mima'
        else:
            password_str='password'

        init_pwd = '123456'
        recordsParam = {}
        recordsParam[username_str] = req_dict.get("username")
        records=hangqinginfoforecast.getbyparams(hangqinginfoforecast, hangqinginfoforecast, recordsParam)
        if len(records)<1:
            msg['code'] = 400
            msg['msg'] = '用户不存在'
            return JsonResponse(msg, encoder=CustomJsonEncoder)

        eval('''hangqinginfoforecast.objects.filter({}='{}').update({}='{}')'''.format(username_str,username,password_str,init_pwd))
        
        return JsonResponse(msg, encoder=CustomJsonEncoder)



def hangqinginfoforecast_session(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code,"msg": mes.normal_code, "data": {}}

        req_dict={"id":request.session.get('params').get("id")}
        msg['data']  = hangqinginfoforecast.getbyparams(hangqinginfoforecast, hangqinginfoforecast, req_dict)[0]

        return JsonResponse(msg, encoder=CustomJsonEncoder)


def hangqinginfoforecast_default(request):

    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code,"msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        req_dict.update({"isdefault":"是"})
        data=hangqinginfoforecast.getbyparams(hangqinginfoforecast, hangqinginfoforecast, req_dict)
        if len(data)>0:
            msg['data']  = data[0]
        else:
            msg['data']  = {}
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def hangqinginfoforecast_page(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = request.session.get("req_dict")

        global hangqinginfoforecast

        #获取全部列名
        columns=  hangqinginfoforecast.getallcolumn( hangqinginfoforecast, hangqinginfoforecast)

        if "vipread" in req_dict and "vipread" not in columns:
          del req_dict["vipread"]

        #当前登录用户所在表
        tablename = request.session.get("tablename")

        '''__authSeparate__此属性为真，params添加userid，后台只查询个人数据'''
        try:
            __authSeparate__=hangqinginfoforecast.__authSeparate__
        except:
            __authSeparate__=None

        if __authSeparate__=="是":
            tablename=request.session.get("tablename")
            if tablename!="users" and 'userid' in columns and 'userid' not in req_dict:
                try:
                    req_dict['userid']=request.session.get("params").get("id")
                except:
                    pass

        #当项目属性hasMessage为”是”，生成系统自动生成留言板的表messages，同时该表的表属性hasMessage也被设置为”是”,字段包括userid（用户id），username(用户名)，content（留言内容），reply（回复）
        #接口page需要区分权限，普通用户查看自己的留言和回复记录，管理员查看所有的留言和回复记录
        try:
            __hasMessage__=hangqinginfoforecast.__hasMessage__
        except:
            __hasMessage__=None
        if  __hasMessage__=="是":
            tablename=request.session.get("tablename")
            if tablename!="users":
                req_dict["userid"]=request.session.get("params").get("id")

        # 判断当前表的表属性isAdmin,为真则是管理员表
        # 当表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
        __isAdmin__ = None

        allModels = apps.get_app_config('main').get_models()
        for m in allModels:
            if m.__tablename__==tablename:

                try:
                    __isAdmin__ = m.__isAdmin__
                except:
                    __isAdmin__ = None
                break

        # 当前表也是有管理员权限的表
        if  __isAdmin__ == "是" and 'hangqinginfoforecast' != 'forum' :
            if req_dict.get("userid") and 'hangqinginfoforecast' != 'chat' and 'hangqinginfoforecast' != 'examrecord':
                del req_dict["userid"]
        else:
            if tablename!="users" and tablename!="jdfnl" and 'hangqinginfoforecast'[:7]!='discuss' and "userid" in hangqinginfoforecast.getallcolumn(hangqinginfoforecast,hangqinginfoforecast):
                req_dict["userid"] = request.session.get("params").get("id")

        #当列属性authTable有值(某个用户表)[该列的列名必须和该用户表的登陆字段名一致]，则对应的表有个隐藏属性authTable为”是”，那么该用户查看该表信息时，只能查看自己的
        try:
            __authTables__=hangqinginfoforecast.__authTables__
        except:
            __authTables__=None

        if __authTables__!=None and  __authTables__!={} and __isAdmin__ == "是":
            for authColumn,authTable in __authTables__.items():
                if authTable==tablename:
                    params = request.session.get("params")
                    req_dict[authColumn]=params.get(authColumn)
                    username=params.get(authColumn)
                    break
        q = Q()

        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  =hangqinginfoforecast.page(hangqinginfoforecast, hangqinginfoforecast, req_dict, request, q)
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def hangqinginfoforecast_autoSort(request):
    '''
    ．智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
主要信息列表（如商品列表，新闻列表）中使用，显示最近点击的或最新添加的5条记录就行
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = request.session.get("req_dict")
        if "clicknum"  in hangqinginfoforecast.getallcolumn(hangqinginfoforecast,hangqinginfoforecast):
            req_dict['sort']='clicknum'
        elif "browseduration"  in hangqinginfoforecast.getallcolumn(hangqinginfoforecast,hangqinginfoforecast):
            req_dict['sort']='browseduration'
        else:
            req_dict['sort']='clicktime'
        req_dict['order']='desc'
        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  = hangqinginfoforecast.page(hangqinginfoforecast,hangqinginfoforecast, req_dict)

        return JsonResponse(msg, encoder=CustomJsonEncoder)

#分类列表
def hangqinginfoforecast_lists(request):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":[]}
        msg['data'],_,_,_,_  = hangqinginfoforecast.page(hangqinginfoforecast, hangqinginfoforecast, {})
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def hangqinginfoforecast_query(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        try:
            query_result = hangqinginfoforecast.objects.filter(**request.session.get("req_dict")).values()
            msg['data'] = query_result[0]
        except Exception as e:

            msg['code'] = crud_error_code
            msg['msg'] = f"发生错误：{e}"
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def hangqinginfoforecast_list(request):
    '''
    前台分页
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = request.session.get("req_dict")
        #获取全部列名
        columns=  hangqinginfoforecast.getallcolumn( hangqinginfoforecast, hangqinginfoforecast)
        if "vipread" in req_dict and "vipread" not in columns:
          del req_dict["vipread"]
        #表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
        try:
            __foreEndList__=hangqinginfoforecast.__foreEndList__
        except:
            __foreEndList__=None
        try:
            __foreEndListAuth__=hangqinginfoforecast.__foreEndListAuth__
        except:
            __foreEndListAuth__=None

        #authSeparate
        try:
            __authSeparate__=hangqinginfoforecast.__authSeparate__
        except:
            __authSeparate__=None

        if __foreEndListAuth__ =="是" and __authSeparate__=="是":
            tablename=request.session.get("tablename")
            if tablename!="users" and request.session.get("params") is not None:
                req_dict['userid']=request.session.get("params").get("id")

        tablename = request.session.get("tablename")
        if tablename == "users" and req_dict.get("userid") != None:#判断是否存在userid列名
            del req_dict["userid"]
        else:
            __isAdmin__ = None

            allModels = apps.get_app_config('main').get_models()
            for m in allModels:
                if m.__tablename__==tablename:

                    try:
                        __isAdmin__ = m.__isAdmin__
                    except:
                        __isAdmin__ = None
                    break

            if __isAdmin__ == "是":
                if req_dict.get("userid"):
                    # del req_dict["userid"]
                    pass
            else:
                #非管理员权限的表,判断当前表字段名是否有userid
                if "userid" in columns:
                    try:
                        pass
                    except:
                        pass
        #当列属性authTable有值(某个用户表)[该列的列名必须和该用户表的登陆字段名一致]，则对应的表有个隐藏属性authTable为”是”，那么该用户查看该表信息时，只能查看自己的
        try:
            __authTables__=hangqinginfoforecast.__authTables__
        except:
            __authTables__=None

        if __authTables__!=None and  __authTables__!={} and __foreEndListAuth__=="是":
            for authColumn,authTable in __authTables__.items():
                if authTable==tablename:
                    try:
                        del req_dict['userid']
                    except:
                        pass
                    params = request.session.get("params")
                    req_dict[authColumn]=params.get(authColumn)
                    username=params.get(authColumn)
                    break
        
        if hangqinginfoforecast.__tablename__[:7]=="discuss":
            try:
                del req_dict['userid']
            except:
                pass


        q = Q()
        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  = hangqinginfoforecast.page(hangqinginfoforecast, hangqinginfoforecast, req_dict, request, q)
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def hangqinginfoforecast_save(request):
    '''
    后台新增
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        if 'clicktime' in req_dict.keys():
            del req_dict['clicktime']
        tablename=request.session.get("tablename")
        __isAdmin__ = None
        allModels = apps.get_app_config('main').get_models()
        for m in allModels:
            if m.__tablename__==tablename:

                try:
                    __isAdmin__ = m.__isAdmin__
                except:
                    __isAdmin__ = None
                break

        #获取全部列名
        columns=  hangqinginfoforecast.getallcolumn( hangqinginfoforecast, hangqinginfoforecast)
        if tablename!='users' and req_dict.get("userid")!=None and 'userid' in columns  and __isAdmin__!='是':
            params=request.session.get("params")
            req_dict['userid']=params.get('id')


        if 'addtime' in req_dict.keys():
            del req_dict['addtime']

        idOrErr= hangqinginfoforecast.createbyreq(hangqinginfoforecast,hangqinginfoforecast, req_dict)
        if idOrErr is Exception:
            msg['code'] = crud_error_code
            msg['msg'] = idOrErr
        else:
            msg['data'] = idOrErr

        return JsonResponse(msg, encoder=CustomJsonEncoder)

def hangqinginfoforecast_add(request):
    '''
    前台新增
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        tablename=request.session.get("tablename")

        #获取全部列名
        columns=  hangqinginfoforecast.getallcolumn( hangqinginfoforecast, hangqinginfoforecast)
        try:
            __authSeparate__=hangqinginfoforecast.__authSeparate__
        except:
            __authSeparate__=None

        if __authSeparate__=="是":
            tablename=request.session.get("tablename")
            if tablename!="users" and 'userid' in columns:
                try:
                    req_dict['userid']=request.session.get("params").get("id")
                except:
                    pass

        try:
            __foreEndListAuth__=hangqinginfoforecast.__foreEndListAuth__
        except:
            __foreEndListAuth__=None

        if __foreEndListAuth__ and __foreEndListAuth__!="否":
            tablename=request.session.get("tablename")
            if tablename!="users":
                req_dict['userid']=request.session.get("params").get("id")


        if 'addtime' in req_dict.keys():
            del req_dict['addtime']
        error= hangqinginfoforecast.createbyreq(hangqinginfoforecast,hangqinginfoforecast, req_dict)
        if error is Exception:
            msg['code'] = crud_error_code
            msg['msg'] = error
        else:
            msg['data'] = error
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def hangqinginfoforecast_thumbsup(request,id_):
    '''
     点赞：表属性thumbsUp[是/否]，刷表新增thumbsupnum赞和crazilynum踩字段，
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        id_=int(id_)
        type_=int(req_dict.get("type",0))
        rets=hangqinginfoforecast.getbyid(hangqinginfoforecast,hangqinginfoforecast,id_)

        update_dict={
        "id":id_,
        }
        if type_==1:#赞
            update_dict["thumbsupnum"]=int(rets[0].get('thumbsupnum'))+1
        elif type_==2:#踩
            update_dict["crazilynum"]=int(rets[0].get('crazilynum'))+1
        error = hangqinginfoforecast.updatebyparams(hangqinginfoforecast,hangqinginfoforecast, update_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg, encoder=CustomJsonEncoder)


def hangqinginfoforecast_info(request,id_):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}

        data = hangqinginfoforecast.getbyid(hangqinginfoforecast,hangqinginfoforecast, int(id_))
        if len(data)>0:
            msg['data']=data[0]
            if msg['data'].__contains__("reversetime"):
                if isinstance(msg['data']['reversetime'], datetime.datetime):
                    msg['data']['reversetime'] = msg['data']['reversetime'].strftime("%Y-%m-%d %H:%M:%S")
                else:
                    if msg['data']['reversetime'] != None:
                        reversetime = datetime.datetime.strptime(msg['data']['reversetime'], '%Y-%m-%d %H:%M:%S')
                        msg['data']['reversetime'] = reversetime.strftime("%Y-%m-%d %H:%M:%S")

        #浏览点击次数
        try:
            __browseClick__= hangqinginfoforecast.__browseClick__
        except:
            __browseClick__=None

        if __browseClick__=="是"  and  "clicknum"  in hangqinginfoforecast.getallcolumn(hangqinginfoforecast,hangqinginfoforecast):
            try:
                clicknum=int(data[0].get("clicknum",0))+1
            except:
                clicknum=0+1
            click_dict={"id":int(id_),"clicknum":clicknum,"clicktime":datetime.datetime.now()}
            ret=hangqinginfoforecast.updatebyparams(hangqinginfoforecast,hangqinginfoforecast,click_dict)
            if ret!=None:
                msg['code'] = crud_error_code
                msg['msg'] = ret
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def hangqinginfoforecast_detail(request,id_):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}

        data =hangqinginfoforecast.getbyid(hangqinginfoforecast,hangqinginfoforecast, int(id_))
        if len(data)>0:
            msg['data']=data[0]
            if msg['data'].__contains__("reversetime"):
                if isinstance(msg['data']['reversetime'], datetime.datetime):
                    msg['data']['reversetime'] = msg['data']['reversetime'].strftime("%Y-%m-%d %H:%M:%S")
                else:
                    if msg['data']['reversetime'] != None:
                        reversetime = datetime.datetime.strptime(msg['data']['reversetime'], '%Y-%m-%d %H:%M:%S')
                        msg['data']['reversetime'] = reversetime.strftime("%Y-%m-%d %H:%M:%S")

        #浏览点击次数
        try:
            __browseClick__= hangqinginfoforecast.__browseClick__
        except:
            __browseClick__=None

        if __browseClick__=="是"   and  "clicknum"  in hangqinginfoforecast.getallcolumn(hangqinginfoforecast,hangqinginfoforecast):
            try:
                clicknum=int(data[0].get("clicknum",0))+1
            except:
                clicknum=0+1
            click_dict={"id":int(id_),"clicknum":clicknum,"clicktime":datetime.datetime.now()}

            ret=hangqinginfoforecast.updatebyparams(hangqinginfoforecast,hangqinginfoforecast,click_dict)
            if ret!=None:
                msg['code'] = crud_error_code
                msg['msg'] = ret
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def hangqinginfoforecast_update(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        if 'clicktime' in req_dict.keys() and req_dict['clicktime']=="None":
            del req_dict['clicktime']
        if req_dict.get("mima") and "mima" not in hangqinginfoforecast.getallcolumn(hangqinginfoforecast,hangqinginfoforecast) :
            del req_dict["mima"]
        if req_dict.get("password") and "password" not in hangqinginfoforecast.getallcolumn(hangqinginfoforecast,hangqinginfoforecast) :
            del req_dict["password"]
        try:
            del req_dict["clicknum"]
        except:
            pass


        error = hangqinginfoforecast.updatebyparams(hangqinginfoforecast, hangqinginfoforecast, req_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error

        return JsonResponse(msg)


def hangqinginfoforecast_delete(request):
    '''
    批量删除
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")

        error=hangqinginfoforecast.deletes(hangqinginfoforecast,
            hangqinginfoforecast,
             req_dict.get("ids")
        )
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)


def hangqinginfoforecast_vote(request,id_):
    '''
    浏览点击次数（表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1）
统计商品或新闻的点击次数；提供新闻的投票功能
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code}


        data= hangqinginfoforecast.getbyid(hangqinginfoforecast, hangqinginfoforecast, int(id_))
        for i in data:
            votenum=i.get('votenum')
            if votenum!=None:
                params={"id":int(id_),"votenum":votenum+1}
                error=hangqinginfoforecast.updatebyparams(hangqinginfoforecast,hangqinginfoforecast,params)
                if error!=None:
                    msg['code'] = crud_error_code
                    msg['msg'] = error
        return JsonResponse(msg)

def hangqinginfoforecast_importExcel(request):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": {}}

        excel_file = request.FILES.get("file", "")
        file_type = excel_file.name.split('.')[1]
        
        if file_type in ['xlsx', 'xls']:
            data = xlrd.open_workbook(filename=None, file_contents=excel_file.read())
            table = data.sheets()[0]
            rows = table.nrows
            
            try:
                for row in range(1, rows):
                    row_values = table.row_values(row)
                    req_dict = {}
                    hangqinginfoforecast.createbyreq(hangqinginfoforecast, hangqinginfoforecast, req_dict)
                    
            except:
                pass
                
        else:
            msg = {
                "msg": "文件类型错误",
                "code": 500
            }
                
        return JsonResponse(msg)

def hangqinginfoforecast_autoSort2(request):
    return JsonResponse({"code": 0, "msg": '',  "data":{}})













