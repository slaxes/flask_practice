'''
处理数据集为html格式，参数如下：
src: 读取的文件路径
id: 对应问题的id序列list
'''
def load_html(src='./app/static/data/test1.txt',id=[y for y in range(0,60)]):
    with open(src, 'r', encoding='utf-8') as f:
        g = f.read().split('\n')
    with open('./app/templates/src.html', 'w', encoding='utf-8') as f:
        target_matrix = []
        for x in range(0, len(g)):
            item = g[x].split('||')
            target_matrix.append(
            '''
            <li class="inf-list" name="list" id="inf-list''' + str(x+1) + '''">
                <span id="span''' + str(3*x+1) + '''" title="name">''' + 'id:' + str(id[x]) + ' ' + item[0] + ''' </span>
                <span id="span''' + str(3*x+2) + '''" title="email">''' + item[1] + '''<input id="input''' + str(2*x+1) + '''" type="text" maxlength="1" size="2" onkeyup="value=value.replace(/[^\d]/g,'')" style="text-align: center;display:block;width:20px"></span>
                <span id="span''' + str(3*x+3) + '''" title="phone">''' + item[2] + '''<input id="input''' + str(2*x+2) + '''" type="text" maxlength="1" size="2" onkeyup="value=value.replace(/[^\d]/g,'')" style="text-align: center;display:block;width:20px"></span>
            </li>
            ''')
        f.writelines('\n'.join(target_matrix))
