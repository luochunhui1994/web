#-*-coding:utf-8-*-
from flask import Flask,render_template,request,url_for
import os
import glob
import pymysql
import pandas as pd
import datetime
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
import seaborn as sns
app = Flask(__name__,static_url_path='',static_folder='./static')
def generate_matplotlib_png(datas):
    in_weight = pd.DataFrame(datas).groupby('industry')['stockweight'].sum()
    in_weight = in_weight.to_frame()
    in_weight['industry'] = in_weight.index
    labels = in_weight['industry']
    sizes = in_weight['stockweight']
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False, startangle=150)
    plt.axis('equal')
    plt.title("行业分布")
    time=datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
    png_name="my_matplotlib"+time+".png"
    plt.savefig(f"./static/{png_name}")
    plt.clf()
    return png_name

@app.route('/')
def index():
    conn = pymysql.connect(user='root', host='localhost', passwd='root', db='etf',cursorclass=pymysql.cursors.DictCursor, charset='utf8')
    cur = conn.cursor()
    sql_name_list = "select distinct ETFname, ETFid from table2 "
    cur.execute(sql_name_list)
    datas2 = cur.fetchall()
    name_list = pd.DataFrame(datas2)
    name_list['combine'] = name_list['ETFname'] + ' ' + name_list['ETFid']
    name_list = list(name_list['combine'].values)
    return render_template('base.html',name_list=name_list)

@app.route('/gets/',methods=['POST'])

def search():
    conn = pymysql.connect(user='root', host='localhost', passwd='root', db='etf',cursorclass=pymysql.cursors.DictCursor, charset='utf8')
    cur = conn.cursor()
    S = request.values.get('question')
    sql="select stockname,stockweight,industry from table2  where ETFid='%s' order by stockweight  DESC  limit 20" %S
    sql_name="select distinct ETFname from table2 where ETFid='%s'" %S
    sql_index = "select distinct target_index, target_name from table2 where ETFid='%s'" % S
    cur.execute(sql)
    datas = cur.fetchall()
    cur.execute(sql_name)
    datas1 = cur.fetchall()
    name_search = datas1[0].get('ETFname') + S
    cur.execute(sql_index)
    data_index = cur.fetchall()
    index_code= data_index[0]['target_index']
    index_name =data_index[0]['target_name']

    path = './static'
    for infile in glob.glob(os.path.join(path, '*.png')):
        os.remove(infile)
    matplotlib_png = generate_matplotlib_png(datas)
    return render_template('search.html',items=datas,name_search=index_name,
                          matplotlib_png=matplotlib_png)

if __name__ == '__main__':
    app.run(debug=True)