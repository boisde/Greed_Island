#!/usr/bin/env python
# coding:utf-8


def parse_atom_expr(expr, args):
    # 只处理正确的子查询
    if 'is_not' in expr or len(expr) == 1:
        has_not = False
        for key in expr:
            if key == 'is_not':
                has_not = True
            else:
                col = key
                col_op = expr[col].keys()[0]
                col_val = expr[col][col_op]
                # 检查col_op, 看是单元操作符(支持=,>,<,<=,>=,like,regexp,regexp binary), 还是多元操作符(in,between)
                if col_op.strip() in ('=','>','<','<=','>=','like','regexp','regexp binary'):
                    expr_str = '%s %s ?' % (col.strip(), col_op.strip())
                    args.append(col_val[0] if isinstance(col_val, list) else col_val)
                elif col_op.strip() == 'in':
                    if not isinstance(col_val, list):
                        raise TypeError("Wrong values for column[%s], should be a list." % col)
                    expr_str = '%s in (%s)' % (col.strip(), ','.join(['?' for _ in xrange(len(col_val))]))
                    args.extend(col_val)
                elif col_op.strip() == 'between':
                    if not isinstance(col_val, list) or (isinstance(col_val, list) and len(col_val) != 2):
                        raise TypeError("Wrong values for column[%s], should be a list of length 2." % col_val)
                    expr_str = '%s between ? and ?' % col.strip()
                    args.extend(col_val)
                else:
                    raise ValueError("Wrong column operation [%s]." % col_op)
        expr_str = 'NOT %s' % expr_str if has_not else expr_str
        return expr_str
    else:
        raise ValueError("Wrong expression json")


def json_to_query_str(expr_json, args):
    op = expr_json['op']
    expr_list = expr_json['exprs']

    first_expr = expr_list[0]
    is_atom, expr_str_list = 'is_not' in first_expr or len(first_expr) == 1, []
    for expr in expr_list:
        if is_atom:
            expr_str_list.append(parse_atom_expr(expr, args))
        else:
            # 递归处理非原子子查询
            expr_str = json_to_query_str(expr, args)
            expr_str_list.append(expr_str)
    return '(%s)' % (' %s ' % str(op).strip()).join(expr_str_list)


# 跑我
if __name__ == '__main__':
    expr_json_atom = {
        'op': 'AND',
        'exprs': [
            {"is_not": 1, "staff_id": {"=": 0}},
            {"status": {"in": ["FIN", "ERR", "ERR_VALID"]}},
            {"money": {"between": ["15", "20"]}},
        ]
    }

    expr_json_level_2 = {
        'op': 'AND',
        'exprs': [
            expr_json_atom,
            # expr_json_atom,
        ]
    }

    expr_json_example = {
        'op': 'OR',
        'exprs': [
            expr_json_level_2,
            # expr_json_level_2,
            # expr_json_level_2,
        ]
    }
    put_my_args_here = []
    # {
    #     'op': 'OR',
    #     'exprs': [
    #         {
    #             'op': 'AND',
    #             'exprs': [
    #                 {
    #                     'op': 'AND',
    #                     'exprs': [
    #                         {'is_not': 1, 'col_a': {'=': 2}},
    #                         {'col_b': {'in': ['b1', 'b2', 'b3']}},
    #                         {'col_c': {'between': ['c1', 'c2']}}]
    #                 }
    #             ]
    #         },
    #         {
    #             'op': 'AND',
    #             'exprs': [
    #                 {
    #                     'op': 'AND',
    #                     'exprs': [
    #                         {'is_not': 1, 'col_a': {'=': 2}},
    #                         {'col_b': {'in': ['b1', 'b2', 'b3']}},
    #                         {'col_c': {'between': ['c1', 'c2']}}
    #                     ]
    #                 }
    #             ]
    #         }
    #     ]
    # }
    print "In [1]:\n %s\n\n" % expr_json_example
    print "Out [1]:\n %s\n" % json_to_query_str(expr_json_example, put_my_args_here)
    print "Out [2]:\n %s\n" % put_my_args_here

    # print json_to_query_str({'exprs': [{'id': {'in': [u'7783149', u'7749919', u'7771104']}}], 'op': 'AND'},
    # put_my_args_here), put_my_args_here
