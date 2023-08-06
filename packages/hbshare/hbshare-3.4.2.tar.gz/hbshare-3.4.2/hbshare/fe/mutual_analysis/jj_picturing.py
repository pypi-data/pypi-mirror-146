import pandas as pd
from hbshare.fe.XZ import db_engine
from hbshare.fe.XZ import functionality


util=functionality.Untils()
hbdb=db_engine.HBDB()
localdb=db_engine.PrvFunDB().engine


def industry_pic(jjdm,jjjc,th1=0.5,th2=0.5):


    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from hbs_industry_property",con=localdb)['asofdate'][0]

    sql="SELECT * from hbs_industry_property where jjdm='{0}' and asofdate='{1}' "\
        .format(jjdm,latest_date)
    industry_p_old=pd.read_sql(sql,con=localdb).rename(columns={'cen_ind':'行业集中度',
                                                            'ratio_ind':'行业换手率',
                                                            'cen_theme':'主题集中度',
                                                            'ratio_theme':'主题换手率',
                                                            'industry_num':'行业暴露数',
                                                            'top5': '前五大行业',
                                                            })

    float_col_list_old=industry_p_old.columns.tolist()
    float_col_list_old.remove('jjdm')
    float_col_list_old.remove('asofdate')
    float_col_list_old.remove('前五大行业')


    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from hbs_industry_property_new",con=localdb)['asofdate'][0]

    sql="SELECT * from hbs_industry_property_new where jjdm='{0}' and asofdate='{1}' "\
        .format(jjdm,latest_date)
    industry_p=pd.read_sql(sql,con=localdb).rename(columns={'cen_ind_1':'一级行业集中度',
                                                            'ratio_ind_1':'一级行业换手率',
                                                            'cen_ind_2': '二级行业集中度',
                                                            'ratio_ind_2': '二级行业换手率',
                                                            'cen_ind_3': '三级行业集中度',
                                                            'ratio_ind_3': '三级行业换手率',
                                                            'industry_num':'行业暴露数',
                                                            'top5': '前五大行业',
                                                            'longtou_med':'龙头占比（时序中位数）',
                                                            'longtou_mean': '龙头占比（时序均值）',
                                                            'longtou_med_rank': '龙头占比（时序中位数）排名',
                                                            'longtou_mean_rank': '龙头占比（时序均值）排名',

                                                            })

    float_col_list=industry_p.columns.tolist()
    float_col_list.remove('jjdm')
    float_col_list.remove('asofdate')
    float_col_list.remove('前五大行业')


    industry_detail_df_list=[]
    class_name_list=['yjxymc','ejxymc','sjxymc']
    name_map=dict(zip([ 'zsbl_mean', 'ROE_mean', 'NETASSETPS_mean',
       'DIVIDENDRATIO_mean', 'OPERCASHFLOWPS_mean', 'TOTALMV_mean', 'PE_mean',
       'PB_mean', 'PEG_mean', 'EPS_mean', 'NETPROFITGROWRATE_mean',
       'OPERATINGREVENUEYOY_mean', 'longtou_zjbl_for_ind_mean', 'zsbl_med',
       'ROE_med', 'NETASSETPS_med', 'DIVIDENDRATIO_med', 'OPERCASHFLOWPS_med',
       'TOTALMV_med', 'PE_med', 'PB_med', 'PEG_med', 'EPS_med',
       'NETPROFITGROWRATE_med', 'OPERATINGREVENUEYOY_med',
       'longtou_zjbl_for_ind_med', 'jjdm', 'zsbl_mean_rank', 'ROE_mean_rank',
       'NETASSETPS_mean_rank', 'DIVIDENDRATIO_mean_rank',
       'OPERCASHFLOWPS_mean_rank', 'TOTALMV_mean_rank', 'PE_mean_rank',
       'PB_mean_rank', 'PEG_mean_rank', 'EPS_mean_rank',
       'NETPROFITGROWRATE_mean_rank', 'OPERATINGREVENUEYOY_mean_rank',
       'longtou_zjbl_for_ind_mean_rank', 'zsbl_med_rank', 'ROE_med_rank',
       'NETASSETPS_med_rank', 'DIVIDENDRATIO_med_rank',
       'OPERCASHFLOWPS_med_rank', 'TOTALMV_med_rank', 'PE_med_rank',
       'PB_med_rank', 'PEG_med_rank', 'EPS_med_rank',
       'NETPROFITGROWRATE_med_rank', 'OPERATINGREVENUEYOY_med_rank',
       'longtou_zjbl_for_ind_med_rank', 'growth_mean_rank', 'value_mean_rank',
       'growth_med_rank', 'value_med_rank'],['占持仓比例(时序均值）','净资产收益率(时序均值）',
                                             '每股净资产与价格比率(时序均值）','股息率(时序均值）',
                                             '经营现金流与价格比率(时序均值）','总市值(时序均值）',
                                             'PE(时序均值）','PB(时序均值）','PEG(时序均值）',
                                             '每股收益与价格比率(时序均值）','净利润增长率(时序均值）',
                                             '主营业务增长率(时序均值）','行业龙头占比(时序均值）',
                                             '占持仓比例(时序中位数）','净资产收益率(时序中位数）',
                                             '每股净资产与价格比率(时序中位数）','股息率(时序中位数）',
                                             '经营现金流与价格比率(时序中位数）','总市值(时序中位数）',
                                             'PE(时序中位数）','PB(时序中位数）','PEG(时序中位数）',
                                             '每股收益与价格比率(时序中位数）','净利润增长率(时序中位数）',
                                             '主营业务增长率(时序中位数）','行业龙头占比(时序中位数）',
                                             'jjdm','占持仓比例(时序均值）排名','净资产收益率(时序均值）排名',
                                             '每股净资产与价格比率(时序均值）排名','股息率(时序均值）排名',
                                             '经营现金流与价格比率(时序均值）排名','总市值(时序均值）排名',
                                             'PE(时序均值）排名','PB(时序均值）排名','PEG(时序均值）排名',
                                             '每股收益与价格比率(时序均值）排名','净利润增长率(时序均值）排名',
                                             '主营业务增长率(时序均值）排名','行业龙头占比(时序均值）排名',
                                             '占持仓比例(时序中位数）排名','净资产收益率(时序中位数）排名',
                                             '每股净资产与价格比率(时序中位数）排名','股息率(时序中位数）排名',
                                             '经营现金流与价格比率(时序中位数）排名','总市值(时序中位数）排名',
                                             'PE(时序中位数）排名','PB(时序中位数）排名','PEG(时序中位数）排名',
                                             '每股收益与价格比率(时序中位数）排名','净利润增长率(时序中位数）排名',
                                             '主营业务增长率(时序中位数）排名','行业龙头占比(时序中位数）排名',
                                             '综合成长属性(时序均值）排名','综合价值属性(时序均值）排名','综合成长属性(时序中位数）排名',
                                             '综合价值属性(时序中位数）排名','asofdate']))

    sql=" select * from hbs_industry_financial_stats where ENDDATE>='{0}' and ENDDATE<='{1}'"\
        .format(str(int(latest_date[0:4])-3)+latest_date[4:6],latest_date[0:6])
    industry_financial_info=pd.read_sql(sql,con=localdb).groupby('industry_name').mean().rename(columns={
        "ROE":"行业净资产收益率","EPS":"行业每股收益比股价","OPERCASHFLOWPS":"行业经营现金流与价格比率",
        "NETPROFITGROWRATE":"行业净利润增长率","OPERATINGREVENUEYOY":"行业主营业务增长率",
        "NETASSETPS":"行业每股净资产与价格比率","DIVIDENDRATIO":"行业股息率","AVERAGEMV":"行业平均市值","TOTALMV":"行业总市值",
        "PE":"行业PE","PB":"行业PB","PEG":"行业PEG",
                                                                                                           })
    industry_financial_info.columns=industry_financial_info.columns.str.replace('TOP',"")
    industry_financial_info.columns = industry_financial_info.columns.str.replace('TOP', "")
    industry_financial_info.columns = industry_financial_info.columns.str.replace('MV', "市值")
    industry_financial_info.columns = industry_financial_info.columns.str.replace('%', "分位数")
    industry_financial_info.reset_index(inplace=True)

    for i in range(3):
        latest_date = pd.read_sql(
            "select max(asofdate) as asofdate from hbs_industry_property_{0}_industry_level".format(i+1), con=localdb)['asofdate'][0]

        sql = "SELECT * from hbs_industry_property_{2}_industry_level where jjdm='{0}' and asofdate='{1}' " \
            .format(jjdm, latest_date,i+1)
        temp_ind_detail=pd.read_sql(sql, con=localdb).rename(columns=name_map)
        temp_ind_detail.rename(columns={class_name_list[i]:'行业名称'},inplace=True)

        temp_ind_detail=pd.merge(temp_ind_detail,industry_financial_info,how='left',left_on='行业名称',right_on='industry_name')

        temp_ind_detail=temp_ind_detail[['行业名称','占持仓比例(时序中位数）', '占持仓比例(时序中位数）排名', '占持仓比例(时序均值）',
       '占持仓比例(时序均值）排名', '综合价值属性(时序中位数）排名', '综合价值属性(时序均值）排名',
       '综合成长属性(时序中位数）排名', '综合成长属性(时序均值）排名','行业龙头占比(时序中位数）', '行业龙头占比(时序中位数）排名', '行业龙头占比(时序均值）', '行业龙头占比(时序均值）排名',
                                         '主营业务增长率(时序中位数）', '主营业务增长率(时序中位数）排名', '主营业务增长率(时序均值）',
       '主营业务增长率(时序均值）排名','行业主营业务增长率','净利润增长率(时序中位数）', '净利润增长率(时序中位数）排名', '净利润增长率(时序均值）',
       '净利润增长率(时序均值）排名','行业净利润增长率','净资产收益率(时序中位数）', '净资产收益率(时序中位数）排名', '净资产收益率(时序均值）',
       '净资产收益率(时序均值）排名','行业净资产收益率','每股净资产与价格比率(时序中位数）', '每股净资产与价格比率(时序中位数）排名',
       '每股净资产与价格比率(时序均值）', '每股净资产与价格比率(时序均值）排名','行业每股净资产与价格比率','每股收益与价格比率(时序中位数）',
       '每股收益与价格比率(时序中位数）排名', '每股收益与价格比率(时序均值）', '每股收益与价格比率(时序均值）排名','行业每股收益比股价',
                                         '经营现金流与价格比率(时序中位数）', '经营现金流与价格比率(时序中位数）排名', '经营现金流与价格比率(时序均值）',
       '经营现金流与价格比率(时序均值）排名','行业经营现金流与价格比率','股息率(时序中位数）', '股息率(时序中位数）排名',
       '股息率(时序均值）', '股息率(时序均值）排名','行业股息率', 'PE(时序中位数）',
       'PE(时序中位数）排名', 'PE(时序均值）', 'PE(时序均值）排名','行业PE', 'PB(时序中位数）',
       'PB(时序中位数）排名', 'PB(时序均值）', 'PB(时序均值）排名','行业PB', 'PEG(时序中位数）',
       'PEG(时序中位数）排名', 'PEG(时序均值）', 'PEG(时序均值）排名','行业PEG', '总市值(时序中位数）','总市值(时序中位数）排名',
 '总市值(时序均值）','总市值(时序均值）排名', '行业平均市值','25分位数市值','50分位数市值', '75分位数市值', '90分位数市值','asofdate'
]]

        ind_detial_float_col=temp_ind_detail.columns.tolist()
        ind_detial_float_col.sort()
        for col in ['总市值(时序中位数）','总市值(时序中位数）排名',
 '总市值(时序均值）','总市值(时序均值）排名', '行业平均市值','25分位数市值','50分位数市值', '75分位数市值', '90分位数市值','asofdate','行业名称']:
            ind_detial_float_col.remove(col)

        for col in ind_detial_float_col:
            temp_ind_detail[col]=temp_ind_detail[col].map("{:.2%}".format)
        industry_detail_df_list.append(temp_ind_detail )


    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from hbs_industry_shift_property_new",con=localdb)['asofdate'][0]

    sql="SELECT * from hbs_industry_shift_property_new where jjdm='{0}' and asofdate='{1}' "\
        .format(jjdm,latest_date)
    industry_sp=pd.read_sql(sql,con=localdb).set_index('项目名').fillna(0)
    ind_sp_float_col_list=industry_sp.columns.tolist()
    ind_sp_float_col_list.remove('jjdm')
    ind_sp_float_col_list.remove('asofdate')


    #generate the label:
    if(industry_p['一级行业集中度'][0]>th1 and industry_p['一级行业换手率'][0]>th2):
        industry_p['一级行业类型']='博弈'
    elif(industry_p['一级行业集中度'][0]>th1 and industry_p['一级行业换手率'][0]<th2):
        industry_p['一级行业类型'] = '专注'
    elif(industry_p['一级行业集中度'][0]<th1 and industry_p['一级行业换手率'][0]>th2):
        industry_p['一级行业类型'] = '轮动'
    elif(industry_p['一级行业集中度'][0]<th1 and industry_p['一级行业换手率'][0]<th2):
        industry_p['一级行业类型'] = '配置'
        
        
    if(industry_p['二级行业集中度'][0]>th1 and industry_p['二级行业换手率'][0]>th2):
        industry_p['二级行业类型']='博弈'
    elif(industry_p['二级行业集中度'][0]>th1 and industry_p['二级行业换手率'][0]<th2):
        industry_p['二级行业类型'] = '专注'
    elif(industry_p['二级行业集中度'][0]<th1 and industry_p['二级行业换手率'][0]>th2):
        industry_p['二级行业类型'] = '轮动'
    elif(industry_p['二级行业集中度'][0]<th1 and industry_p['二级行业换手率'][0]<th2):
        industry_p['二级行业类型'] = '配置'
        
    if(industry_p['三级行业集中度'][0]>th1 and industry_p['三级行业换手率'][0]>th2):
        industry_p['三级行业类型']='博弈'
    elif(industry_p['三级行业集中度'][0]>th1 and industry_p['三级行业换手率'][0]<th2):
        industry_p['三级行业类型'] = '专注'
    elif(industry_p['三级行业集中度'][0]<th1 and industry_p['三级行业换手率'][0]>th2):
        industry_p['三级行业类型'] = '轮动'
    elif(industry_p['三级行业集中度'][0]<th1 and industry_p['三级行业换手率'][0]<th2):
        industry_p['三级行业类型'] = '配置'


    for col in float_col_list:
        industry_p[col]=industry_p[col].map("{:.2%}".format)


    for col in ind_sp_float_col_list[0:int(len(ind_sp_float_col_list)/2)]:
        industry_sp.loc[industry_sp.index!='切换次数',col]=\
            industry_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
    for col in ind_sp_float_col_list[int(len(ind_sp_float_col_list)/2):]:
        industry_sp[col]=\
            industry_sp[col].astype(float).map("{:.2%}".format)

    industry_p['基金简称']=[jjjc]

    if(len(industry_p_old)>0):


        latest_date = pd.read_sql(
            "select max(asofdate) as asofdate from hbs_theme_shift_property", con=localdb)['asofdate'][0]

        sql = "SELECT * from hbs_theme_shift_property where jjdm='{0}' and asofdate='{1}' " \
            .format(jjdm, latest_date)
        theme_sp = pd.read_sql(sql, con=localdb).set_index('项目名').fillna(0)

        theme_sp_float_col_list = theme_sp.columns.tolist()
        theme_sp_float_col_list.remove('jjdm')
        theme_sp_float_col_list.remove('asofdate')

        if(industry_p_old['主题集中度'][0]>th1 and industry_p_old['主题换手率'][0]>th2):
            industry_p_old['主题类型']='博弈'
        elif(industry_p_old['主题集中度'][0]>th1 and industry_p_old['主题换手率'][0]<th2):
            industry_p_old['主题类型'] = '专注'
        elif(industry_p_old['主题集中度'][0]<th1 and industry_p_old['主题换手率'][0]>th2):
            industry_p_old['主题类型'] = '轮动'
        elif(industry_p_old['主题集中度'][0]<th1 and industry_p_old['主题换手率'][0]<th2):
            industry_p_old['主题类型'] = '配置'



        for col in theme_sp_float_col_list[0:int(len(theme_sp_float_col_list) / 2)]:
            theme_sp.loc[theme_sp.index != '切换次数', col] = \
                theme_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
        for col in theme_sp_float_col_list[int(len(theme_sp_float_col_list) / 2):]:
            theme_sp[col] = \
                theme_sp[col].astype(float).map("{:.2%}".format)

        theme_p=industry_p_old[['jjdm','基金简称','主题类型','主题集中度', '主题换手率','大金融', '消费', 'TMT',
           '周期', '制造', 'asofdate']]
        theme_sp = theme_sp[['Total_rank',
                             '大金融_rank', '消费_rank', 'TMT_rank', '周期_rank', '制造_rank',
                             'Total', '大金融', '消费', 'TMT', '周期', '制造', 'asofdate']]
        theme_sp.reset_index(inplace=True)
    else:
        theme_p=[]
        theme_sp=[]

    industry_p=industry_p[['jjdm','基金简称','一级行业类型','一级行业集中度', '一级行业换手率','前五大行业','龙头占比（时序均值）',
       '龙头占比（时序中位数）', '龙头占比（时序均值）排名', '龙头占比（时序中位数）排名','二级行业类型','二级行业集中度', '二级行业换手率',
                           '三级行业类型','三级行业集中度', '三级行业换手率','asofdate']]

    industry_sp=industry_sp[['Total_rank', '农林牧渔_rank',
       '基础化工_rank', '钢铁_rank', '有色金属_rank', '电子_rank', '家用电器_rank',
       '食品饮料_rank', '纺织服饰_rank', '轻工制造_rank', '医药生物_rank', '公用事业_rank',
       '交通运输_rank', '房地产_rank', '商贸零售_rank', '社会服务_rank', '综合_rank',
       '建筑材料_rank', '建筑装饰_rank', '电力设备_rank', '国防军工_rank', '计算机_rank',
       '传媒_rank', '通信_rank', '银行_rank', '非银金融_rank', '汽车_rank', '机械设备_rank',
       '煤炭_rank', '石油石化_rank', '环保_rank', '美容护理_rank','Total', '农林牧渔', '基础化工', '钢铁', '有色金属', '电子', '家用电器', '食品饮料', '纺织服饰',
       '轻工制造', '医药生物', '公用事业', '交通运输', '房地产', '商贸零售', '社会服务', '综合', '建筑材料',
       '建筑装饰', '电力设备', '国防军工', '计算机', '传媒', '通信', '银行', '非银金融', '汽车', '机械设备',
       '煤炭', '石油石化', '环保', '美容护理','asofdate']]
    industry_sp.reset_index(inplace=True)

    return industry_p,industry_sp,theme_p,theme_sp,industry_detail_df_list

def style_pic(jjdm,jjjc,fre,th1=0.5,th2=0.5):

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from nav_style_property_value where fre='{0}'"
            .format(fre),con=localdb)['asofdate'][0]

    sql="SELECT * from nav_style_property_value where jjdm='{0}' and fre='{1}' and asofdate='{2}' "\
        .format(jjdm,fre,latest_date)
    value_p=pd.read_sql(sql,con=localdb).rename(columns={'shift_ratio_rank':'换手率排名',
                                                         'centralization_rank':'集中度排名',
                                                         '成长_mean':'成长暴露排名',
                                                         '价值_mean':'价值暴露排名',
                                                         '成长_abs_mean': '成长绝对暴露',
                                                         '价值_abs_mean': '价值绝对暴露',
                                                         'manager_change':'经理是否未变更',
                                                         'shift_ratio':'换手率',
                                                         'centralization':'集中度',
                                                         'fre':'回归周期',
                                                         })


    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from hbs_style_property "
            .format(fre),con=localdb)['asofdate'][0]

    sql="SELECT * from hbs_style_property where jjdm='{0}' and asofdate='{1}' "\
        .format(jjdm,latest_date)
    value_p_hbs=pd.read_sql(sql,con=localdb).rename(columns={'cen_lv':'集中度（持仓）',
                                                             'shift_lv':'换手率（持仓）',
                                                             '成长':'成长绝对暴露（持仓）',
                                                             '价值':'价值绝对暴露（持仓）',
                                                             'cen_lv_rank':'集中度排名（持仓）',
                                                             'shift_lv_rank':'换手率排名（持仓）',
                                                             '成长_rank':'成长暴露排名（持仓）',
                                                             '价值_rank':'价值暴露排名（持仓）',})


    # generate the label for nav based :
    winning_value=value_p[['成长暴露排名','价值暴露排名']].T[value_p[['成长暴露排名','价值暴露排名']].T[0]
                                                 ==value_p[['成长暴露排名','价值暴露排名']].T.max()[0]].index[0]
    if(value_p['集中度排名'][0]>th1 and value_p['换手率排名'][0]>th2 ):
        value_p['风格类型']='博弈'
        value_p['风格偏好']=winning_value[0:2]
    elif(value_p['集中度排名'][0]>th1 and value_p['换手率排名'][0]<th2 ):
        value_p['风格类型'] = '专注'
        value_p['风格偏好'] = winning_value[0:2]
    elif(value_p['集中度排名'][0]<th1 and value_p['换手率排名'][0]>th2 ):
        value_p['风格类型'] = '轮动'
        value_p['风格偏好'] = '均衡'
    elif(value_p['集中度排名'][0]<th1 and value_p['换手率排名'][0]<th2 ):
        value_p['风格类型'] = '配置'
        value_p['风格偏好'] =  '均衡'

    value_p['基金简称']=jjjc
    value_p=value_p[['jjdm','基金简称','风格类型','风格偏好','换手率排名','集中度排名',
                     '成长暴露排名', '价值暴露排名','成长绝对暴露','价值绝对暴露' ,'经理是否未变更',
                     '换手率', '集中度','回归周期','asofdate']]

    # generate the label for hbs based :
    winning_value=value_p_hbs[['成长暴露排名（持仓）','价值暴露排名（持仓）']].T[value_p_hbs[['成长暴露排名（持仓）','价值暴露排名（持仓）']].T[0]
                                                 ==value_p_hbs[['成长暴露排名（持仓）','价值暴露排名（持仓）']].T.max()[0]].index[0]
    if(value_p_hbs['集中度排名（持仓）'][0]>th1 and value_p_hbs['换手率排名（持仓）'][0]>th2 ):
        value_p_hbs['风格类型']='博弈'
        value_p_hbs['风格偏好']=winning_value[0:2]
    elif(value_p_hbs['集中度排名（持仓）'][0]>th1 and value_p_hbs['换手率排名（持仓）'][0]<th2 ):
        value_p_hbs['风格类型'] = '专注'
        value_p_hbs['风格偏好'] = winning_value[0:2]
    elif(value_p_hbs['集中度排名（持仓）'][0]<th1 and value_p_hbs['换手率排名（持仓）'][0]>th2 ):
        value_p_hbs['风格类型'] = '轮动'
        value_p_hbs['风格偏好'] = '均衡'
    elif(value_p_hbs['集中度排名（持仓）'][0]<th1 and value_p_hbs['换手率排名（持仓）'][0]<th2 ):
        value_p_hbs['风格类型'] = '配置'
        value_p_hbs['风格偏好'] =  '均衡'

    value_p_hbs['基金简称']=jjjc
    value_p_hbs=value_p_hbs[['jjdm','基金简称','风格类型','风格偏好','集中度（持仓）', '换手率（持仓）',
                             '成长绝对暴露（持仓）', '价值绝对暴露（持仓）', '集中度排名（持仓）',
       '换手率排名（持仓）', '成长暴露排名（持仓）', '价值暴露排名（持仓）', 'asofdate']]

    for col in ['集中度（持仓）', '换手率（持仓）', '成长绝对暴露（持仓）', '价值绝对暴露（持仓）', '集中度排名（持仓）',
       '换手率排名（持仓）', '成长暴露排名（持仓）', '价值暴露排名（持仓）']:
        value_p_hbs[col]=value_p_hbs[col].map("{:.2%}".format)

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from nav_style_property_size where fre='{0}'"
            .format(fre),con=localdb)['asofdate'][0]

    sql="SELECT * from nav_style_property_size where jjdm='{0}' and fre='{1}' and asofdate='{2}' "\
        .format(jjdm,fre,latest_date)
    size_p=pd.read_sql(sql,con=localdb).rename(columns={'shift_ratio_rank':'换手率排名',
                                                         'centralization_rank':'集中度排名',
                                                         '大盘_mean':'大盘暴露排名',
                                                         '中盘_mean':'中盘暴露排名',
                                                        '小盘_mean':'小盘暴露排名',
                                                        '大盘_abs_mean': '大盘绝对暴露',
                                                        '中盘_abs_mean': '中盘绝对暴露',
                                                        '小盘_abs_mean': '小盘绝对暴露',
                                                         'manager_change':'经理是否未变更',
                                                         'shift_ratio':'换手率',
                                                         'centralization':'集中度',
                                                         'fre':'回归周期',
                                                         })

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from hbs_size_property "
            .format(fre),con=localdb)['asofdate'][0]

    sql="SELECT * from hbs_size_property where jjdm='{0}' and asofdate='{1}' "\
        .format(jjdm,latest_date)
    size_p_hbs=pd.read_sql(sql,con=localdb).rename(columns={'cen_lv':'集中度（持仓）',
                                                             'shift_lv':'换手率（持仓）',
                                                             '大盘':'大盘绝对暴露（持仓）',
                                                             '中盘':'中盘绝对暴露（持仓）',
                                                             '小盘': '小盘绝对暴露（持仓）',
                                                             'cen_lv_rank':'集中度排名（持仓）',
                                                             'shift_lv_rank':'换手率排名（持仓）',
                                                             '大盘_rank':'大盘暴露排名（持仓）',
                                                             '中盘_rank':'中盘暴露排名（持仓）',
                                                             '小盘_rank': '小盘暴露排名（持仓）',
                                                            })



    # generate the label for nav based :
    winning_size=[x[0] for x in size_p[['大盘暴露排名','中盘暴露排名','小盘暴露排名']].T[size_p[['大盘暴露排名','中盘暴露排名','小盘暴露排名']].T[0]>0.5].index.tolist()]
    winning_size=''.join(winning_size)

    if(size_p['集中度排名'][0]>th1 and size_p['换手率排名'][0]>th2 ):
        size_p['规模风格类型']='博弈'
        size_p['规模偏好']=winning_size
    elif(size_p['集中度排名'][0]>th1 and size_p['换手率排名'][0]<th2 ):
        size_p['规模风格类型'] = '专注'
        size_p['规模偏好'] = winning_size
    elif(size_p['集中度排名'][0]<th1 and size_p['换手率排名'][0]>th2 ):
        size_p['规模风格类型'] = '轮动'
        size_p['规模偏好'] = '均衡'
    elif(size_p['集中度排名'][0]<th1 and size_p['换手率排名'][0]<th2 ):
        size_p['规模风格类型'] = '配置'
        size_p['规模偏好'] ='均衡'

    size_p['基金简称']=jjjc
    size_p=size_p[['jjdm','基金简称','规模风格类型','规模偏好','换手率排名','集中度排名','大盘暴露排名',
                   '大盘绝对暴露','中盘暴露排名','中盘绝对暴露','小盘暴露排名','小盘绝对暴露', '经理是否未变更',
                     '换手率', '集中度','回归周期','asofdate']]

    # generate the label for hbs based :
    winning_size=[x[0] for x in size_p_hbs[['大盘暴露排名（持仓）','中盘暴露排名（持仓）','小盘暴露排名（持仓）']].T[size_p_hbs[['大盘暴露排名（持仓）','中盘暴露排名（持仓）','小盘暴露排名（持仓）']].T[0]>0.5].index.tolist()]
    winning_size=''.join(winning_size)

    if(size_p_hbs['集中度排名（持仓）'][0]>th1 and size_p_hbs['换手率排名（持仓）'][0]>th2 ):
        size_p_hbs['规模风格类型']='博弈'
        size_p_hbs['规模偏好']=winning_size
    elif(size_p_hbs['集中度排名（持仓）'][0]>th1 and size_p_hbs['换手率排名（持仓）'][0]<th2 ):
        size_p_hbs['规模风格类型'] = '专注'
        size_p_hbs['规模偏好'] = winning_size
    elif(size_p_hbs['集中度排名（持仓）'][0]<th1 and size_p_hbs['换手率排名（持仓）'][0]>th2 ):
        size_p_hbs['规模风格类型'] = '轮动'
        size_p_hbs['规模偏好'] = '均衡'
    elif(size_p_hbs['集中度排名（持仓）'][0]<th1 and size_p_hbs['换手率排名（持仓）'][0]<th2 ):
        size_p_hbs['规模风格类型'] = '配置'
        size_p_hbs['规模偏好'] ='均衡'

    size_p_hbs['基金简称']=jjjc
    size_p_hbs=size_p_hbs[['jjdm','基金简称','规模风格类型','规模偏好','集中度（持仓）', '换手率（持仓）', '大盘绝对暴露（持仓）', '中盘绝对暴露（持仓）', '小盘绝对暴露（持仓）',
       '集中度排名（持仓）', '换手率排名（持仓）', '大盘暴露排名（持仓）', '中盘暴露排名（持仓）', '小盘暴露排名（持仓）',
    'asofdate']]
    for col in ['集中度（持仓）', '换手率（持仓）', '大盘绝对暴露（持仓）', '中盘绝对暴露（持仓）', '小盘绝对暴露（持仓）',
       '集中度排名（持仓）', '换手率排名（持仓）', '大盘暴露排名（持仓）', '中盘暴露排名（持仓）', '小盘暴露排名（持仓）']:
        size_p_hbs[col]=size_p_hbs[col].map("{:.2%}".format)

    #shift property for nav based
    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from nav_shift_property_value where fre='{0}'"
            .format(fre),con=localdb)['asofdate'][0]

    sql="SELECT * from nav_shift_property_value where jjdm='{0}' and asofdate='{1}' and fre='{2}' "\
        .format(jjdm,latest_date,fre)
    value_sp=pd.read_sql(sql,con=localdb).set_index('项目名').fillna(0)
    value_sp_float_col_list=value_sp.columns.tolist()
    value_sp_float_col_list.remove('jjdm')
    value_sp_float_col_list.remove('asofdate')
    value_sp_float_col_list.remove('fre')


    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from nav_shift_property_size where fre='{0}'"
            .format(fre),con=localdb)['asofdate'][0]

    sql="SELECT * from nav_shift_property_size where jjdm='{0}' and asofdate='{1}' and fre='{2}' "\
        .format(jjdm,latest_date,fre)
    size_sp=pd.read_sql(sql,con=localdb).set_index('项目名').fillna(0)
    size_sp_float_col_list=size_sp.columns.tolist()
    size_sp_float_col_list.remove('jjdm')
    size_sp_float_col_list.remove('asofdate')
    size_sp_float_col_list.remove('fre')



    # shift property for hbs based
    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from hbs_shift_property_value"
            .format(fre),con=localdb)['asofdate'][0]

    sql="SELECT * from hbs_shift_property_value where jjdm='{0}' and asofdate='{1}'  "\
        .format(jjdm,latest_date)
    value_sp_hbs=pd.read_sql(sql,con=localdb).set_index('项目名').fillna(0)
    value_sp_hbs_float_col_list=value_sp_hbs.columns.tolist()
    value_sp_hbs_float_col_list.remove('jjdm')
    value_sp_hbs_float_col_list.remove('asofdate')


    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from hbs_shift_property_size "
            .format(fre),con=localdb)['asofdate'][0]

    sql="SELECT * from hbs_shift_property_size where jjdm='{0}' and asofdate='{1}' "\
        .format(jjdm,latest_date)
    size_sp_hbs=pd.read_sql(sql,con=localdb).set_index('项目名').fillna(0)
    size_sp_hbs_float_col_list=size_sp_hbs.columns.tolist()
    size_sp_hbs_float_col_list.remove('jjdm')
    size_sp_hbs_float_col_list.remove('asofdate')
    
    


    for col in ['换手率排名', '集中度排名', '成长暴露排名', '价值暴露排名',
                       '换手率', '集中度', ]:
        value_p[col]=value_p[col].map("{:.2%}".format)

    for col in ['换手率排名', '集中度排名', '大盘暴露排名', '中盘暴露排名','小盘暴露排名',
                       '换手率', '集中度', ]:
        size_p[col]=size_p[col].map("{:.2%}".format)


    for col in ['Total', '成长', '价值']:
        value_sp.loc[value_sp.index!='切换次数',col]=\
            value_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
        value_sp_hbs.loc[value_sp_hbs.index!='切换次数',col]=\
            value_sp_hbs.iloc[1:][col].astype(float).map("{:.2%}".format)
    for col in ['Total_rank', '成长_rank', '价值_rank']:
        value_sp[col]=\
            value_sp[col].astype(float).map("{:.2%}".format)
        value_sp_hbs[col]=\
            value_sp_hbs[col].astype(float).map("{:.2%}".format)

    for col in ['Total', '大盘', '中盘', '小盘']:
        size_sp.loc[size_sp.index!='切换次数',col]=\
            size_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
        size_sp_hbs.loc[size_sp_hbs.index!='切换次数',col]=\
            size_sp_hbs.iloc[1:][col].astype(float).map("{:.2%}".format)
    for col in ['Total_rank', '大盘_rank', '中盘_rank', '小盘_rank']:
        size_sp[col]=\
            size_sp[col].astype(float).map("{:.2%}".format)
        size_sp_hbs[col]=\
            size_sp_hbs[col].astype(float).map("{:.2%}".format)


    value_sp=value_sp[['Total_rank', '成长_rank', '价值_rank',
                       'Total', '成长', '价值','fre','asofdate']]
    value_sp_hbs=value_sp_hbs[['Total_rank', '成长_rank', '价值_rank',
                       'Total', '成长', '价值','asofdate']]
    size_sp = size_sp[['Total_rank','大盘_rank', '中盘_rank',
       '小盘_rank','Total', '大盘', '中盘', '小盘','fre','asofdate']]
    size_sp_hbs = size_sp_hbs[['Total_rank', '大盘_rank', '中盘_rank',
                       '小盘_rank', 'Total', '大盘', '中盘', '小盘', 'asofdate']]

    value_sp.reset_index(inplace=True)
    size_sp.reset_index(inplace=True)
    value_sp_hbs.reset_index(inplace=True)
    size_sp_hbs.reset_index(inplace=True)


    return  value_p,value_p_hbs,value_sp,value_sp_hbs, size_p,size_p_hbs,size_sp,size_sp_hbs

def stock_trading_pci(jjdm,jjjc,ind_cen,th1=0.75,th2=0.25,th3=0.5,th4=0.5,th5=0.75,th6=0.5):

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from hbs_holding_property "
        ,con=localdb)['asofdate'][0]

    sql="SELECT * from hbs_holding_property where jjdm='{0}' and asofdate='{1}' "\
        .format(jjdm,latest_date)
    stock_p=pd.read_sql(sql,con=localdb)

    float_col=stock_p.columns.tolist()
    float_col.remove('jjdm')
    float_col.remove('asofdate')
    float_col.remove('持股数量')
    float_col.remove('PE')
    float_col.remove('PB')
    float_col.remove('ROE')
    float_col.remove('股息率')
    float_col.remove('PE_中位数')
    float_col.remove('PB_中位数')
    float_col.remove('ROE_中位数')
    float_col.remove('股息率_中位数')


    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from hbs_stock_trading_property "
        ,con=localdb)['asofdate'][0]

    sql="SELECT * from hbs_stock_trading_property where jjdm='{0}' and asofdate='{1}' "\
        .format(jjdm,latest_date)
    stock_tp=pd.read_sql(sql,con=localdb)

    tp_float_col=stock_tp.columns.tolist()
    tp_float_col.remove('jjdm')
    tp_float_col.remove('平均持有时间（出重仓前）')
    tp_float_col.remove('平均持有时间（出持仓前）')
    tp_float_col.remove('asofdate')


    #generate the labels

    if(stock_p['个股集中度'][0]>th1 and stock_tp['平均持有时间（出持仓前）_rank'][0]>th1 ):
        stock_p['个股风格A']='专注'
    elif(stock_p['个股集中度'][0]>th1 and stock_tp['平均持有时间（出持仓前）_rank'][0]<th2 ):
        stock_p['个股风格A'] = '博弈'
    elif(stock_p['个股集中度'][0]<th2 and stock_tp['平均持有时间（出持仓前）_rank'][0]>th1 ):
        stock_p['个股风格A'] = '配置'
    elif(stock_p['个股集中度'][0]<th2 and stock_tp['平均持有时间（出持仓前）_rank'][0]<th2 ):
        stock_p['个股风格A'] = '轮动'
    else:
        stock_p['个股风格A'] = '无'


    if(stock_p['个股集中度'][0]>th1 and ind_cen<th6 ):
        stock_p['个股风格B']='自下而上'
    elif(stock_p['个股集中度'][0]<th6 and ind_cen>th1 ):
        stock_p['个股风格B'] = '自上而下'

    else:
        stock_p['个股风格B'] = '无'

    if(stock_p['个股集中度'][0]>th1 and stock_p['个股集中度'][0]-stock_p['hhi'][0]>0.05):
        stock_p['是否有尾仓(针对高个股集中基金）']='有尾仓'
    else:
        stock_p['是否有尾仓(针对高个股集中基金）'] = '无尾仓'

    if(stock_tp['左侧概率（出持仓前,半年线）_rank'][0]>th3 and stock_tp['左侧程度（出持仓前,半年线）'][0]>th4):
        stock_tp['左侧标签']='深度左侧'
    elif(stock_tp['左侧概率（出持仓前,半年线）_rank'][0]>th3 and stock_tp['左侧程度（出持仓前,半年线）'][0]<th4):
        stock_tp['左侧标签'] = '左侧'
    else:
        stock_tp['左侧标签'] = '无'

    lable=''
    if(stock_tp['新股概率（出持仓前）_rank'][0]>th5):
        lable+='偏好新股'
    if( stock_tp['次新股概率（出持仓前）_rank'][0]>th5):
        lable+='偏好次新股'
    stock_tp['新股次新股偏好']=lable



    for col in float_col:
        stock_p[col]= stock_p[col].map("{:.2%}".format)
    for col in tp_float_col:
        stock_tp[col] = stock_tp[col].map("{:.2%}".format)



    stock_p['基金简称'] = jjjc
    stock_tp['基金简称'] = jjjc

    stock_p=stock_p[['jjdm','基金简称','个股风格A','个股风格B','是否有尾仓(针对高个股集中基金）','个股集中度', 'hhi','持股数量',
                     '前三大', '前五大', '前十大', '平均仓位', '仓位换手率','PE_rank', 'PB_rank', 'ROE_rank', '股息率_rank', 'PE_中位数_rank',
       'PB_中位数_rank', 'ROE_中位数_rank', '股息率_中位数_rank','PE', 'PB', 'ROE', '股息率',
                     'PE_中位数', 'PB_中位数', 'ROE_中位数', '股息率_中位数','asofdate'
                     ]]
    stock_tp=stock_tp[['jjdm','基金简称','左侧标签', '新股次新股偏好','左侧概率（出重仓前,半年线）_rank', '左侧概率（出持仓前,半年线）_rank',
       '左侧概率（出重仓前,年线）_rank', '左侧概率（出持仓前,年线）_rank',
                       '平均持有时间（出重仓前）_rank', '平均持有时间（出持仓前）_rank','出重仓前平均收益率_rank',
       '出全仓前平均收益率_rank',
                       '新股概率（出重仓前）_rank','新股概率（出持仓前）_rank', '次新股概率（出重仓前）_rank', '次新股概率（出持仓前）_rank','平均持有时间（出重仓前）', '平均持有时间（出持仓前）', '出重仓前平均收益率', '出全仓前平均收益率',
       '左侧概率（出重仓前,半年线）', '左侧概率（出持仓前,半年线）', '左侧概率（出重仓前,年线）', '左侧概率（出持仓前,年线）',
       '左侧程度（出重仓前,半年线）', '左侧程度（出持仓前,半年线）', '左侧程度（出重仓前,年线）', '左侧程度（出持仓前,年线）',
       '新股概率（出重仓前）', '新股概率（出持仓前）', '次新股概率（出重仓前）', '次新股概率（出持仓前）','asofdate'
                       ]]

    return stock_p,stock_tp

if __name__ == '__main__':



    jjdm='161606'
    jjjc=hbdb.db2df("select jjjc from st_fund.t_st_gm_jjxx where jjdm='{0}'".format(jjdm),db='funduser')['jjjc'][0]


    value_p,value_p_hbs,value_sp,value_sp_hbs, size_p,size_p_hbs,size_sp,size_sp_hbs=style_pic(jjdm,jjjc,fre='M')
    industry_p,industry_sp,theme_p,theme_sp,industry_detail_df_list=industry_pic(jjdm,jjjc)
    stock_p,stock_tp=stock_trading_pci(jjdm,jjjc,ind_cen=float(industry_p['一级行业集中度'][0].split('%')[0])/100)


    plot=functionality.Plot(2000,400)
    plot2=functionality.Plot(2000,100)

    print("%html <h3>行业画像</h3>")
    plot2.plotly_table(industry_p, 8000, 'asdf')
    plot.plotly_table(industry_sp, 6000, 'asdf')

    print("%html <h3>一级行业画像</h3>")
    plot.plotly_table(industry_detail_df_list[0],8000,'asdf')
    print("%html <h3>二级行业画像</h3>")
    plot.plotly_table(industry_detail_df_list[1],8000,'asdf')
    print("%html <h3>三级行业画像</h3>")
    plot.plotly_table(industry_detail_df_list[2],8000,'asdf')

    if(len(theme_p)>0):
        print("%html <h3>主题画像</h3>")
        plot2.plotly_table(theme_p, 2000, 'asdf')
        plot.plotly_table(theme_sp, 2000, 'asdf')
    else:
        print("%html <h3>主题画像暂无</h3>")


    print("%html <h3>风格画像_基于持仓</h3>")
    plot2.plotly_table(value_p_hbs, 2000, 'asdf')
    plot.plotly_table(value_sp_hbs, 2000, 'asdf')
    print("%html <h3>风格画像_基于净值</h3>")
    plot2.plotly_table(value_p, 2000, 'asdf')
    plot.plotly_table(value_sp, 2000, 'asdf')

    print("%html <h3>规模风格画像_基于持仓</h3>")
    plot2.plotly_table(size_p_hbs, 2000, 'asdf')
    plot.plotly_table(size_sp_hbs, 2000, 'asdf')
    print("%html <h3>规模风格画像_基于净值</h3>")
    plot2.plotly_table(size_p, 2000, 'asdf')
    plot.plotly_table(size_sp, 2000, 'asdf')


    print("%html <h3>个股交易画像</h3>")
    plot2.plotly_table(stock_p, 4000, 'asdf')
    plot2.plotly_table(stock_tp, 8000, 'asdf')