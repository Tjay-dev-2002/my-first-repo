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
from .models import shuiguobaojia
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


def shuiguobaojia_register(request):
    if request.method in ["POST", "GET"]:
        msg = {'code': normal_code, "msg": mes.normal_code}
        req_dict = request.session.get("req_dict")


        error = shuiguobaojia.createbyreq(shuiguobaojia, shuiguobaojia, req_dict)
        if error is Exception:
            msg['code'] = crud_error_code
            msg['msg'] = "用户已存在,请勿重复注册!"
        else:
            msg['data'] = error
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def shuiguobaojia_login(request):
    if request.method in ["POST", "GET"]:
        msg = {'code': normal_code, "msg": mes.normal_code}
        req_dict = request.session.get("req_dict")
        datas = shuiguobaojia.getbyparams(shuiguobaojia, shuiguobaojia, req_dict)
        if not datas:
            msg['code'] = password_error_code
            msg['msg'] = mes.password_error_code
            return JsonResponse(msg, encoder=CustomJsonEncoder)

        try:
            __sfsh__= shuiguobaojia.__sfsh__
        except:
            __sfsh__=None

        if  __sfsh__=='是':
            if datas[0].get('sfsh')!='是':
                msg['code']=other_code
                msg['msg'] = "账号已锁定，请联系管理员审核!"
                return JsonResponse(msg, encoder=CustomJsonEncoder)
                
        req_dict['id'] = datas[0].get('id')


        return Auth.authenticate(Auth, shuiguobaojia, req_dict)


def shuiguobaojia_logout(request):
    if request.method in ["POST", "GET"]:
        msg = {
            "msg": "登出成功",
            "code": 0
        }

        return JsonResponse(msg, encoder=CustomJsonEncoder)


def shuiguobaojia_resetPass(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code}

        req_dict = request.session.get("req_dict")

        columns=  shuiguobaojia.getallcolumn( shuiguobaojia, shuiguobaojia)

        try:
            __loginUserColumn__= shuiguobaojia.__loginUserColumn__
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
        records=shuiguobaojia.getbyparams(shuiguobaojia, shuiguobaojia, recordsParam)
        if len(records)<1:
            msg['code'] = 400
            msg['msg'] = '用户不存在'
            return JsonResponse(msg, encoder=CustomJsonEncoder)

        eval('''shuiguobaojia.objects.filter({}='{}').update({}='{}')'''.format(username_str,username,password_str,init_pwd))
        
        return JsonResponse(msg, encoder=CustomJsonEncoder)



def shuiguobaojia_session(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code,"msg": mes.normal_code, "data": {}}

        req_dict={"id":request.session.get('params').get("id")}
        msg['data']  = shuiguobaojia.getbyparams(shuiguobaojia, shuiguobaojia, req_dict)[0]

        return JsonResponse(msg, encoder=CustomJsonEncoder)


def shuiguobaojia_default(request):

    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code,"msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        req_dict.update({"isdefault":"是"})
        data=shuiguobaojia.getbyparams(shuiguobaojia, shuiguobaojia, req_dict)
        if len(data)>0:
            msg['data']  = data[0]
        else:
            msg['data']  = {}
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def shuiguobaojia_page(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = request.session.get("req_dict")

        global shuiguobaojia

        #获取全部列名
        columns=  shuiguobaojia.getallcolumn( shuiguobaojia, shuiguobaojia)

        if "vipread" in req_dict and "vipread" not in columns:
          del req_dict["vipread"]

        #当前登录用户所在表
        tablename = request.session.get("tablename")

        '''__authSeparate__此属性为真，params添加userid，后台只查询个人数据'''
        try:
            __authSeparate__=shuiguobaojia.__authSeparate__
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
            __hasMessage__=shuiguobaojia.__hasMessage__
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
        if  __isAdmin__ == "是" and 'shuiguobaojia' != 'forum' :
            if req_dict.get("userid") and 'shuiguobaojia' != 'chat' and 'shuiguobaojia' != 'examrecord':
                del req_dict["userid"]
        else:
            if tablename!="users" and tablename!="jdfnl" and 'shuiguobaojia'[:7]!='discuss' and "userid" in shuiguobaojia.getallcolumn(shuiguobaojia,shuiguobaojia):
                req_dict["userid"] = request.session.get("params").get("id")

        #当列属性authTable有值(某个用户表)[该列的列名必须和该用户表的登陆字段名一致]，则对应的表有个隐藏属性authTable为”是”，那么该用户查看该表信息时，只能查看自己的
        try:
            __authTables__=shuiguobaojia.__authTables__
        except:
            __authTables__=None

        if __authTables__!=None and  __authTables__!={} and __isAdmin__ == "是":
            for authColumn,authTable in __authTables__.items():
                if authTable==tablename:
                    params = request.session.get("params")
                    req_dict[authColumn]=params.get(authColumn)
                    username=params.get(authColumn)
                    break
        if tablename == 'shangjia':
            from .models import shangjia
            req_dict['shangjiamingcheng'] = request.session.get("params").get(shangjia.__loginUserColumn__)
            if 'userid' in req_dict.keys():
                del req_dict["userid"]
        if tablename == 'gongyingshang':
            from .models import gongyingshang
            req_dict['gongyingshangmingcheng'] = request.session.get("params").get(gongyingshang.__loginUserColumn__)
            if 'userid' in req_dict.keys():
                del req_dict["userid"]
        q = Q()

        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  =shuiguobaojia.page(shuiguobaojia, shuiguobaojia, req_dict, request, q)
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def shuiguobaojia_autoSort(request):
    '''
    ．智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
主要信息列表（如商品列表，新闻列表）中使用，显示最近点击的或最新添加的5条记录就行
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = request.session.get("req_dict")
        if "clicknum"  in shuiguobaojia.getallcolumn(shuiguobaojia,shuiguobaojia):
            req_dict['sort']='clicknum'
        elif "browseduration"  in shuiguobaojia.getallcolumn(shuiguobaojia,shuiguobaojia):
            req_dict['sort']='browseduration'
        else:
            req_dict['sort']='clicktime'
        req_dict['order']='desc'
        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  = shuiguobaojia.page(shuiguobaojia,shuiguobaojia, req_dict)

        return JsonResponse(msg, encoder=CustomJsonEncoder)

#分类列表
def shuiguobaojia_lists(request):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":[]}
        msg['data'],_,_,_,_  = shuiguobaojia.page(shuiguobaojia, shuiguobaojia, {})
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def shuiguobaojia_query(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        try:
            query_result = shuiguobaojia.objects.filter(**request.session.get("req_dict")).values()
            msg['data'] = query_result[0]
        except Exception as e:

            msg['code'] = crud_error_code
            msg['msg'] = f"发生错误：{e}"
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def shuiguobaojia_list(request):
    '''
    前台分页
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = request.session.get("req_dict")
        #获取全部列名
        columns=  shuiguobaojia.getallcolumn( shuiguobaojia, shuiguobaojia)
        if "vipread" in req_dict and "vipread" not in columns:
          del req_dict["vipread"]
        #表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
        try:
            __foreEndList__=shuiguobaojia.__foreEndList__
        except:
            __foreEndList__=None
        try:
            __foreEndListAuth__=shuiguobaojia.__foreEndListAuth__
        except:
            __foreEndListAuth__=None

        #authSeparate
        try:
            __authSeparate__=shuiguobaojia.__authSeparate__
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
            __authTables__=shuiguobaojia.__authTables__
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
        
        if shuiguobaojia.__tablename__[:7]=="discuss":
            try:
                del req_dict['userid']
            except:
                pass


        q = Q()
        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  = shuiguobaojia.page(shuiguobaojia, shuiguobaojia, req_dict, request, q)
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def shuiguobaojia_save(request):
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
        columns=  shuiguobaojia.getallcolumn( shuiguobaojia, shuiguobaojia)
        if tablename!='users' and req_dict.get("userid")!=None and 'userid' in columns  and __isAdmin__!='是':
            params=request.session.get("params")
            req_dict['userid']=params.get('id')


        if 'addtime' in req_dict.keys():
            del req_dict['addtime']

        idOrErr= shuiguobaojia.createbyreq(shuiguobaojia,shuiguobaojia, req_dict)
        if idOrErr is Exception:
            msg['code'] = crud_error_code
            msg['msg'] = idOrErr
        else:
            msg['data'] = idOrErr

        return JsonResponse(msg, encoder=CustomJsonEncoder)

def shuiguobaojia_add(request):
    '''
    前台新增
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        tablename=request.session.get("tablename")

        #获取全部列名
        columns=  shuiguobaojia.getallcolumn( shuiguobaojia, shuiguobaojia)
        try:
            __authSeparate__=shuiguobaojia.__authSeparate__
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
            __foreEndListAuth__=shuiguobaojia.__foreEndListAuth__
        except:
            __foreEndListAuth__=None

        if __foreEndListAuth__ and __foreEndListAuth__!="否":
            tablename=request.session.get("tablename")
            if tablename!="users":
                req_dict['userid']=request.session.get("params").get("id")


        if 'addtime' in req_dict.keys():
            del req_dict['addtime']
        error= shuiguobaojia.createbyreq(shuiguobaojia,shuiguobaojia, req_dict)
        if error is Exception:
            msg['code'] = crud_error_code
            msg['msg'] = error
        else:
            msg['data'] = error
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def shuiguobaojia_thumbsup(request,id_):
    '''
     点赞：表属性thumbsUp[是/否]，刷表新增thumbsupnum赞和crazilynum踩字段，
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        id_=int(id_)
        type_=int(req_dict.get("type",0))
        rets=shuiguobaojia.getbyid(shuiguobaojia,shuiguobaojia,id_)

        update_dict={
        "id":id_,
        }
        if type_==1:#赞
            update_dict["thumbsupnum"]=int(rets[0].get('thumbsupnum'))+1
        elif type_==2:#踩
            update_dict["crazilynum"]=int(rets[0].get('crazilynum'))+1
        error = shuiguobaojia.updatebyparams(shuiguobaojia,shuiguobaojia, update_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg, encoder=CustomJsonEncoder)


def shuiguobaojia_info(request,id_):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}

        data = shuiguobaojia.getbyid(shuiguobaojia,shuiguobaojia, int(id_))
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
            __browseClick__= shuiguobaojia.__browseClick__
        except:
            __browseClick__=None

        if __browseClick__=="是"  and  "clicknum"  in shuiguobaojia.getallcolumn(shuiguobaojia,shuiguobaojia):
            try:
                clicknum=int(data[0].get("clicknum",0))+1
            except:
                clicknum=0+1
            click_dict={"id":int(id_),"clicknum":clicknum,"clicktime":datetime.datetime.now()}
            ret=shuiguobaojia.updatebyparams(shuiguobaojia,shuiguobaojia,click_dict)
            if ret!=None:
                msg['code'] = crud_error_code
                msg['msg'] = ret
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def shuiguobaojia_detail(request,id_):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}

        data =shuiguobaojia.getbyid(shuiguobaojia,shuiguobaojia, int(id_))
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
            __browseClick__= shuiguobaojia.__browseClick__
        except:
            __browseClick__=None

        if __browseClick__=="是"   and  "clicknum"  in shuiguobaojia.getallcolumn(shuiguobaojia,shuiguobaojia):
            try:
                clicknum=int(data[0].get("clicknum",0))+1
            except:
                clicknum=0+1
            click_dict={"id":int(id_),"clicknum":clicknum,"clicktime":datetime.datetime.now()}

            ret=shuiguobaojia.updatebyparams(shuiguobaojia,shuiguobaojia,click_dict)
            if ret!=None:
                msg['code'] = crud_error_code
                msg['msg'] = ret
        return JsonResponse(msg, encoder=CustomJsonEncoder)

def shuiguobaojia_update(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        if 'clicktime' in req_dict.keys() and req_dict['clicktime']=="None":
            del req_dict['clicktime']
        if req_dict.get("mima") and "mima" not in shuiguobaojia.getallcolumn(shuiguobaojia,shuiguobaojia) :
            del req_dict["mima"]
        if req_dict.get("password") and "password" not in shuiguobaojia.getallcolumn(shuiguobaojia,shuiguobaojia) :
            del req_dict["password"]
        try:
            del req_dict["clicknum"]
        except:
            pass


        error = shuiguobaojia.updatebyparams(shuiguobaojia, shuiguobaojia, req_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error

        return JsonResponse(msg)


def shuiguobaojia_delete(request):
    '''
    批量删除
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")

        error=shuiguobaojia.deletes(shuiguobaojia,
            shuiguobaojia,
             req_dict.get("ids")
        )
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)


def shuiguobaojia_vote(request,id_):
    '''
    浏览点击次数（表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1）
统计商品或新闻的点击次数；提供新闻的投票功能
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code}


        data= shuiguobaojia.getbyid(shuiguobaojia, shuiguobaojia, int(id_))
        for i in data:
            votenum=i.get('votenum')
            if votenum!=None:
                params={"id":int(id_),"votenum":votenum+1}
                error=shuiguobaojia.updatebyparams(shuiguobaojia,shuiguobaojia,params)
                if error!=None:
                    msg['code'] = crud_error_code
                    msg['msg'] = error
        return JsonResponse(msg)

def shuiguobaojia_importExcel(request):
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
                    shuiguobaojia.createbyreq(shuiguobaojia, shuiguobaojia, req_dict)
                    
            except:
                pass
                
        else:
            msg = {
                "msg": "文件类型错误",
                "code": 500
            }
                
        return JsonResponse(msg)

def shuiguobaojia_autoSort2(request):
    return JsonResponse({"code": 0, "msg": '',  "data":{}})








def shuiguobaojia_shBatch(request):
    '''
    批量审核
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")

        for id in req_dict.get("ids"):
            data =shuiguobaojia.getbyid(shuiguobaojia,shuiguobaojia, int(id))
            if len(data)>0:
                data=data[0]
                data['sfsh'] = req_dict.get("sfsh")
                data['shhf'] = req_dict.get("shhf")
                shuiguobaojia.updatebyparams(shuiguobaojia, shuiguobaojia, data)

        return JsonResponse(msg)






