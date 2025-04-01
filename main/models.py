#coding:utf-8
__author__ = "ila"
from django.db import models

from .model import BaseModel

from datetime import datetime



class hangqinginfo(BaseModel):
    __doc__ = u'''hangqinginfo'''
    __tablename__ = 'hangqinginfo'



    __authTables__={}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='是'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    shijian=models.CharField ( max_length=255, null=True, unique=False, verbose_name='时间' )
    product=models.CharField ( max_length=255, null=True, unique=False, verbose_name='产品/品种' )
    place=models.CharField ( max_length=255, null=True, unique=False, verbose_name='所在产地' )
    jiage=models.FloatField   (  null=True, unique=False, verbose_name='价格' )
    pricetext=models.CharField ( max_length=255, null=True, unique=False, verbose_name='价格描述' )
    sorj=models.FloatField   (  null=True, unique=False, verbose_name='升/降(%)' )
    detailurl=models.TextField   (  null=True, unique=False, verbose_name='详情地址' )
    '''
    shijian=VARCHAR
    product=VARCHAR
    place=VARCHAR
    jiage=Float
    pricetext=VARCHAR
    sorj=Float
    detailurl=Text
    '''
    class Meta:
        db_table = 'hangqinginfo'
        verbose_name = verbose_name_plural = '行情信息'
class purchaseinfo(BaseModel):
    __doc__ = u'''purchaseinfo'''
    __tablename__ = 'purchaseinfo'



    __authTables__={}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    catename=models.CharField ( max_length=255, null=True, unique=False, verbose_name='采购品种' )
    qty=models.FloatField   (  null=True, unique=False, verbose_name='采购量' )
    unit=models.CharField ( max_length=255, null=True, unique=False, verbose_name='单位' )
    shplace=models.CharField ( max_length=255, null=True, unique=False, verbose_name='收货地' )
    level=models.IntegerField  (  null=True, unique=False, verbose_name='采购等级' )
    releasetime=models.CharField ( max_length=255, null=True, unique=False, verbose_name='更新时间' )
    breedname=models.CharField ( max_length=255, null=True, unique=False, verbose_name='类型' )
    linkname=models.CharField ( max_length=255, null=True, unique=False, verbose_name='采购方' )
    '''
    catename=VARCHAR
    qty=Float
    unit=VARCHAR
    shplace=VARCHAR
    level=Integer
    releasetime=VARCHAR
    breedname=VARCHAR
    linkname=VARCHAR
    '''
    class Meta:
        db_table = 'purchaseinfo'
        verbose_name = verbose_name_plural = '采购信息'
class gongyingshang(BaseModel):
    __doc__ = u'''gongyingshang'''
    __tablename__ = 'gongyingshang'

    __loginUser__='gongyingshangmingcheng'


    __authTables__={}
    __authPeople__='是'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __loginUserColumn__='gongyingshangmingcheng'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='是'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    gongyingshangmingcheng=models.CharField ( max_length=255,null=False,unique=True, verbose_name='供应商名称' )
    mima=models.CharField ( max_length=255,null=False, unique=False, verbose_name='密码' )
    touxiang=models.TextField   (  null=True, unique=False, verbose_name='头像' )
    fuzeren=models.CharField ( max_length=255, null=True, unique=False, verbose_name='负责人' )
    lianxidianhua=models.CharField ( max_length=255, null=True, unique=False, verbose_name='联系电话' )
    gongyingshangdizhi=models.CharField ( max_length=255, null=True, unique=False, verbose_name='供应商地址' )
    zizhizheng=models.TextField   (  null=True, unique=False, verbose_name='资质证' )
    sfsh=models.CharField ( max_length=255, null=True, unique=False,default='待审核', verbose_name='是否审核' )
    shhf=models.TextField   (  null=True, unique=False, verbose_name='审核回复' )
    '''
    gongyingshangmingcheng=VARCHAR
    mima=VARCHAR
    touxiang=Text
    fuzeren=VARCHAR
    lianxidianhua=VARCHAR
    gongyingshangdizhi=VARCHAR
    zizhizheng=Text
    sfsh=VARCHAR
    shhf=Text
    '''
    class Meta:
        db_table = 'gongyingshang'
        verbose_name = verbose_name_plural = '供应商'
class shangjia(BaseModel):
    __doc__ = u'''shangjia'''
    __tablename__ = 'shangjia'

    __loginUser__='shangjiamingcheng'


    __authTables__={}
    __authPeople__='是'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __loginUserColumn__='shangjiamingcheng'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    shangjiamingcheng=models.CharField ( max_length=255,null=False,unique=True, verbose_name='商家名称' )
    mima=models.CharField ( max_length=255,null=False, unique=False, verbose_name='密码' )
    touxiang=models.TextField   (  null=True, unique=False, verbose_name='头像' )
    fuzeren=models.CharField ( max_length=255, null=True, unique=False, verbose_name='负责人' )
    shangjiadianhua=models.CharField ( max_length=255, null=True, unique=False, verbose_name='商家电话' )
    '''
    shangjiamingcheng=VARCHAR
    mima=VARCHAR
    touxiang=Text
    fuzeren=VARCHAR
    shangjiadianhua=VARCHAR
    '''
    class Meta:
        db_table = 'shangjia'
        verbose_name = verbose_name_plural = '商家'
class shuiguofenlei(BaseModel):
    __doc__ = u'''shuiguofenlei'''
    __tablename__ = 'shuiguofenlei'



    __authTables__={}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    shuiguofenlei=models.CharField ( max_length=255,null=False,unique=True, verbose_name='水果分类' )
    '''
    shuiguofenlei=VARCHAR
    '''
    class Meta:
        db_table = 'shuiguofenlei'
        verbose_name = verbose_name_plural = '水果分类'
class shuiguoxinxi(BaseModel):
    __doc__ = u'''shuiguoxinxi'''
    __tablename__ = 'shuiguoxinxi'



    __authTables__={'shangjiamingcheng':'shangjia',}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='是'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    shuiguomingcheng=models.CharField ( max_length=255,null=False, unique=False, verbose_name='水果名称' )
    shuiguofenlei=models.CharField ( max_length=255,null=False, unique=False, verbose_name='水果分类' )
    fengmian=models.TextField   (  null=True, unique=False, verbose_name='封面' )
    chandi=models.CharField ( max_length=255, null=True, unique=False, verbose_name='产地' )
    guige=models.CharField ( max_length=255, null=True, unique=False, verbose_name='规格' )
    shuiguoxiangqing=models.TextField   (  null=True, unique=False, verbose_name='水果详情' )
    shuliang=models.IntegerField  ( null=False, unique=False, verbose_name='库存数量' )
    shangjiamingcheng=models.CharField ( max_length=255, null=True, unique=False, verbose_name='商家名称' )
    '''
    shuiguomingcheng=VARCHAR
    shuiguofenlei=VARCHAR
    fengmian=Text
    chandi=VARCHAR
    guige=VARCHAR
    shuiguoxiangqing=Text
    shuliang=Integer
    shangjiamingcheng=VARCHAR
    '''
    class Meta:
        db_table = 'shuiguoxinxi'
        verbose_name = verbose_name_plural = '水果信息'
class caigouxuqiu(BaseModel):
    __doc__ = u'''caigouxuqiu'''
    __tablename__ = 'caigouxuqiu'



    __authTables__={'shangjiamingcheng':'shangjia',}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    shuiguomingcheng=models.CharField ( max_length=255,null=False, unique=False, verbose_name='水果名称' )
    shuiguofenlei=models.CharField ( max_length=255,null=False, unique=False, verbose_name='水果分类' )
    fengmian=models.TextField   (  null=True, unique=False, verbose_name='封面' )
    chandi=models.CharField ( max_length=255, null=True, unique=False, verbose_name='产地' )
    guige=models.CharField ( max_length=255, null=True, unique=False, verbose_name='规格' )
    caigoushuliang=models.IntegerField  ( null=False, unique=False, verbose_name='采购数量' )
    shangjiamingcheng=models.CharField ( max_length=255, null=True, unique=False, verbose_name='商家名称' )
    shangjiadianhua=models.CharField ( max_length=255, null=True, unique=False, verbose_name='商家电话' )
    caigouyaoqiu=models.TextField   (  null=True, unique=False, verbose_name='采购要求' )
    '''
    shuiguomingcheng=VARCHAR
    shuiguofenlei=VARCHAR
    fengmian=Text
    chandi=VARCHAR
    guige=VARCHAR
    caigoushuliang=Integer
    shangjiamingcheng=VARCHAR
    shangjiadianhua=VARCHAR
    caigouyaoqiu=Text
    '''
    class Meta:
        db_table = 'caigouxuqiu'
        verbose_name = verbose_name_plural = '采购需求'
class shuiguobaojia(BaseModel):
    __doc__ = u'''shuiguobaojia'''
    __tablename__ = 'shuiguobaojia'



    __authTables__={'shangjiamingcheng':'shangjia','gongyingshangmingcheng':'gongyingshang',}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='是'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    shuiguomingcheng=models.CharField ( max_length=255,null=False, unique=False, verbose_name='水果名称' )
    shuiguofenlei=models.CharField ( max_length=255,null=False, unique=False, verbose_name='水果分类' )
    fengmian=models.TextField   (  null=True, unique=False, verbose_name='封面' )
    chandi=models.CharField ( max_length=255, null=True, unique=False, verbose_name='产地' )
    guige=models.CharField ( max_length=255, null=True, unique=False, verbose_name='规格' )
    caigoushuliang=models.IntegerField  ( null=False, unique=False, verbose_name='采购数量' )
    shuiguodanjia=models.FloatField   ( null=False, unique=False, verbose_name='水果单价' )
    zongjiage=models.IntegerField  (  null=True, unique=False, verbose_name='总价格' )
    caigouyaoqiu=models.TextField   (  null=True, unique=False, verbose_name='采购要求' )
    baojiashijian=models.DateTimeField  (  null=True, unique=False, verbose_name='报价时间' )
    shangjiamingcheng=models.CharField ( max_length=255, null=True, unique=False, verbose_name='商家名称' )
    shangjiadianhua=models.CharField ( max_length=255, null=True, unique=False, verbose_name='商家电话' )
    gongyingshangmingcheng=models.CharField ( max_length=255, null=True, unique=False, verbose_name='供应商名称' )
    fuzeren=models.CharField ( max_length=255, null=True, unique=False, verbose_name='负责人' )
    lianxidianhua=models.CharField ( max_length=255, null=True, unique=False, verbose_name='联系电话' )
    sfsh=models.CharField ( max_length=255, null=True, unique=False,default='待审核', verbose_name='是否审核' )
    shhf=models.TextField   (  null=True, unique=False, verbose_name='审核回复' )
    ispay=models.CharField ( max_length=255, null=True, unique=False,default='未支付', verbose_name='是否支付' )
    '''
    shuiguomingcheng=VARCHAR
    shuiguofenlei=VARCHAR
    fengmian=Text
    chandi=VARCHAR
    guige=VARCHAR
    caigoushuliang=Integer
    shuiguodanjia=Float
    zongjiage=Integer
    caigouyaoqiu=Text
    baojiashijian=DateTime
    shangjiamingcheng=VARCHAR
    shangjiadianhua=VARCHAR
    gongyingshangmingcheng=VARCHAR
    fuzeren=VARCHAR
    lianxidianhua=VARCHAR
    sfsh=VARCHAR
    shhf=Text
    ispay=VARCHAR
    '''
    class Meta:
        db_table = 'shuiguobaojia'
        verbose_name = verbose_name_plural = '水果报价'
class shuiguofahuo(BaseModel):
    __doc__ = u'''shuiguofahuo'''
    __tablename__ = 'shuiguofahuo'



    __authTables__={'shangjiamingcheng':'shangjia','gongyingshangmingcheng':'gongyingshang',}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    shuiguomingcheng=models.CharField ( max_length=255,null=False, unique=False, verbose_name='水果名称' )
    shuiguofenlei=models.CharField ( max_length=255,null=False, unique=False, verbose_name='水果分类' )
    fengmian=models.TextField   (  null=True, unique=False, verbose_name='封面' )
    chandi=models.CharField ( max_length=255, null=True, unique=False, verbose_name='产地' )
    guige=models.CharField ( max_length=255, null=True, unique=False, verbose_name='规格' )
    caigoushuliang=models.IntegerField  ( null=False, unique=False, verbose_name='发货数量' )
    dingdanxiangqing=models.CharField ( max_length=255,null=False, unique=False, verbose_name='订单详情' )
    shuiguodanjia=models.FloatField   ( null=False, unique=False, verbose_name='水果单价' )
    fahuoshijian=models.DateTimeField  (  null=True, unique=False, verbose_name='发货时间' )
    wuliuxiangqing=models.TextField   (  null=True, unique=False, verbose_name='物流详情' )
    shangjiamingcheng=models.CharField ( max_length=255, null=True, unique=False, verbose_name='商家名称' )
    shangjiadianhua=models.CharField ( max_length=255, null=True, unique=False, verbose_name='商家电话' )
    gongyingshangmingcheng=models.CharField ( max_length=255, null=True, unique=False, verbose_name='供应商名称' )
    fuzeren=models.CharField ( max_length=255, null=True, unique=False, verbose_name='负责人' )
    lianxidianhua=models.CharField ( max_length=255, null=True, unique=False, verbose_name='联系电话' )
    '''
    shuiguomingcheng=VARCHAR
    shuiguofenlei=VARCHAR
    fengmian=Text
    chandi=VARCHAR
    guige=VARCHAR
    caigoushuliang=Integer
    dingdanxiangqing=VARCHAR
    shuiguodanjia=Float
    fahuoshijian=DateTime
    wuliuxiangqing=Text
    shangjiamingcheng=VARCHAR
    shangjiadianhua=VARCHAR
    gongyingshangmingcheng=VARCHAR
    fuzeren=VARCHAR
    lianxidianhua=VARCHAR
    '''
    class Meta:
        db_table = 'shuiguofahuo'
        verbose_name = verbose_name_plural = '水果发货'
class gongyingshangkucun(BaseModel):
    __doc__ = u'''gongyingshangkucun'''
    __tablename__ = 'gongyingshangkucun'



    __authTables__={'gongyingshangmingcheng':'gongyingshang',}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='是'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    shuiguomingcheng=models.CharField ( max_length=255,null=False, unique=False, verbose_name='水果名称' )
    shuiguofenlei=models.CharField ( max_length=255,null=False, unique=False, verbose_name='水果分类' )
    fengmian=models.TextField   (  null=True, unique=False, verbose_name='封面' )
    shuiguochandi=models.CharField ( max_length=255, null=True, unique=False, verbose_name='水果产地' )
    shuiguoguige=models.CharField ( max_length=255, null=True, unique=False, verbose_name='水果规格' )
    shuiguoxiangqing=models.TextField   (  null=True, unique=False, verbose_name='水果详情' )
    shuliang=models.IntegerField  ( null=False, unique=False, verbose_name='库存数量' )
    gongyingshangmingcheng=models.CharField ( max_length=255, null=True, unique=False, verbose_name='供应商名称' )
    '''
    shuiguomingcheng=VARCHAR
    shuiguofenlei=VARCHAR
    fengmian=Text
    shuiguochandi=VARCHAR
    shuiguoguige=VARCHAR
    shuiguoxiangqing=Text
    shuliang=Integer
    gongyingshangmingcheng=VARCHAR
    '''
    class Meta:
        db_table = 'gongyingshangkucun'
        verbose_name = verbose_name_plural = '供应商库存'
class cuxiaohuodong(BaseModel):
    __doc__ = u'''cuxiaohuodong'''
    __tablename__ = 'cuxiaohuodong'



    __authTables__={'shangjiamingcheng':'shangjia',}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='是'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    huodongbiaoti=models.CharField ( max_length=255, null=True, unique=False, verbose_name='活动标题' )
    fengmiantupian=models.TextField   (  null=True, unique=False, verbose_name='封面图片' )
    cuxiaochanpin=models.CharField ( max_length=255, null=True, unique=False, verbose_name='促销产品' )
    cuxiaoleixing=models.CharField ( max_length=255, null=True, unique=False, verbose_name='促销类型' )
    cuxiaoneirong=models.TextField   (  null=True, unique=False, verbose_name='促销内容' )
    fabushijian=models.DateTimeField  (  null=True, unique=False, verbose_name='发布时间' )
    shangjiamingcheng=models.CharField ( max_length=255, null=True, unique=False, verbose_name='商家名称' )
    shangjiadianhua=models.CharField ( max_length=255, null=True, unique=False, verbose_name='商家电话' )
    reversetime=models.DateTimeField  (  null=True, unique=False, verbose_name='倒计结束时间' )
    storeupnum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='收藏数' )
    '''
    huodongbiaoti=VARCHAR
    fengmiantupian=Text
    cuxiaochanpin=VARCHAR
    cuxiaoleixing=VARCHAR
    cuxiaoneirong=Text
    fabushijian=DateTime
    shangjiamingcheng=VARCHAR
    shangjiadianhua=VARCHAR
    reversetime=DateTime
    storeupnum=Integer
    '''
    class Meta:
        db_table = 'cuxiaohuodong'
        verbose_name = verbose_name_plural = '促销活动'
class hangqinginfoforecast(BaseModel):
    __doc__ = u'''hangqinginfoforecast'''
    __tablename__ = 'hangqinginfoforecast'



    __authTables__={}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    shijian=models.CharField ( max_length=255, null=True, unique=False, verbose_name='时间' )
    product=models.CharField ( max_length=255, null=True, unique=False, verbose_name='产品/品种' )
    jiage=models.FloatField   (  null=True, unique=False, verbose_name='价格' )
    '''
    shijian=VARCHAR
    product=VARCHAR
    jiage=Float
    '''
    class Meta:
        db_table = 'hangqinginfoforecast'
        verbose_name = verbose_name_plural = '行情预测'
class newstype(BaseModel):
    __doc__ = u'''newstype'''
    __tablename__ = 'newstype'



    __authTables__={}
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    typename=models.CharField ( max_length=255,null=False, unique=False, verbose_name='分类名称' )
    '''
    typename=VARCHAR
    '''
    class Meta:
        db_table = 'newstype'
        verbose_name = verbose_name_plural = '公告信息分类'
class news(BaseModel):
    __doc__ = u'''news'''
    __tablename__ = 'news'



    __authTables__={}
    __thumbsUp__='是'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='是'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='是'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    title=models.CharField ( max_length=255,null=False, unique=False, verbose_name='标题' )
    introduction=models.TextField   (  null=True, unique=False, verbose_name='简介' )
    typename=models.CharField ( max_length=255, null=True, unique=False, verbose_name='分类名称' )
    name=models.CharField ( max_length=255, null=True, unique=False, verbose_name='发布人' )
    headportrait=models.TextField   (  null=True, unique=False, verbose_name='头像' )
    clicknum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='点击次数' )
    clicktime=models.DateTimeField  (auto_now=True,  null=True, unique=False, verbose_name='最近点击时间' )
    thumbsupnum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='赞' )
    crazilynum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='踩' )
    storeupnum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='收藏数' )
    picture=models.TextField   ( null=False, unique=False, verbose_name='图片' )
    content=models.TextField   ( null=False, unique=False, verbose_name='内容' )
    '''
    title=VARCHAR
    introduction=Text
    typename=VARCHAR
    name=VARCHAR
    headportrait=Text
    clicknum=Integer
    clicktime=DateTime
    thumbsupnum=Integer
    crazilynum=Integer
    storeupnum=Integer
    picture=Text
    content=Text
    '''
    class Meta:
        db_table = 'news'
        verbose_name = verbose_name_plural = '公告信息'
class storeup(BaseModel):
    __doc__ = u'''storeup'''
    __tablename__ = 'storeup'



    __authTables__={}
    __authSeparate__='是'#后台列表权限
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    userid=models.BigIntegerField  ( null=False, unique=False, verbose_name='用户id' )
    refid=models.BigIntegerField  (  null=True, unique=False, verbose_name='商品id' )
    tablename=models.CharField ( max_length=255, null=True, unique=False, verbose_name='表名' )
    name=models.CharField ( max_length=255,null=False, unique=False, verbose_name='名称' )
    picture=models.TextField   (  null=True, unique=False, verbose_name='图片' )
    type=models.CharField ( max_length=255, null=True, unique=False,default='1', verbose_name='类型' )
    inteltype=models.CharField ( max_length=255, null=True, unique=False, verbose_name='推荐类型' )
    remark=models.CharField ( max_length=255, null=True, unique=False, verbose_name='备注' )
    '''
    userid=BigInteger
    refid=BigInteger
    tablename=VARCHAR
    name=VARCHAR
    picture=Text
    type=VARCHAR
    inteltype=VARCHAR
    remark=VARCHAR
    '''
    class Meta:
        db_table = 'storeup'
        verbose_name = verbose_name_plural = '收藏表'
