from app import app
from flask import render_template,request,url_for
import json
import os
import pickle
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC_TXT = os.path.join(APP_ROOT, 'static/data')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html",name = "index")

@app.route('/html', methods=['GET', 'POST'])
def src():
    return render_template("src.html",name = "src")

@app.route('/info', methods=['GET', 'POST'])
def info():
    if request.method =='POST':
        data = request.data
        info_post("test1.txt","result.pkl",data)
    else:
        return json.dumps({"result":data_dic('test1.txt')})

@app.route('/result', methods=['GET'])
def result():
    result = pickle.load(open('result.pkl','rb'))
    return json.dumps({"main-question1-acc":result['main-question1-acc'],"main-question2-acc":result['main-question2-acc'] })

def data_dic(mainfile):
    f = open(os.path.join(APP_STATIC_TXT, mainfile),'r')
    result = []
    i = 0
    for line in f:
        query = line.strip('\n').split("||")[0]
        mainques1 = line.strip('\n').split("||")[1]
        mainques2 = line.strip('\n').split("||")[2]
        list_dic = {}
        list_dic["query"] = query
        list_dic["main-question1"] = mainques1
        list_dic["main-question2"] = mainques2
        list_dic["id"] = i
        result.append(list_dic)
        i += 1
    f.close()
    return result

def info_post(inputfile,resultfile,data):
    if not os.path.exists(resultfile):
        result = {}
        all_infos = []
        result['all-query'] =len(data_dic(inputfile))
        for i in range(result['all-query']):
            info = {}
            info['id'] = i
            info['main-question1'] = 4
            info['main-question2'] = 4
            all_infos.append(info)
        result['info'] = all_infos
        result['main-question1-acc'] = 0.0
        result['main-question2-acc'] = 0.0
        result['main-question1-true-num'] = 0
        result['main-question2-true-num'] = 0
        result['test-num'] = 0
        pickle.dump(result,open(resultfile,'wb'))

    result = pickle.load(open(resultfile,'rb'))
    if data['main-question1'] == 1:
        if result['info'][data['id']]['main-question1'] == 4:
            result['main-question1-true-num'] += 1
            result['test-num'] += 1
        elif result['info'][data['id']]['main-question1'] != 1:
            result['main-question1-true-num'] += 1
        result['main-question1-acc'] = result['main-question1-true-num']*1.0 / result['all-query']

    elif data['main-question1'] == 2:
        if result['info'][data['id']]['main-question1'] == 4:
            result['test-num'] += 1
        if result['info'][data['id']]['main-question1'] == 1:
            result['main-question1-true-num'] -= 1
        result['main-question1-acc'] = result['main-question1-true-num']*1.0 / result['all-query']

    elif data['main-question1'] == 3:
        if result['info'][data['id']]['main-question1'] == 4:
            result['test-num'] += 1
        if result['info'][data['id']]['main-question1'] == 1:
            result['main-question1-true-num'] -= 1
        result['main-question1-acc'] = result['main-question1-true-num']*1.0 / result['all-query']

    if data['main-question2'] == 1:
        if result['info'][data['id']]['main-question2'] == 4:
            result['main-question2-true-num'] += 1
            result['test-num'] += 1
        elif result['info'][data['id']]['main-question2'] != 1:
            result['main-question2-true-num'] += 1
        result['main-question2-acc'] = result['main-question2-true-num'] * 1.0 / result['all-query']

    elif data['main-question2'] == 2:
        if result['info'][data['id']]['main-question2'] == 4:
            result['test-num'] += 1
        if result['info'][data['id']]['main-question1'] == 1:
            result['main-question2-true-num'] -= 1
        result['main-question2-acc'] = result['main-question2-true-num'] * 1.0 / result['all-query']

    elif data['main-question1'] == 3:
        if result['info'][data['id']]['main-question2'] == 4:
            result['test-num'] += 1
        if result['info'][data['id']]['main-question2'] == 1:
            result['main-question2-true-num'] -= 1
        result['main-question2-acc'] = result['main-question2-true-num'] * 1.0 / result['all-query']

    result['info'][data['id']]['main-question1'] = data['main-question1']
    result['info'][data['id']]['main-question2'] = data['main-question2']
    pickle.dump(result,open(resultfile,'wb'))


