def evalVar(var):
    """
    'a[b][c].d.e[f]' ->
    ['a[b][c]', 'd', 'e[f]'] ->
    [['a', 'b', 'c'], ['d'], ['e', 'f']]
    'Chan1[i].Cmd' -> Chan1_Cmd i
    """
    name_parts = map(
        lambda n: map(lambda x: x.strip(']'), n.split('[')),
        var.split('.')
    )
    list1 = var.split('.')
    name1 = []
    name2 = []
    for l in list1:
        temp = l.split('[')
        for t in temp:
            if ']' in t :
                name2.append(t.strip(']'))
        name1.append(l.split('[')[0])
    return '%s %s' % ("_".join(name1),name2[0])



def analyzeParams(params):
    """
    @param params: as `i:Node; j:Node`
    @return a tuple as `{'i': 'Node', 'j': 'Node'}, '[paramdef "i" "Node"; paramdef "j" "Node"]'`
    """
    if not params:
        return {}, '[]'
    parts = params.split(';')
    print(parts)
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
print(analyzeParams('i:client; j: client ',))