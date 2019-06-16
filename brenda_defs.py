# 用于PR部分提取信息
import re

# 把数据库文件去除换行保存在new id中
'''
def del_t_and_n(id):
    r = open('new%s.txt'%id, 'w', encoding='UTF-8')
    f1 = f.read()
    f2 = f1.replace('    ', '\t')
    f3 = f2.replace('\n\t', ' ')
    print(f3, file=r)
'''


#  pr的读取 保存为一个列表到fn中（这得重新处理列表的分割符号）
def pr_read(i, ec):
    # 属性值初始化
    prname = ''
    note = 'null'
    uniprot = 'null'
    swissprot = 'null'
    # 统一化列表格式，去除回车符所占的列表位
    a = re.split(r"\s(?![^(]*\))", i)

    a.pop()
    # 检测注释是否存在
    patten = re.findall(r'[(].*[)]', i)
    if patten:
        note = patten[0]
        a.remove(note)
    # 提取前两个信息
    title = a.pop(0)
    iid = a.pop(0).strip('#')
    rf = a.pop()
    if '<' not in rf:
        rf = a.pop() + ',' + rf
    iid = ec + '_' + iid
    # 提取uniprot或swissprot编号
    if a[-1] == 'UniProt':
        uniprot = a[-2]
        a.remove(uniprot)
        a.remove('UniProt')
    elif a[-1] == 'SwissProt':
        swissprot = a[-2]
        a.remove(swissprot)
        a.remove('SwissProt')
    # 提取pr物种名
    for x in a:
        prname = prname + " " + x
    # 导出标签值到文件fn中，并标准化
    ir = '{0}#{1}#{2}#{3}#{4}#{5}'.format(iid, prname.strip(), uniprot, swissprot, note, rf)
    ir = title + '#' + ir
    print(ir) #, file=pr_file)


#  RN的读取
def rn_read(i, ec):
    rn_file = open('%s in brenda' % ec, 'a', encoding='UTF-8')
    a = i.split()
    title = a.pop(0).strip()
    rn_name = ''
    for x in a:
        rn_name = rn_name + ' ' + x
    ir = title + '#' + rn_name
    print(ir)


def sy_read(i, ec):
    # 创建变量
    sy_content = ''
    iid = 'null'
    rf = 'null'
    note = 'null'
    # 读取 i 去除所有空字符
    a = re.split(r"\s(?![^(]*\))", i)
    title = a.pop(0)
    # print(a)
    if '#' in i:
        patten = re.findall(r'[(].*[)]', i)
        if patten:
            note1 = patten[0]
            if len(note1) > 5:
                note = patten[0]
                a.remove(note)
        iid = a.pop(0).strip('#')
        a.pop()
        rf = a.pop()
        for x in a:
            sy_content = sy_content + ' ' + x
    else:  # 不指向固定的iid的内容
        m = i.split()
        m.pop(0)
        sy_content = ''
        for x in m:
            sy_content = sy_content + ' ' + x
    iid = ec + '_' + iid
    ir = title + '#' + iid + '#' + sy_content + '#' + note + '#' + rf
    print(ir)


def en_read(i, ec):
    a = i.split()
    a.pop(0)
    iid = a.pop(0).strip('#')
    iid = ec + '_' + iid
    mutant = a.pop(0)
    rf = a.pop()
    a0 = ''
    for x in a:
        a0 = a0 + ' ' + x
    mutant1 = a0.replace('(', '')
    a1 = mutant1.replace(')', '')
    k = a1.split(';')
    for s in k:
        details = s.split()
        id = details.pop(0).strip('#')
        detail = ''
        iid = ec + '_' + id
        for v in details:
            detail = detail + ' ' + v
        ir = iid + '#' + mutant + '#' + detail
        print(ir)


# AC
'''
def AC_read(i, ec):
    # 创建变量
    main_content = ''
    iid = 'null'
    note = 'null'
    rf = 'null'

    # 读取 i 去除所有空字符
    a = re.split(r"\s(?![^(]*\))", i)
    title = a.pop(0)
    if '\n' in a:
        a.remove('\n')
    rf = a.pop()
    if '#' in i:
        p1 = re.compile(r'[(](.*)[)]', re.S)
        note_p = re.findall(p1, i)
        note = '(' + note_p[0] + ')'
        iid = a.pop(0).replace('#', '')
        for x in a:
            main_content = main_content + ' ' + x
    else:  # 不指向固定的iid的内容
        m = i.split()
        m.pop(0)
        for x in m:
            main_content = main_content + ' ' + x
    iid = ec + '_' + iid
    ir = title + '#' + iid + '#' + main_content + '#' + note + '#' + rf
    print(ir)
'''

# AP TODO 仍有bug，未完成
'''
def AP_read(i, ec):
    # 创建变量
    main_content = ''
    iid = 'null'
    note = 'null'
    rf = 'null'

    # 读取 i 去除所有空字符
    a = re.split(r"\s(?![^(]*\))", i)
    title = a.pop(0)
    if '\n' in a:
        a.remove('\n')
    rf = a.pop()

    p1 = re.compile(r'[(](.*)[)]', re.S)
    note_p = re.findall(p1, i)
    note = '(' + note_p[0] + ')'

    iid = a.pop(0).replace('#', '')
    for x in a:
        main_content = main_content + ' ' + x
    m = i.split()
    m.pop(0)
    for x in m:
        main_content = main_content + ' ' + x
    iid = ec + '_' + iid
    ir = title, '#', iid, '#', main_content, '#', note, '#', rf
    print(ir)

# TODO KI KM PHO PHR PHS SA TO TR TS

def SP_read(i,ec):
    if 'mutant' in i:
        # 初始化
        content = ''
        a = i.split()
        title = a.pop(0)
        reference = a.pop()
        iid = ''

        # if reference too long
        for v in a:
            if '<' in v and '>' not in v:
                reference = v + reference
                a.remove(v)

        # if iid too long
        for t in a[0:2]:
            if '#' in t:
                iid = iid + t + ','
                a.remove(t)
        iid = iid.replace('#', '')
        q = iid.split(',')          # q : the list of iid

        # 将主要内容拼接成一整块
        for x in a:
            content = content + x + ' '

        # to get substrates and products
        b = content.split()
        content = ''        # release the content
        n = 0               # times tag
        notes = ''
        dyh = 0             # the site of '='
        notes_start = 0
        for c in b:
            n += 1
            if c == '=':
                dyh = n
            if '(' in c and ')' not in c:
                notes_start = n

        dw = b[0:dyh]                   # substrate
        cw = b[dyh:notes_start - 1]     # production
        b1 = b[notes_start-1:]          # the next notes and tips
        final_dw = []
        final_cw = []

        # reform the substrate and product
        for x in dw:
            if x == '+' or x == '=':
                pass
            else:
                final_dw.append(x)
        for x in cw:
            if x == '+' or x == '=':
                pass
            else:
                final_cw.append(x)

        # get details and match the mutants
        pattern = re.compile(r'[(](.*)[)]', re.I)

        note_id = 'null'
        content_adds = ''
        for bn in b1:
            content = content + bn + ' '
        note_f = re.findall(pattern, content)
        note_total = note_f[0]
        note_total_list = note_total.split(';')
        for bt in b1:
            content_adds = content_adds + bt + ' '
        content_adds = content_adds.replace('(' + note_total + ')', '')

        for one_note in note_total_list:
            note = one_note.split()
            for e in note:
                if '#' in e:
                    note_id = e.replace('#', '')
                    note.remove(e)
            for ids in q:
                if note_id == ids:
                    ir = ec + '_' + note_id, final_dw, final_cw, note, note_id, content_adds
                    print(ir)

'''
def sp_read(i,ec):
    a = i.split()
    title = a.pop(0)
    n = 0
    mid = 1
    dw = ''
    cw = ''
    notes = ''
    note_start = 0
    note_end = 0
    for q in a:
        n += 1
        if q == '=':
            mid = n
        if '(#' in q:
            note_start = n
        if '>)' in q:
            note_end = n

    dw_list = []
    cw_list = []
    for e in a[0:mid]:
        if e == '+' or e == '=':
            dw_list.append(dw)
            dw = ''
            continue
        else:
            dw = dw + ' ' + e
    for e in a[mid:note_start]:
        if e == '+' or e == '(#':
            cw_list.append(cw)
            cw = ''
            continue
        else:
            cw = cw + ' ' + e
    for e in a[note_start-1:note_end]:
        notes = notes + ' ' + e
    notes = notes.replace('(#', '#')
    notes = notes.replace('>)', '>')
    note_list = notes.split(';')
    for r in note_list:
        b = r.split()
        if b:
            y = b.pop(0)
            y1 = y.replace('#', '')
            y2 = y1.split(',')
            rf = b.pop()
            for u in y2:
                iid = ec + '_' + u
                note = ' '.join(b)
                print(dw_list, cw_list, iid, '#', note, '#', rf)


def re_read(i,ec):
    a = i.split()
    title = a.pop(0)
    n = 0
    mid = 1
    dw = ''
    cw = ''
    notes = ''
    note_start = 0
    note_end = 0
    for q in a:
        n += 1
        if q == '=':
            mid = n
        if '(#' in q:
            note_start = n
        if '>)' in q:
            note_end = n

    dw_list = []
    cw_list = []
    for e in a[0:mid]:
        if e == '+' or e == '=':
            dw_list.append(dw)
            dw = ''
            continue
        else:
            dw = dw + ' ' + e
    for e in a[mid:note_start]:
        if e == '+' or e == '(#':
            cw_list.append(cw)
            cw = ''
            continue
        else:
            cw = cw + ' ' + e
    for e in a[note_start-1:note_end]:
        notes = notes + ' ' + e
    notes = notes.replace('(#', '#')
    notes = notes.replace('>)', '>')
    note_list = notes.split(';')
    for r in note_list:
        b = r.split()
        if b:
            y = b.pop(0)
            y1 = y.replace('#', '')
            y2 = y1.split(',')
            rf = b.pop()
            for u in y2:
                iid = ec + '_' + u
                note = ' '.join(b)
                print(dw_list, cw_list, iid, '#', note, '#', rf)


def km_read(i, ec):
    a = i.split()
    title = a[0]
    iid = a[1]
    iid = ec + '_' + iid.replace('#', '')
    km_value = a[2]
    km_details = a[2]
    rf = a[-1]
    for x in a[2:]:
        if '}' in x:
            km_details = km_details + ' ' + x
    patten = re.findall(r'[(].*[)]', i)
    notes = 'null'
    if patten:
        notes = patten[0]
    ir = title + '#' + iid + '#' + km_value + '#' + km_details + '#' + notes + '#' + rf
    print(ir)


def ki_read(i, ec):
    a = i.split()
    title = a[0]
    iid = a[1]
    iid = ec + '_' + iid.replace('#', '')
    ki_value = a[2]
    ki_details = a[3]
    rf = a[-1]
    for x in a[2:]:
        if '}' in x:
            ki_details = ki_details + ' ' + x
    patten = re.findall(r'[(].*[)]', i)
    notes = 'null'
    if patten:
        notes = patten[0]
    ir = '{0}#{1}#{2}#{3}#{4}#{5}'.format(title, iid, ki_value, ki_details, notes, rf)
    print(ir)


def pho_read(i, ec):
    a = re.split(r"\s(?![^(]*\))", i)
    a.pop()
    title = a[0]
    iid = a[1].replace('#', '')
    iid = ec + '_' + iid
    pho_value = a[2]
    pattern = re.findall(r'[(].*[)]', i)
    if pattern:
        notes = a[3]
        rf = a[4]
    else:
        notes = 'null'
        rf = a[3]
    ir = '{0}#{1}#{2}#{3}#{4}'.format(title, iid, pho_value, notes, rf)
    print(ir)


def phr_read(i, ec):
    a = re.split(r"\s(?![^(]*\))", i)
    a.pop()
    title = a[0]
    iid = a[1].replace('#', '')
    iid = ec + '_' + iid
    phr_value = a[2]
    pattern = re.findall(r'[(].*[)]', i)
    if pattern:
        notes = a[3]
        rf = a[4]
    else:
        notes = 'null'
        rf = a[3]
    ir = '{0}#{1}#{2}#{3}#{4}'.format(title, iid, phr_value, notes, rf)
    print(ir)


def phs_read(i, ec):
    a = re.split(r"\s(?![^(]*\))", i)
    a.pop()
    title = a[0]
    iid = a[1].replace('#', '')
    iid = ec + '_' + iid
    pho_value = a[2]
    pattern = re.findall(r'[(].*[)]', i)
    if pattern:
        notes = a[3]
        rf = a[4]
    else:
        notes = 'null'
        rf = a[3]
    print(title, iid, pho_value, notes, rf)


def sa_read(i, ec):
    a = re.split(r"\s(?![^(]*\))", i)
    a.pop()
    title = a[0]
    iid = a[1].replace('#', '')
    iid = ec + '_' + iid
    sa_value = a[2]
    pattern = re.findall(r'[(].*[)]', i)
    if pattern:
        notes = a[3]
        rf = a[4]
    else:
        notes = 'null'
        rf = a[3]
    ir = '{0}#{1}#{2}#{3}#{4}'.format(title, iid, sa_value, notes, rf)
    print(ir)


def to_read(i, ec):
    a = re.split(r"\s(?![^(]*\))", i)
    a.pop()
    title = a[0]
    iid = a[1].replace('#', '')
    iid = ec + '_' + iid
    to_value = a[2]
    pattern = re.findall(r'[(].*[)]', i)
    if pattern:
        notes = a[3]
        rf = a[4]
    else:
        notes = 'null'
        rf = a[3]
    ir = '{0}#{1}#{2}#{3}#{4}'.format(title, iid, to_value, notes, rf)
    print(ir)


def tr_read(i, ec):
    a = re.split(r"\s(?![^(]*\))", i)
    a.pop()
    title = a[0]
    iid = a[1].replace('#', '')
    iid = ec + '_' + iid
    tr_value = a[2]
    pattern = re.findall(r'[(].*[)]', i)
    if pattern:
        notes = a[3]
        rf = a[4]
    else:
        notes = 'null'
        rf = a[3]
    ir = '{0}#{1}#{2}#{3}#{4}'.format(title, iid, tr_value, notes, rf)
    print(ir)


def ts_read(i, ec):
    a = re.split(r"\s(?![^(]*\))", i)
    a.pop()
    title = a[0]
    iid = a[1].replace('#', '')
    iid = ec + '_' + iid
    ts_value = a[2]
    pattern = re.findall(r'[(].*[)]', i)
    if pattern:
        notes = a[3]
        rf = a[4]
    else:
        notes = 'null'
        rf = a[3]
    ir = '{0}#{1}#{2}#{3}#{4}'.format(title, iid, ts_value, notes, rf)
    print(ir)

