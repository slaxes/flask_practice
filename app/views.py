from app import app
from flask import render_template,request,url_for
import json
import os
import pickle
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC_TXT = os.path.join(APP_ROOT, 'static/data')
APP_TEMPLATE = os.path.join(APP_ROOT,'templates')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html",name = "index")


@app.route('/info', methods=['GET', 'POST'])
def info():
    if request.method == 'POST':
        data = request.get_json()
        json_data = json.loads(data)
        info_post("test1.txt","result.pkl",list(json_data["result"]))
        result_path = os.path.join(APP_STATIC_TXT,'result.pkl')
        if not os.path.exists(result_path):
            return json.dumps({"main_question1_acc": 0.0, "main_question2_acc": 0.0})
        result = pickle.load(open(result_path, 'rb'))
        return json.dumps(
            {"main_question1_acc": result['main_question1_acc'], "main_question2_acc": result['main_question2_acc']})
    else:
        return json.dumps({"result":data_dic('test1.txt')})


@app.route('/result', methods=['GET'])
def result():
    result_path = os.path.join(APP_STATIC_TXT, 'result.pkl')
    if not os.path.exists(result_path):
        return json.dumps({"main_question1_acc":0.0 ,"main_question2_acc":0.0 })
    result = pickle.load(open(result_path,'rb'))
    return json.dumps({"main_question1_acc":result['main_question1_acc'],"main_question2_acc":result['main_question2_acc'] })


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
        list_dic["main_question1"] = mainques1
        list_dic["main_question2"] = mainques2
        list_dic["id"] = i
        result.append(list_dic)
        i += 1
    f.close()
    return result


def info_post(inputfile,resultfile,list_data):
    resultfile = os.path.join(APP_STATIC_TXT,resultfile)
    if not os.path.exists(resultfile):
        result = {}
        all_infos = []
        result['all_query'] =len(data_dic(inputfile))
        for i in range(result['all_query']):
            info = {}
            info['id'] = i
            info['main_question1'] = 4
            info['main_question2'] = 4
            all_infos.append(info)
        result['info'] = all_infos
        result['main_question1_acc'] = 0.0
        result['main_question2_acc'] = 0.0
        result['main_question1_true_num'] = 0
        result['main_question2_true_num'] = 0
        result['test_num'] = 0
        pickle.dump(result,open(resultfile,'wb'))

    f = open(resultfile,'rb')
    result = pickle.load(f)
    f.close()

    for data in list_data:
        if data["main_question1"] == "":
            continue
        if data["main_question2"] == "":
            continue

        if data['main_question1'] == '1':
            if result['info'][data['id']]['main_question1'] == 4:
                result['main_question1_true_num'] += 1
                result['test_num'] += 1
            elif result['info'][data['id']]['main_question1'] != 1:
                result['main_question1_true_num'] += 1
            if result['test_num'] != 0:
                result['main_question1_acc'] = result['main_question1_true_num'] * 1.0 / result['test_num']

        elif data['main_question1'] == '2':
            if result['info'][data['id']]['main_question1'] == 4:
                result['test_num'] += 1
            if result['info'][data['id']]['main_question1'] == 1:
                result['main_question1_true_num'] -= 1
            if result['test_num'] != 0:
                result['main_question1_acc'] = result['main_question1_true_num'] * 1.0 / result['test_num']

        elif data['main_question1'] == '3':
            if result['info'][data['id']]['main_question1'] == 4:
                result['test_num'] += 1
            if result['info'][data['id']]['main_question1'] == 1:
                result['main_question1_true_num'] -= 1
            if result['test_num'] != 0:
                result['main_question1_acc'] = result['main_question1_true_num'] * 1.0 / result['test_num']

        if data['main_question2'] == '1':
            if result['info'][data['id']]['main_question2'] == 4:
                result['main_question2_true_num'] += 1
            elif result['info'][data['id']]['main_question2'] != 1:
                result['main_question2_true_num'] += 1
            if result['test_num'] != 0:
                result['main_question2_acc'] = result['main_question2_true_num'] * 1.0 / result['test_num']

        elif data['main_question2'] == '2':
            if result['info'][data['id']]['main_question1'] == 1:
                result['main_question2_true_num'] -= 1
            if result['test_num'] != 0:
                result['main_question2_acc'] = result['main_question2_true_num'] * 1.0 / result['test_num']

        elif data['main_question1'] == '3':
            if result['info'][data['id']]['main_question2'] == 1:
                result['main_question2_true_num'] -= 1
            if result['test_num'] != 0:
                result['main_question2_acc'] = result['main_question2_true_num'] * 1.0 / result['test_num']

        result['info'][data['id']]['main_question1'] = int(data['main_question1'])
        result['info'][data['id']]['main_question2'] = int(data['main_question2'])

    pickle.dump(result,open(resultfile,'wb'))


def select_data(inputfile,resultfile,size):
    resultfile = os.path.join(APP_STATIC_TXT, resultfile)
    data_all = data_dic(inputfile)
    resultdatas = pickle.load(open(resultfile,'rb'))['info']
    id = []
    return_data = []
    i = 0
    for resultdata in resultdatas:
        if resultdata['main_question1'] == 4:
            return_data.append(data_all[resultdata['id']])
            id.append(resultdata['id'])
            i += 1
            if i == size:
                break
    return return_data,id