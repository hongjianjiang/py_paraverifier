# coding=utf-8
import json
import re
import logging
import getopt
import sys
import os


class TypeDef(object):
    def __init__(self, text):
        # hash map of all constants
        self.consts = []
        self.typedefs = []
        # value range of each type
        self.typenames = {}
        self.recordnames = {}
        self.value = []
        self.evaluate(text)

    def evalEnum(self, text):
        state_list = []
        enums = re.findall(r'\w*?\s*:\s*enum\s*\{(.*?)\}\s*;', text, re.S)
        enums1 = re.findall(r'(\w*?)\s*:\s*enum\s*\{(.*?)\}\s*;', text, re.S)
        consts =  re.findall(r'(\w*?)\s*:\s*\d\.\..*?\s*;', text, re.S)
        self.consts = consts
        self.typenames['bool'] = ['False', 'True'];

        for e in enums:
            state_list.append(e)
        for e1 in enums1:
            self.typenames[e1[0]] = e1[1].replace(" ","").split(',')
        return state_list

    def evalRecord(self,text):
        record = re.findall(r'(\w*?)\s*:\s*record(.*?)\s*end;', text, re.S)
        for r in record:
            ls = r[1].strip('\n').split(';')
            ls.remove('')
            for l in ls:
                var = re.findall(r'(.*?)\s*\:',l,re.S)[0].strip()
                if r[0] in self.recordnames.keys():
                    self.recordnames[r[0]] = self.recordnames[r[0]]+(';'+var)
                else:
                    self.recordnames[r[0]]=  var
            # self.typenames[r[0]] =
    # def evalScalarset(self, text):
    #     scalarsets = re.findall(r'(\w*?)\s*:\s*(\w+?)\s*\.\.\s*(\w+?)\s*;', text, re.S)
    #
    #     def const2num(v, text):
    #         return int(re.findall(r'%s\s*:\s*(\d+)\s*;' % v, text, re.S)[0])
    #
    #     for name, v1, v2 in scalarsets:
    #         num1 = int(v1) if re.match(r'\d+', v1) else const2num(v1, text)
    #         num2 = int(v2) if re.match(r'\d+', v2) else const2num(v2, text)
    #         self.typedefs.append('enum %s (int_consts [%s]);' % (
    #             name,
    #             '; '.join(map(lambda x: str(x), range(num1, num2 + 1)))
    #         ))
    #         self.typenames[name] = map(lambda x: '%d' % x, range(num1, num2 + 1))

    def evalBool(self):
        # self.const_defs += ['let _True = boolc true', 'let _False = boolc false']
        self.typenames['bool'] = ['False', 'True'];

    def evaluate(self, text):
        # self.evalEnum(text)
        # self.evalScalarset(text)
        self.evalBool()
        for t in self.evalEnum(text):
            # self.value.append(t.replace(" ","").split(','))
            for item in t.replace(" ","").split(','):
                self.value.append(item)
        self.evalRecord(text)


index = -1


class Record(object):
    def __init__(self, text, typenames):
        super(Record, self).__init__()
        self.typenames = typenames
        self.evaluate(text)

    def judgeRecord(self, n, p, v):
        if v in self.typenames:
            return '  [arrdef [(\"%s\", %s)] \"%s\"]' % (n, p, v)
        else:
            return '  record_def \"%s\" %s _%s' % (n, p, v)

    def handleArr(self, n, v):
        try:
            if v[:5] == 'array':
                global index
                pattern = re.compile(r'array\s*\[(.+)\]\s*of\s*(.+)')
                pattern2 = re.compile(r'array\s*\[(.+)\]\s*of\s*array\s*\[(.+)\]\s*of\s*(.+)')
                if pattern2.match(v):
                    index += 2
                    param1, param2, t = pattern2.findall(v)[0]
                    pds = '[paramdef "i%d" "%s"; paramdef "i%d" "%s"]' % (index - 1, param1, index, param2)
                elif pattern.match(v):
                    index += 1
                    param, t = pattern.findall(v)[0]
                    pds = '[paramdef "i%d" "%s"]' % (index, param)
                else:
                    logging.error('new type: %s' % v)
                return self.judgeRecord(n, pds, t)
            else:
                return self.judgeRecord(n, '[]', v)
        except:
            logging.error(v)

    def evaluate(self, text):
        records = []
        record_strs = re.findall(r'(\w*?)\s*:\s*record\s*(.+?)\s*end\s*;', text, re.S)
        for name, fields in record_strs:
            fields = map(
                lambda x: tuple(map(lambda y: y.strip(), x.split(':'))),
                filter(lambda x: x.strip(), fields.split(';'))
            )
            values = map(
                lambda name, t: self.handleArr(name, t),
                fields
            )
            values = 'let _%s = List.concat [\n%s\n]' % (name, ';\n'.join(values))
            records.append(values)
        self.value = '\n\n'.join(records)


class Vardef(object):
    def __init__(self, text, typenames,recordnames,consts):
        super(Vardef, self).__init__()
        self.typenames = typenames
        self.recordnames = recordnames
        self.consts = consts
        self.evaluate(text)

    def judgeRecord(self, n, p, v):
        if (v in self.consts or v in self.typenames) and p in self.consts:
            return 'nat=>nat'
        elif (v == 'boolean') and p in self.consts:
            return 'nat=>bool'
        elif (v in self.consts or v in self.typenames) and p == "":
            return 'nat'
        elif v == 'boolean':
            return 'bool'
        elif v in self.recordnames:
            return v
        else:
            return 'nat'
            # if v == 'boolean':
            #     return 'bool'
            # else:
            #     return 'nat'
            # return '%s' % (v)

    def handleArr(self, n, v):
        if v[:5] == 'array':
            global index
            pattern = re.compile(r'array\s*\[(.+)\]\s*of\s*(.+)')
            param, t = pattern.findall(v)[0]
            index += 1
            return self.judgeRecord(n,  param, t)
        else:
            return self.judgeRecord(n, '', v)

    def evaluate(self, text):
        vs = {}
        var_str = re.findall(r'var\s+((?:\w*\s*:\s*.*?\s*;\s*)*)', text, re.S)[0]
        fields = map(
            lambda x: tuple(map(lambda y: y.strip(), x.split(':'))),
            filter(lambda x: x.strip(), var_str.split(';'))
        )
        for name, t in fields:
            if self.handleArr(name, t) in self.recordnames:
                if ';' in self.recordnames[self.handleArr(name,t)]:
                    for t in self.recordnames[self.handleArr(name,t)].split(';'):
                        vs[name+"_"+ t] = 'nat=>nat'
                else:
                    vs[self.recordnames[self.handleArr(name, t)]] = self.handleArr(name, t)
            else:
                vs[name] = self.handleArr(name, t)
        self.value = vs

def analyzeParams(params):
    """
    @param params: as `i:Node; j:Node`
    @return a tuple as `{'i': 'Node', 'j': 'Node'}, '[paramdef "i" "Node"; paramdef "j" "Node"]'`
    """
    if not params:
        return {}, '[]'
    parts = params.split(';')
    param_name_dict = {}
    # for p in parts: param_name_dict[p.split(':')[0].strip()] = p.split(':')[1].strip()
    param_defs = map(
        lambda x: ' '.join(map(
            lambda y: '%s' % y.strip(),
            x.strip().split(':')[0])
        ),
        parts
    )
    return param_name_dict, param_defs


def escape(name):
    return 'n_%s' % (re.sub(r'_+', '_', re.sub(r'[^a-zA-Z0-9]', '_', name).strip('_')))


class Formula(object):

    __PRIORITY = {
        '(': 100, '=': 50, '!=': 50, '!': 40, '&': 30, '|': 20, '->': 10
    }
    __RELATION_OP = {
        '&': '%s & %s',
        '|': '%s | %s',
        '->': '%s -> %s',
        '=': '%s = %s',
        '!=': '~ (%s = %s)',
    }

    def __init__(self, text):
        super(Formula, self).__init__()
        # self.param_names = param_names
        # self.consts = consts
        try:
            self.text = self.splitText(text)
            self.suffix = self.process(self.text)
            self.value = self.evaluate(self.suffix)
        except Exception as e:
            print(e,text,self.text)

    def splitText(self, text):
        dividers = r'(do|\sendforall|\sendexists|\send|\(|\)|=|!=|!|&|\||->)'
        parts = filter(lambda p: p, map(lambda x: x.strip(), re.split(dividers, text)))
        big_parts = []
        to_add = []
        exp_ends = 0
        for p in parts:
            if p.startswith(('forall', 'exists')):
                exp_ends += 1
                to_add.append(p)
            elif p.startswith('end'):
                exp_ends -= 1
                to_add.append('end')
                if exp_ends == 0:
                    big_parts.append(' '.join(to_add))
                    to_add = []
            elif exp_ends > 0:
                to_add.append(p)
            else:
                big_parts.append(p)
        if len(big_parts) == 0:
            print(text,parts)
            logging.error('could not split text: %s'%text)
        return big_parts

    def process(self, text):
        ops = []
        suffix = []
        for t in text:
            if t in self.__PRIORITY:
                while ops != [] and ops[-1] != '(' and self.__PRIORITY[t] <= self.__PRIORITY[ops[-1]]:
                    suffix.append(ops.pop())
                ops.append(t)
            elif t == ')':
                while ops[-1] != '(':
                    suffix.append(ops.pop())
                ops.pop()
            else:
                suffix.append(t)
        while ops != []:
            suffix.append(ops.pop())
        return suffix

    def evalVar(self,var):
        """
        'a[b][c].d.e[f]' ->
        ['a[b][c]', 'd', 'e[f]'] ->
        [['a', 'b', 'c'], ['d'], ['e', 'f']]
        'Chan1[i].Cmd' -> Chan1_Cmd i
        """
        # print('evalVar:', var)
        if '.' in var:
            list1 = var.split('.')
            name1 = []
            name2 = []
            for l in list1:
                temp = l.split('[')
                for t in temp:
                    if ']' in t:
                        name2.append(t.strip(']'))
                name1.append(l.split('[')[0])
            return '%s %s' % ("_".join(name1), name2[0])
        elif '[' in var:
            return var.replace('[',' ').replace(']',' ')
        else:
            return var

    def evaluate(self, suffix):
        values = []
        for s in suffix:
            if s not in self.__PRIORITY:
                values.append((False, self.evalVar(s)))
            elif s in ['=', '!=']:
                right = (values.pop()[1])
                left = (values.pop()[1])
                values.append((True, self.__RELATION_OP[s] % (left, right)))
            elif s == '!':
                evaled, atom = values.pop()
                if evaled: val = '~ (%s)'% self.evalVar(atom)
                elif atom.strip()[:6] in ['forall', 'exists']:
                    val = '~ %s'% self.evalVar(atom)
                else: val = 'eqn %s (const _False)'% self.evalVar(atom)
                values.append((True, val))
            elif s in ['&', '|', '->']:
                def do_eval(evaled, atom):
                    if evaled: return atom
                    elif atom.strip()[:6] in ['forall', 'exists']:
                        return atom
                    else: return 'eqn %s (const _True)'% self.evalVar(atom)
                rval = do_eval(*values.pop())
                lval = do_eval(*values.pop())
                values.append((True, self.__RELATION_OP[s]%(lval, rval)))
            else:
                print(self.text,suffix)
                logging.error('unknown operator %s'%s)
        if values[0][0]: return values[0][1]
        elif values[0][1].strip()[:6] in ['forall', 'exists']:
            return values[0][1]
        else:
            return 'eqn %s (const _True)' % values[0][1]


class Statement(object):
    def __init__(self, text):
        super(Statement, self).__init__()
        # self.param_names = param_names
        # self.consts = consts
        self.statements = self.splitText(text)
        self.value = self.evaluate(self.statements)

    def splitText(self, text):
        parts = filter(lambda p: p, map(lambda x: x.strip(), re.split(r'(;|do|then|else)', text)))
        big_parts = []
        to_add = []
        exp_ends = 0
        for p in parts:
            if p.startswith(('if', 'for')):
                exp_ends += 1
                to_add.append(p)
            elif p.startswith('end'):
                exp_ends -= 1
                to_add.append(p)
                if exp_ends == 0:
                    big_parts.append(' '.join(to_add))
                    to_add = []
            elif exp_ends > 0:
                to_add.append(p)
            elif p != ';':
                big_parts.append(p)
        if len(big_parts) == 0:
            for p in parts: print(p)
            logging.error('could not split text: %s' % text)
        return big_parts

    def evalVar(self, var):
        """
        'a[b][c].d.e[f]' ->
        ['a[b][c]', 'd', 'e[f]'] ->
        [['a', 'b', 'c'], ['d'], ['e', 'f']]
        'Chan1[i].Cmd' -> Chan1_Cmd i
        """
        # print('evalVar:', var)
        if '.' in var:
            list1 = var.split('.')
            name1 = []
            name2 = []
            for l in list1:
                temp = l.split('[')
                for t in temp:
                    if ']' in t:
                        name2.append(t.strip(']'))
                name1.append(l.split('[')[0])
            return '%s %s' % ("_".join(name1), name2[0])
        elif '[' in var:
            return var.replace('[', ' ').replace(']', ' ')
        else:
            return var

    # def evalAtom(self, atom, param_names):
    #     if atom in self.consts:
    #         return '(const _%s)' % atom
    #     elif atom in param_names:
    #         return '(param (paramref \"%s\"))' % atom
    #     elif re.match(r'^\d+$', atom):
    #         return '(const (intc %s))' % atom
    #     elif atom.lower() in ['true', 'false']:
    #         return '(const (boolc %s))' % atom.lower()
    #     else:
    #         return '(var %s)' % self.evalVar(atom)

    def partitionIf(self, statement):
        parts = filter(lambda p: p, map(lambda x: x.strip(), re.split(r'(;|do|then|else)', statement)))
        sub_clause = []
        to_add = []
        exp_ends = 0
        for p in parts:
            if p.startswith(('if', 'for', 'exists')):
                exp_ends += 1
                to_add.append(p)
            elif p.startswith(('elsif', 'else')) and exp_ends == 1:
                sub_clause.append(' '.join(to_add))
                to_add = [p]
            elif p.startswith('end'):
                exp_ends -= 1
                if exp_ends == 0:
                    sub_clause.append(' '.join(to_add))
                    to_add = []
                else:
                    to_add.append(p)
            elif exp_ends > 0:
                to_add.append(p)
            else:
                logging.error('should not exists statement out of if sub clause')
        return sub_clause

    def analyzeIf(self, sub_clause):
        if sub_clause.startswith('if'):
            f, s = re.findall(r'if(.*?)then(.*)', sub_clause, re.S)[0]
            formula = Formula(f.strip(), param_names, consts)
            inner_ss = self.evaluate(self.splitText(s.strip()), param_names, consts)
            return formula.value, inner_ss
        elif sub_clause.startswith('elsif'):
            f, s = re.findall(r'elsif(.*?)then(.*)', sub_clause, re.S)[0]
            formula = Formula(f.strip(), param_names, consts)
            inner_ss = self.evaluate(self.splitText(s.strip()), param_names, consts)
            return formula.value, inner_ss
        elif sub_clause.startswith('else'):
            s = re.findall(r'else(.*)', sub_clause, re.S)[0]
            inner_ss = self.evaluate(self.splitText(s.strip()), param_names, consts)
            return (inner_ss,)
        else:
            logging.error('not a subclause of if statement: %s' % sub_clause)

    def evalIf(self, statement, param_names, consts):
        sub_clause = map(
            lambda s: self.analyzeIf(s),
            self.partitionIf(statement)
        )
        def inner(sc):
            try:
                if len(sc) == 1:
                    return '(ifStatement %s %s)' % sc[0]
                # ifelse语句的后半句不能是elsif
                elif len(sc) == 2 and len(sc[1]) == 1:
                    return '(ifelseStatement %s %s %s)' % (sc[0][0], sc[0][1], sc[1][0])
                elif len(sc) >= 2:
                    latter = inner(sc[1:])
                    return '(ifelseStatement %s %s %s)' % (sc[0][0], sc[0][1], latter)
                else:
                    logging.error('wrong subclause')
            except:
                msg = '\n'.join(map(lambda x: str(x), sub_clause))
                logging.error('wrong sub clause: \n%s\n\n%s\n\n' % (self.partitionIf(statement), msg))

        return inner(sub_clause)

    def evalFor(self, statement):
        params, statement_str = re.findall(r'for(.*?)do(.*)end(?:for)*', statement, re.S)[0]
        param_name_dict, param_defs = analyzeParams(params)
        for p in param_names:
            if p not in param_name_dict: param_name_dict[p] = 0
        inner_ss = self.evaluate(self.splitText(statement_str), param_name_dict, consts)
        return '(forStatement %s %s)' % (inner_ss, param_defs)

    def evaluate(self, statements):
        def inner(statement):
            if statement.startswith('if'):
                return self.evalIf(statement, param_names, consts)
            elif statement.startswith('for'):
                return self.evalFor(statement, param_names, consts)
            elif re.match(r'clear\s', statement):
                try:
                    estr = statement[5:]
                    return 'clear %s' % (self.evalVar(estr.strip()))
                except:
                    logging.error('unable to handle statement1: %s' % statement)
            else:
                try:
                    vstr, estr = statement.split(':=')
                    v = self.evalVar(vstr.strip())
                    e = estr.strip()
                    return '(assign %s %s)' % (v, e)
                except:
                    logging.error('unable to handle statement2: %s' % statement)
        if len(statements) > 1:
            return '(parallel [%s])' % ('; '.join(statements))
        elif len(statements) == 1:
            return inner(statements[0])
        else:
            logging.error('no statement to be evaluated')


class Rule(object):
    def __init__(self, text):
        super(Rule, self).__init__()
        pattern = re.compile(r'rule\s*\"(.*?)\"\s*(.*?)==>.*?begin(.*?)end\s*;', re.S)
        self.name, guard, statements = pattern.findall(text)[0]
        self.name = escape(self.name)
        # self.params = params
        # self.param_names = param_names
        self.formula = Formula(guard)
        self.statement = Statement(statements)
        self.value = '''%s,guard:%s,action:%s''' % (self.name, self.formula.value, self.statement.value)

    def __str__(self):
        return self.value


class RuleSet(object):
    def __init__(self, text):
        super(RuleSet, self).__init__()
        rules = []
        self.rudic = {}
        self.finalRules = []
        self.vars = []
        self.finalActions = []
        rules += self.rulesets(text)

    def rulesets(self, text):
        rules = []
        action = {}
        vars = []
        pattern = re.compile(r'ruleset(.*?)do\s*(rule.*?)endruleset\s*;', re.S)
        rulesets = pattern.findall(text)
        for params, rules_str in rulesets:
            rule_texts = re.findall(r'(rule.*?end;)', rules_str, re.S)
            for r in rule_texts:
                r1 = Rule(r)
                rule_guard = re.findall(r"\"\w*\"\s*(.*?)(?=\=\=\>)", r, re.S)[0]
                rule_action = re.findall(r"(?<=begin)\s*(.+?)(?=end;)", r, re.S)[0]
                rule_name = re.findall(r"\"(.*?)\"", r, re.S)[0]
                # print(rule_guard,rule_action,rule_name)
                rule_var = re.findall(r'(?<=\[)(.*?)(?=\])', r, re.S)
                # print(len(rule_guard),len(rule_action),len(rule_name),len(rule_var))
                for v in rule_var:
                    if v in vars:
                        pass
                    else:
                        vars.append(v)
                self.rudic['name'] = rule_name.replace("\"", "")
                self.rudic['var'] = vars
                # # print(rule_guard[i].strip(),r1.formula.evalVar(rule_guard[i].strip()))
                # f = Formula(rule_guard.strip())
                self.rudic['guard'] = Formula(rule_guard.strip()).value
                temp = re.findall(r"[^;]+?(?=:\=)", rule_action.replace(" ", "").replace("\n", ""), re.S)
                pre = re.findall(r"(?<=:\=).+?(?=;)", rule_action.replace(" ", "").replace("\n", ""), re.S)
                for j in range(len(temp)):
                    action[r1.statement.evalVar(temp[j])] = r1.statement.evalVar(pre[j])
                    self.finalActions.append(action)
                self.rudic['assign'] = action
                # print(self.rudic)

                action = {}
                self.finalRules.append(self.rudic)
                self.rudic = {}
                vars = []
        return rules


class StartState(object):
    def __init__(self, text):
        super(StartState, self).__init__()
        init_p1 = r'startstate\s*(?:\".*?\"){0,1}(?:.*?begin){0,1}(.*?)endstartstate\s*;'
        statements = re.findall(init_p1, text, re.S)[0].strip()
        assign = re.findall(r'do\s*(.*?)endfor;\s*', statements, re.S)[0]
        var = re.findall(r'(\w)\s*:\s*\w+', statements, re.S)
        statements = []
        for i in Formula(assign.strip().replace(':','')).value.split(';'):
            statements.append(i.strip())
        statements.remove('')
        self.value = {}
        self.value["var"] = var
        self.value["guard"] = " & ".join(statements)


class Invariant(object):
    def __init__(self, text, consts, typenames):
        super(Invariant, self).__init__()
        self.value = []
        self.invsets(text,consts)

    def invsets(self, text, consts):
        pattern = r'ruleset\s*([\w :;]*)do\s*invariant\s*\"(.*?)\"\s*(.*?)\s*;{0,1}\s*endruleset\s*;'
        inv_strs = re.findall(pattern, text, re.S)
        for params, name, form in inv_strs:
            pds = {}
            vars = re.findall(r'(\w)\s*:\s*\w+',params,re.S)
            formula = Formula(form)
            pds["vars"] = vars
            pds['prop'] = formula.evalVar(formula.value)
            # print(formula.value,formula.evalVar(formula.value))
            self.value.append(pds)


class Protocol(object):
    def __init__(self, name, filename):
        self.name = escape(name)
        f = open('../Protocol/'+filename, 'r')
        self.content = f.read()
        f.close()
        self.evaluate()

    def evaluate(self):
        types = TypeDef(self.content)
        vardefs = Vardef(self.content, types.typenames,types.recordnames,types.consts)
        init = StartState(self.content)
        rulesets = RuleSet(self.content)
        invs = Invariant(self.content, types.consts, types.typenames)
        data = {
            'name':self.name,
            'vars':vardefs.value,
            'states':types.value,
            'init':init.value,
            'rules':rulesets.finalRules,
            'invs': invs.value
        }
        with open('../Protocol/'+self.name+'.json','w') as f:
            json.dump(data,f,indent=4)


if __name__ == '__main__':
    help_msg = 'Usage: python gen.py [-n|-m|-h] for [--name|--murphi|--help]\n'
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'n:m:h', ['name=', 'murphi=', 'help'])
        name = None
        murphi = None
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                sys.stdout.write(help_msg)
                sys.exit()
            elif opt in ('-n', '--name'):
                name = arg
            elif opt in ('-m', '--murphi'):
                murphi = arg
            else:
                sys.stderr.write(help_msg)
                sys.exit()
        if murphi is not None and os.path.isfile('../Protocol/'+ murphi):
            basename = os.path.basename(murphi)
            if name is None:
                name = basename if len(basename.split('.')) == 1 else '.'.join(basename.split('.')[:-1])
            protocol = Protocol(name, murphi)
        else:
            sys.stderr.write(help_msg)
            sys.exit()
    except getopt.GetoptError:
        sys.stderr.write(help_msg)
        sys.exit()