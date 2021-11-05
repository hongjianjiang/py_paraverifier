import re
import sys


def read_file(url):
    return open(url).read()


def evalConst(text):
    constDict = dict()
    consts = re.findall(r'const\s*(.*?)\s*type', text, re.S)[0]
    temp = consts.split(';')
    l = []
    for i in temp:
        if i:
            l.append(i.strip())
    for i in l:
        pre = re.findall(r'(.*?)\s*:',i,re.S)[0]
        cons = re.findall(r'\d+',i,re.S)[0]
        constDict[pre]=cons
    return constDict

def evalType(text):
    constDict = evalConst(text)
    types = re.findall(r'type\s*(.*?)\s*var',text,re.S)[0]
    temp = types.split(';')
    typeDict = dict()
    l = []
    for i in temp:
        if i:
            l.append(i.strip())
    for i in l:
        if 'enum' in i:
            pre = re.findall(r'(.*?)\s*:', i, re.S)[0]
            cons = re.findall(r'enum\{(.*?)\}', i, re.S)[0]
            typeDict[pre] = cons
        else:
            pre = re.findall(r'(.*?)\s*:', i, re.S)[0]
            cons = re.findall(r'\.\.(\w*)', i, re.S)[0]
            if cons in constDict:
                typeDict[pre]=constDict[cons]
    return typeDict


def evalVar(text):
    typeDict = evalType(text)
    enumDict = dict()
    varDict = dict()
    vars = re.findall(r'var\s*(.*?)\s*ruleset', text, re.S)[0]
    temp = vars.split(';')
    l = []
    for i in temp:
        if i:
            l.append(i.strip())
    for i in l:
        if 'array' in i:
            pre = re.findall(r'(.*?)\s*:', i, re.S)[0]
            cons = re.findall(r'of\s*(.*)', i, re.S)[0]
            inner = re.findall(r'\[(.*)\]',i,re.S)[0]
            enumDict[pre]=inner
            if cons in typeDict:
                if ',' in typeDict[cons]:
                    varDict[pre] = '{' + typeDict[cons] + '}'
        else:
            pre = re.findall(r'(.*?)\s*:', i, re.S)[0]
            cons = re.findall(r':\s*(.*)', i, re.S)[0]
            varDict[pre] = cons
    with open('../Protocol/SMV/{}.smv'.format(fileName),'w') as f:
        f.write('MODULE main\n')
        f.write('VAR\n')
        for k,v in varDict.items():
            if k in enumDict:
                num = typeDict[enumDict[k]]
                for i in range(int(num)):
                    f.write('{}[{}] : {};\n'.format(k,str(i+1),v))
            else:
                f.write('{} : {};\n'.format(k,v))
        f.write('\n--------------------\n')
    return varDict,enumDict


def evalRuleDecl(text):
    typeDict = evalType(text)
    ruleset = re.findall(r'ruleset\s*(.*?)\s*do(.*?)\s*endruleset;',text,re.S)[0]
    param = ruleset[0]
    rules = ruleset[1]
    rs = re.findall(r'"(.*?)"',rules,re.S)
    k = re.findall(r':\s*(.*)',param,re.S)[0]
    num = typeDict[k]
    with open('../Protocol/SMV/{}.smv'.format(fileName),'a') as f:
        for i in rs:
            for j in range(int(num)):
                f.write('n_{}__{} : process Proc__n_{}__{}(n[{}]);\n\n'.format(i,str(j+1),i,str(j+1),str(j+1)))
        f.write('--------------------\n')

def evalInit(text):
    starts = re.findall(r'startstate\s*begin\s*for\s*(.*)\s*do\s*(.*?)\s*endfor;\s*endstartstate;',text,re.S)[0]
    typeDict = evalType(text)
    initDict = dict()
    enumDict = dict()
    param = starts[0]
    k = re.findall(r':\s*(.*)\s',param,re.S)[0]
    num = typeDict[k]
    assigns = starts[1]
    temp = assigns.split(';')
    l = []
    for i in temp:
        if i:
            l.append(i.strip())
    with open('../Protocol/SMV/{}.smv'.format(fileName),'a') as f:
        f.write('ASSIGN\n')
        for i in l:
            if '[' in i:
                pre = re.findall(r'(.*)\[',i,re.S)[0]
                cons = re.findall(r':=\s*(.*)',i,re.S)[0]
                enumDict[pre]=cons
                initDict[pre]=cons
            else:
                pre = re.findall(r'(.*?)\s*:',i,re.S)[0]
                cons = re.findall(r':=\s*(.*)',i,re.S)[0]
                initDict[pre]=cons
        for k,v in initDict.items():
            if 'true' or 'false' in v:
                v = str.upper(v)
            if k in enumDict:
                for i in range(int(num)):
                    f.write('init({}[{}]) := case\n'.format(k,str(i+1)))
                    f.write('TRUE : {};\n'.format(v))
                    f.write('esac;\n')
            else:
                f.write('init({}) := case\n'.format(k))
                f.write('TRUE : {};\n'.format(v))
                f.write('esac;\n')
        f.write('\n--------------------\n')


def evalRule(text):
    typeDict = evalType(text)
    ruleset = re.findall(r'ruleset\s*(.*?)\s*do(.*?)\s*endruleset;',text,re.S)[0]
    param = ruleset[0]
    rules = ruleset[1]
    k = re.findall(r':\s*(.*)',param,re.S)[0]
    num = typeDict[k]
    rs = re.findall(r'rule\s*"(.*?)"\s*(.*?)\s*==>\s*begin\s*(.*?)\s*end;\s*', rules, re.S)
    with open('../Protocol/SMV/{}.smv'.format(fileName),'a') as f:
        for i in rs:
            name = i[0]
            temp = i[1].split('&')
            glist = []
            for t in temp:
                glist.append(t.strip())
            action = i[2].split(';')
            alist = []
            for i in action:
                if i:
                    alist.append(i.strip())
            for j in range(int(num)):
                f.write('MODULE Proc__n_{}__{}(n__{})\n'.format(name,str(j+1),str(j+1)))
                f.write('ASSIGN\n')
                for g in glist:
                    index = glist.index(g)
                    if '[' in g:
                        pre= re.findall(r'(.*)\[',g,re.S)[0]
                        cons = re.findall(r'=\s*(.*)',g,re.S)[0]
                        alt = re.findall(r':=\s*(.*)',alist[index],re.S)[0]
                        gstr = ' & '.join(glist)
                        f.write('next({}__{}) := case\n'.format(pre,str(j+1)))
                        f.write('({}) : {};\n'.format(gstr,alt))
                        f.write('TRUE : {}__{};\n'.format(pre,str(j+1)))
                        f.write('esac;\n')
                    else:
                        pre = re.findall(r'(.*?)\s*=',g,re.S)[0]
                        cons = re.findall(r'=\s*(.*)',g,re.S)[0]
                        alt = re.findall(r':=\s*(.*)',alist[index],re.S)[0]
                        if 'true' or 'false' in alt:
                            alt = str.upper(alt)
                        gstr = ' & '.join(glist)
                        f.write('next({}) := case\n'.format(pre))
                        f.write('({}) : {};\n'.format(gstr,alt))
                        f.write('TRUE : {};\n'.format(pre))
                        f.write('esac;\n')
                f.write('\n---------\n')

if __name__ == '__main__':
    fileName = sys.argv[1]
    text = read_file('../Protocol/'+fileName+'.m')
    evalVar(text)
    evalRuleDecl(text)
    evalInit(text)
    evalRule(text)