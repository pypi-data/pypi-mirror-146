import logging
import py2neo
from pjscan import AnalysisFramework
from pjscan.const import *
from cpg2code.three_address_code_path import ThreeAddressCodePath, ThreeAddressCode

from html import unescape


def addslashes(s):
    if isinstance(s, str):
        d = {"\0": "",
             "\"": "\\\""}
        for x in d:
            s = s.replace(x, d.get(x))
        return unescape(s)
    elif s is None:
        return "NULL"
    else:
        return str(s)


def solve_type_conflict(type1, type2):
    # 解决类型冲突问题
    assert type1 in ["", "string", "number", "boolean", ]
    assert type2 in ["", "string", "number", "boolean", ]

    if type1 == "":
        return type2
    if type2 == "":
        return type1
    if type1 == type2:
        return type1
    _type = {type1, type2}
    if _type == {"number", "boolean"}:
        return "number"
    if _type == {"number", "string"}:
        return "number"
    if _type == {"string", "boolean"}:
        return "boolean"


def join_var_node(identity: int, ADD_ENC_FLAG=False, tmp_var_name="$t_", enc_var_name="_enc") -> str:
    """
    rename variables
    :param identity:
    :param ADD_ENC_FLAG:
    :param tmp_var_name:
    :param enc_var_name:
    :return:
    """
    return (tmp_var_name + str(identity)) if not ADD_ENC_FLAG else (tmp_var_name + str(identity) + enc_var_name)


logger = logging.getLogger(__name__)


class SymbolicTracking(object):
    def doc(self):
        """
        # 此处记录一些抽象守则
        主要是想参考MVP的工作把一些东西迁移过来

        __global_abstract_level 记录抽象规则几个比特位的解释如下

        0b00000000000

        FLAG 0b1
        代表是否对常量进行抽象，抽象方法为
        TYPE_STRING => T_STRING
        TYPE_DOUBLE|TYPE_INTERGER => T_NUMBER
        TYPE_CONST => T_CONT
        TYPE_CLASS_CONST => T_CLASS_CONST
        TYPE_A

        FLAG 0b01
        代表是否对变量进行抽象，抽象方法为
        TYPE_ARRAY => T_ARRAY （同时会抹除数组中的所有元素）
        TYPE_VAR   => T_VAR
        TYPE_

        FLAG 0b001

        FLAG 0b0001

        FLAG 0b00001

        """
        ABS_FLAG_ = 1

    def __init__(self, analysis_framework: AnalysisFramework):
        """
        :param analysis_framework: neo4j graph
        """
        self.tac_path = ThreeAddressCodePath()
        self.analysis_framework = analysis_framework
        self.__global_abstract_level = 0b00000000

    def to_src_code(self):
        return self.tac_path.to_src_code()

    def extract_code(self, node: py2neo.Node, abstract_level=0):
        if not node.has_label(LABEL_AST):
            print(f"[*]  get input  {node}  ; only AST node can be converted")
            return ""
        result = 0
        level_backup = self.__global_abstract_level
        self.__global_abstract_level = abstract_level
        if abstract_level == 0:
            a, b = self.manage_generic_node(node)
            c, d = self.tac_path.to_raw_code()
            if d == '':
                result = a
            else:
                result = d
        elif abstract_level == 1:
            a, b = self.manage_generic_node(node)
            c, d = self.tac_path.to_raw_code()
            if d == '':
                result = a
            else:
                result = d
        self.__global_abstract_level = level_backup
        self.clear_memory()
        return str(result)

    def get_expression_ith_node(self, ith: int) -> py2neo.Node:
        node = self.analysis_framework.match(
            code="_expr_{}".format(ith)
        ).first()
        return self.analysis_framework.get_ast_root_node(node)

    def get_condition_ith_node(self, ith: int) -> py2neo.Node:
        node = self.analysis_framework.match(
            code="_cond_{}".format(ith)
        ).first()
        return self.analysis_framework.get_ast_ith_child_node(
            self.analysis_framework.get_ast_root_node(node), 1
        )

    def clear_memory(self):
        self.tac_path = ThreeAddressCodePath()

    def get_node(self, _id, ):
        """
        DEBUG FUNCTION
        """
        return self.analysis_framework.get_node_itself(_id)

    def gen_formula(self, left: str, right: list, op: str, node_type: str, node_id: int, ltype: str, rtype: list):
        """
        Append formula to tac_path and return left_node (lft_var,lft_type)
        """
        single_tac = ThreeAddressCode(left, right, op, node_type, node_id, ltype, rtype)
        self.tac_path.append(
            ThreeAddressCode(left, right, op, node_type, node_id, ltype, rtype)
        )
        # if self.verbose >= 1:
        #     logger.info(self.tac_path.get_push_info(index=-1))
        return left, ltype

    def manage_basic_block(self, node: py2neo.Node):
        if node[NODE_TYPE] == TYPE_CALL:
            return self.manage_function_call(node)
        elif node[NODE_TYPE] == TYPE_STATIC_CALL:
            return self.manage_static_function_call(node)
        elif node[NODE_TYPE] == TYPE_METHOD_CALL:
            return self.manage_dynamic_function_call(node)
        elif node[NODE_TYPE] == TYPE_DIM:
            return self.manage_dim(node)
        elif node[NODE_TYPE] == TYPE_VAR:
            return self.manage_var(node)
        elif node[NODE_TYPE] == TYPE_STRING:
            return self.manage_constant_string(node)
        elif node[NODE_TYPE] == TYPE_INTEGER:
            return self.manage_constant_integer(node)
        elif node[NODE_TYPE] == TYPE_DOUBLE:
            return self.manage_constant_double(node)
        elif node[NODE_TYPE] == TYPE_CONST:
            return self.manage_generic_constant(node)
        elif node[NODE_TYPE] == TYPE_MAGIC_CONST:
            return self.manage_magic_constant(node)
        elif node[NODE_TYPE] == TYPE_NULL:
            return self.manage_null(node)
        elif node[NODE_TYPE] == TYPE_REF:
            return self.manage_ref(node)
        elif node[NODE_TYPE] == TYPE_CLASS_CONST:
            return self.manage_class_constant(node)
        elif node[NODE_TYPE] == TYPE_STATIC_PROP:
            return self.manage_type_static_prop(node)
        elif node[NODE_TYPE] == TYPE_PROP:
            return self.manage_type_prop(node)
        elif node[NODE_TYPE] == TYPE_ARRAY:
            return self.manage_type_array(node)
        elif node[NODE_TYPE] == TYPE_LIST:
            return self.manage_type_list(node)
        elif node[NODE_TYPE] == TYPE_ARRAY_ELEM:
            return self.manage_type_array_elem(node)
        elif node[NODE_TYPE] == TYPE_GLOBAL:
            return self.manage_global_node(node)

    def manage_global_node(self, node: py2neo.Node):
        return self.manage_generic_node(self.analysis_framework.get_ast_child_node(node))

    def manage_type_static_prop(self, node: py2neo.Node):
        class_code = self.analysis_framework.get_ast_child_node(self.analysis_framework.get_ast_child_node(node))[
            'code']
        expr_code = self.analysis_framework.get_ast_ith_child_node(node, 1)['code']
        return f"{class_code}::${expr_code}", "string"
        # return self.gen_formula(
        #     left=join_var_node(node.identity),
        #     right=[f"{class_code}::${expr_code}"],
        #     op=node[NODE_TYPE],
        #     node_type=node[NODE_TYPE],
        #     node_id=node.identity,
        #     ltype="string",
        #     rtype=['string']
        # )

    def manage_type_list(self, node: py2neo.Node):
        list_nodes = self.analysis_framework.find_ast_child_nodes(node)
        resolved_list_nodes = []
        resolved_list_nodes_types = []
        for list_node in list_nodes:
            assert isinstance(list_node, py2neo.Node)
            res_arg = self.manage_generic_node(list_node)
            resolved_list_nodes.append(res_arg[0])
            resolved_list_nodes_types.append(res_arg[1])
        return self.gen_formula(
            left=join_var_node(node.identity),
            right=resolved_list_nodes,
            op="array",
            node_type=TYPE_CALL,
            node_id=node.identity,
            ltype="string",
            rtype=resolved_list_nodes_types
        )

    def manage_instanceof_operation(self, node: py2neo.Node):
        judge_instance_var, judge_instance_var_type = self.manage_generic_node(
            self.analysis_framework.find_ast_child_nodes(node)[0])

        instance_var, instance_type = \
            self.analysis_framework.find_ast_child_nodes(self.analysis_framework.find_ast_child_nodes(node)[1])[0][
                'code'], 'string'
        return self.gen_formula(
            left=join_var_node(node.identity),
            right=[judge_instance_var, instance_var],
            op=TYPE_INSTANCEOF,
            node_type=TYPE_BINARY_OP,
            node_id=node.identity,
            ltype="string",
            rtype=[judge_instance_var_type, instance_type]
        )

    def manage_new_operation(self, node: py2neo.Node):
        args = self.analysis_framework.ast_step.find_function_arg_node_list(node)
        name_node = self.analysis_framework.find_ast_child_nodes(node)[0]
        resolved_args = []
        resolved_args_types = []
        for arg in args:
            assert isinstance(arg, py2neo.Node)
            res_arg = self.manage_generic_node(arg)
            resolved_args.append(res_arg[0])
            resolved_args_types.append(res_arg[1])
        expr, expr_type = self.gen_formula(
            left=join_var_node(name_node.identity),
            right=resolved_args,
            op=self.analysis_framework.find_ast_child_nodes(name_node)[0][NODE_CODE],
            node_type=TYPE_CALL,
            node_id=node.identity,
            ltype="",  # object
            rtype=resolved_args_types
        )
        return self.gen_formula(
            left=join_var_node(node.identity),
            right=[expr],
            op=TYPE_NEW,
            node_type=TYPE_UNARY_OP,
            node_id=node.identity,
            ltype="",
            rtype=[expr_type]
        )

    def manage_function_call(self, node: py2neo.Node):
        args = self.analysis_framework.ast_step.find_function_arg_node_list(node)
        resolved_args = []
        resolved_args_types = []
        for arg in args:
            assert isinstance(arg, py2neo.Node)
            res_arg = self.manage_generic_node(arg)
            resolved_args.append(res_arg[0])
            resolved_args_types.append(res_arg[1])
        return self.gen_formula(
            left=join_var_node(node.identity),
            right=resolved_args,
            op=self.analysis_framework.code_step.get_ast_call_code(node),
            node_type=TYPE_CALL,
            node_id=node.identity,
            ltype="string",
            rtype=resolved_args_types
        )

    def manage_exit_operation(self, node: py2neo.Node):
        if self.analysis_framework.find_ast_child_nodes(node).__len__() == 0:
            expr, expr_type = None, None
        else:
            expr, expr_type = self.manage_generic_node(
                self.analysis_framework.find_ast_child_nodes(node)[0]
            )
        return self.gen_formula(
            left=join_var_node(node.identity),
            right=[expr] if expr is not None else [],
            op="die",
            node_id=node.identity,
            node_type=TYPE_CALL,
            ltype="boolean",
            rtype=[expr_type] if expr_type is not None else [],
        )

    def manage_empty_operation(self, node: py2neo.Node):
        condition = self.manage_generic_node(
            self.analysis_framework.find_ast_child_nodes(node)[0]
        )
        return self.gen_formula(
            left=join_var_node(node.identity),
            right=[condition[0]],
            op="empty",
            node_type=TYPE_CALL,
            node_id=node.identity,
            ltype="boolean",
            rtype=[condition[1]]
        )

    def manage_var(self, node: py2neo.Node):
        return self.analysis_framework.code_step.get_ast_var_code(node), ""

    def manage_dim(self, node: py2neo.Node):
        """
        $a['shaobao']
        =>
        get_slice($a,'shaobao'] / get_slice($a->file,'shaobao']
        """
        nodes = self.analysis_framework.find_ast_child_nodes(node)
        if nodes[0]['type'] == TYPE_VAR and nodes[1]['type'] == TYPE_STRING:
            return self.analysis_framework.code_step.get_ast_dim_code(node), ""
        else:
            expr_var, expr_type = self.manage_generic_node(nodes[0])
            slice_var, slice_type = self.manage_generic_node(nodes[1])
            if slice_var == "null":
                return expr_var + '[]', ""
            else:
                # if slice_type == 'string' and slice_var.count('"') == 2:
                #     slice_var = slice_var.replace('"', '')
                return expr_var + '[' + str(slice_var) + ']', ""

    def manage_binary_operation(self, node: py2neo.Node):
        l_expr = self.manage_generic_node(self.analysis_framework.find_ast_child_nodes(node)[0])
        r_expr = self.manage_generic_node(self.analysis_framework.find_ast_child_nodes(node)[1])
        if node['flags'][0] in ["BINARY_CONCAT"]:
            return self.gen_formula(
                left=join_var_node(node.identity),
                right=[l_expr[0], r_expr[0]],
                op=node['flags'][0],
                node_type=node[NODE_TYPE],
                node_id=node.identity,
                ltype="string",
                rtype=['string', 'string']
            )

        elif (node['flags'][0] in [FLAG_BINARY_IS_SMALLER, FLAG_BINARY_IS_SMALLER_OR_EQUAL, FLAG_BINARY_IS_GREATER,
                                   FLAG_BINARY_IS_GREATER_OR_EQUAL]):
            return self.gen_formula(join_var_node(node.identity), [l_expr[0], r_expr[0]], node['flags'][0],
                                    node[NODE_TYPE],
                                    node.identity, "boolean", ["number", "number"])
        elif node['flags'][0] in [FLAG_BINARY_BOOL_AND, FLAG_BINARY_BOOL_OR, FLAG_BINARY_BOOL_XOR,
                                  FLAG_BINARY_BITWISE_AND, FLAG_BINARY_BITWISE_XOR, FLAG_BINARY_BITWISE_OR]:  # 布尔运算
            return self.gen_formula(join_var_node(node.identity), [l_expr[0], r_expr[0]], node['flags'][0],
                                    node[NODE_TYPE],
                                    node.identity, "boolean", ["boolean", "boolean"])
        elif node['flags'][0] in [FLAG_BINARY_ADD, FLAG_BINARY_SUB, FLAG_BINARY_MUL, FLAG_BINARY_DIV, FLAG_BINARY_MOD,
                                  FLAG_BINARY_POW, FLAG_BINARY_SHIFT_RIGHT, FLAG_BINARY_SHIFT_LEFT]:  # 算术运算
            return self.gen_formula(join_var_node(node.identity), [l_expr[0], r_expr[0]], node['flags'][0],
                                    node[NODE_TYPE],
                                    node.identity, "number", ["number", "number"])
        elif (node['flags'][0] in [FLAG_BINARY_EQUAL, FLAG_BINARY_NOT_EQUAL, FLAG_BINARY_IS_IDENTICAL,
                                   FLAG_BINARY_IS_NOT_IDENTICAL]):  # 等号运算
            return self.gen_formula(join_var_node(node.identity), [l_expr[0], r_expr[0]], node['flags'][0],
                                    node[NODE_TYPE],
                                    node.identity, "boolean",
                                    [solve_type_conflict(l_expr[1], r_expr[1]),
                                     solve_type_conflict(l_expr[1], r_expr[1])])

    def manage_generic_node(self, node: py2neo.Node):
        """
        In a given test setting, this can be made
        to work with our solver, but to make this work across all
        platforms requires more engineering effort. Another issue
        is of deriving TAC formulas from graph nodes automatically.
        It is a challenging process that involves analyzing
        each AST node and supporting different node
        structures for each node type. For example, the left-hand
        side of an assignment statement in PHP can be a simple
        variable, a constant, a function call, nested function
        calls, etc. We have carefully considered these cases, and
        NAVEX has the support for most such node types and
        structures, yet there are a few instances still under development.
        """
        if node[NODE_TYPE] in {TYPE_CALL, TYPE_DIM, TYPE_VAR, TYPE_METHOD_CALL, TYPE_STATIC_CALL, TYPE_PROP, TYPE_ARRAY,
                               "string", "integer", "double", TYPE_CONST, TYPE_MAGIC_CONST, TYPE_STATIC_PROP,
                               TYPE_CLASS_CONST, TYPE_LIST, TYPE_GLOBAL,
                               TYPE_ARRAY_ELEM, TYPE_NULL, TYPE_REF}:
            return self.manage_basic_block(node)
        elif node[NODE_TYPE] in {TYPE_BINARY_OP}:  # 二元运算符
            return self.manage_binary_operation(node)
        elif node[NODE_TYPE] in {TYPE_UNARY_OP, TYPE_POST_INC, TYPE_POST_DEC, TYPE_PRE_INC, TYPE_PRE_DEC,
                                 TYPE_CAST}:  # 一元运算符
            return self.manage_unary_operation(node)
        elif node[NODE_TYPE] in {TYPE_CONDITIONAL}:  # 三目运算符
            return self.manage_condition_operation(node)
        elif node[NODE_TYPE] in {TYPE_ASSIGN, TYPE_ASSIGN_REF, TYPE_ASSIGN_OP, TYPE_STATIC}:
            return self.manage_assignment_operation(node)
        elif node[NODE_TYPE] == TYPE_EXPR_LIST:
            return self.manage_generic_node(self.analysis_framework.find_ast_child_nodes(node)[0])
        elif node[NODE_TYPE] == TYPE_ENCAPS_LIST:
            return self.manage_encapsulated_list(node)
            # 预定义函数的type
        elif node[NODE_TYPE] == TYPE_EXIT:
            return self.manage_exit_operation(node)
        elif node[NODE_TYPE] == TYPE_EMPTY:
            return self.manage_empty_operation(node)
        elif node[NODE_TYPE] == TYPE_ISSET:
            return self.manage_isset_operation(node)
        elif node[NODE_TYPE] == TYPE_UNSET:
            return self.manage_unset_operation(node)
        elif node[NODE_TYPE] in [TYPE_ECHO, TYPE_PRINT]:
            return self.manage_echo_operation(node)
        elif node[NODE_TYPE] == TYPE_INCLUDE_OR_EVAL and (
                set(node['flags']) & {FLAG_EXEC_INCLUDE, FLAG_EXEC_INCLUDE_ONCE, FLAG_EXEC_REQUIRE,
                                      FLAG_EXEC_REQUIRE_ONCE}):
            return self.manage_include_operation(node)
        elif node[NODE_TYPE] == TYPE_INCLUDE_OR_EVAL and (set(node['flags']) & {FLAG_EXEC_EVAL}):
            return self.manage_eval_operation(node)
        # 其他特殊类型
        elif node[NODE_TYPE] == TYPE_NEW:
            return self.manage_new_operation(node)
        elif node[NODE_TYPE] == TYPE_INSTANCEOF:
            return self.manage_instanceof_operation(node)
        elif node[NODE_TYPE] == TYPE_RETURN:
            return self.manage_return_operation(node)
        # FOR EACH
        elif node[NODE_TYPE] == TYPE_FOREACH:
            return self.manage_foreach_operation(node)
        elif node[NODE_TYPE] in {TYPE_BREAK, TYPE_PARAM, TYPE_CONTINUE}:  # BLACK LIST APIS
            if node[NODE_TYPE] == TYPE_BREAK:
                return "break", ""
            elif node[NODE_TYPE] == TYPE_PARAM:
                return self.manage_param_operation(node)
            elif node[NODE_TYPE] == TYPE_CONTINUE:
                return "continue", ""
        logger.warning("Get not support node type" + node.__str__())
        # not support : AST_PARAM
        return '', ''

    def manage_param_operation(self, node: py2neo.Node):
        if self.analysis_framework.get_ast_ith_child_node(node, i=2)[NODE_TYPE] == TYPE_NULL:
            return '', ''
        else:
            var, var_type = self.manage_generic_node(self.analysis_framework.get_ast_ith_child_node(node, i=1))
            value, value_type = self.manage_generic_node(self.analysis_framework.get_ast_ith_child_node(node, i=2))
            return self.gen_formula(left=var, right=[value], ltype=var_type, rtype=[value_type], op=TYPE_ASSIGN,
                                    node_type=TYPE_ASSIGN, node_id=node[NODE_INDEX], )

    def manage_foreach_operation(self, node: py2neo.Node):
        """
        Convert foreach($a as $v)  to $v = $a[0] CASE A
        Convert foreach($a as $k=>$v) to $v = $a[$k] CASE B
        :param node:
        :return:
        """
        a, a_type = self.manage_generic_node(self.analysis_framework.get_ast_ith_child_node(node, i=0))
        if self.analysis_framework.get_ast_ith_child_node(node, i=2)[NODE_TYPE] == TYPE_NULL:
            # CASE A
            v, v_type = self.manage_generic_node(self.analysis_framework.get_ast_ith_child_node(node, i=1))
            a, a_type = self.gen_formula(  # $a = $a[0] => $a = array_search(0,$a)
                left=a, right=[0, a], ltype='', rtype=['number', a_type], op='array_search', node_type=TYPE_CALL,
                node_id=node[NODE_INDEX]
            )
        else:
            # CASE A
            k, k_type = self.manage_generic_node(self.analysis_framework.get_ast_ith_child_node(node, i=1))
            v, v_type = self.manage_generic_node(self.analysis_framework.get_ast_ith_child_node(node, i=2))
            a, a_type = self.gen_formula(  # $a = $a[0] => $a = array_search(0,$a)
                left=a, right=[k, a], ltype='', rtype=[k_type, a_type], op='array_search', node_type=TYPE_CALL,
                node_id=node[NODE_INDEX]
            )
        return self.gen_formula(
            left=v, right=[a], ltype=v_type, rtype=[a_type], op=TYPE_ASSIGN, node_type=TYPE_ASSIGN,
            node_id=self.analysis_framework.get_ast_ith_child_node(node, i=1)[NODE_INDEX]
        )

    def manage_return_operation(self, node: py2neo.Node):
        return self.manage_generic_node(self.analysis_framework.find_ast_child_nodes(node)[0])

    def manage_condition_operation(self, node: py2neo.Node):
        # 三目运算符 别到时候碰到一个 ?? 我就吐了
        _the_three = self.analysis_framework.find_ast_child_nodes(node)
        condition_node, true_path_node, false_path_node = _the_three[0], _the_three[1], _the_three[2]
        condition_expr, condition_type = self.manage_generic_node(condition_node)
        true_expr, true_type = self.manage_generic_node(true_path_node)
        false_expr, false_type = self.manage_generic_node(false_path_node)
        return self.gen_formula(
            left=join_var_node(node.identity),
            right=[condition_expr, true_expr, false_expr],
            op=TYPE_CONDITIONAL,
            node_type=TYPE_CONDITIONAL,
            node_id=node.identity,
            ltype="string",
            rtype=[condition_type, true_type, false_type]
        )

    def manage_null(self, node: py2neo.Node):
        return "null", ""

    def manage_ref(self, node: py2neo.Node):
        # we ignore it !
        return self.manage_generic_node(self.analysis_framework.find_ast_child_nodes(node)[0])
        # var, var_type = self.manage_generic_node(
        # )
        # return self.gen_formula(
        #     left=join_var_node(node.identity),
        #     right=[var_type],
        #     op=TYPE_REF,
        #     node_type=TYPE_UNARY_OP,
        #     node_id=node.identity,
        #     ltype="string",
        #     rtype=[var_type]
        # )

    def manage_constant_string(self, node: py2neo.Node):
        if self.__global_abstract_level >= 1:
            return "T_STRING", "string"
        if 'code' not in node.keys():
            return "\"\"", "string"
        else:
            code = node['code']  # "\"" + addslashes(code.replace("'", "").replace("\"", "")) + "\""
            return "\"" + addslashes(code) + "\"", "string"

    def manage_constant_integer(self, node: py2neo.Node):
        if self.__global_abstract_level >= 1:
            return "T_NUMBER", "number"
        if 'code' not in node.keys():
            return 0, "number"
        else:
            return int(node['code']), "number"

    def manage_constant_double(self, node: py2neo.Node):
        if self.__global_abstract_level >= 1:
            return "T_NUMBER", "number"
        if 'code' not in node.keys():
            return 0.0, "number"
        else:
            return float(node['code']), "number"

    def manage_type_array(self, node: py2neo.Node):
        """
        for ast_array e.g.
        $a = array(
            $shaobao    => "level_1",
            $sky        => "level_10"
        )

        $t_1 , [$shaobao,'l'], AST_ARRAY_ELEM ,AST_ARRAY_ELEM
        $t_2 ,
        $t_3 , [$t_1,$t_2]  , AST_ARRAY, AST_ARRAY
        $a   , [t_2]        , AST_ASSIGN,AST_ASSIGN
        """
        if self.__global_abstract_level >= 1:
            return self.gen_formula(
                left=join_var_node(node.identity),
                right=["T_ARRAY"],
                op="array",
                node_type=TYPE_CALL,
                node_id=node.identity,
                ltype="",
                rtype=["STRING"]
            )
        args = self.analysis_framework.find_ast_child_nodes(node)  # child node's type is array elem
        resolved_array_elem = []
        resolved_array_elem_types = []
        for arg in args:
            assert isinstance(arg, py2neo.Node)
            arg_expr, arg_type = self.manage_generic_node(arg)
            resolved_array_elem.append(arg_expr)
            resolved_array_elem_types.append(arg_type)
        return self.gen_formula(
            left=join_var_node(node.identity),
            right=resolved_array_elem,
            op="array",
            node_type=TYPE_CALL,
            node_id=node.identity,
            ltype="",
            rtype=resolved_array_elem_types
        )

    def manage_type_array_elem(self, node: py2neo.Node):
        assert node[NODE_TYPE] == TYPE_ARRAY_ELEM
        if self.analysis_framework.get_ast_ith_child_node(node, 1)['type'] == 'NULL':
            array_node = self.analysis_framework.ast_step.get_parent_node(node)
            ith_node = self.analysis_framework.find_ast_child_nodes(array_node).index(node)
            key_expr, key_type = ith_node, 'number'
            value_expr, value_type = self.manage_generic_node(self.analysis_framework.get_ast_child_node(node))
        else:
            key_expr, key_type = self.manage_generic_node(self.analysis_framework.get_ast_ith_child_node(node, 1))
            value_expr, value_type = self.manage_generic_node(self.analysis_framework.get_ast_ith_child_node(node, 0))
        return self.gen_formula(
            left=join_var_node(node.identity),
            right=[key_expr, value_expr],
            op=TYPE_ARRAY_ELEM,
            node_type=TYPE_BINARY_OP,
            node_id=node.identity,
            ltype="",
            rtype=[key_type, value_type]
        )

    def manage_class_constant(self, node: py2neo.Node):
        code = self.analysis_framework.code_step.get_ast_class_const_code(node)
        return self.gen_formula(
            left=join_var_node(node.identity),
            right=[code],
            op=node[NODE_TYPE],
            node_type=node[NODE_TYPE],
            node_id=node.identity,
            ltype="string",
            rtype=['string']
        )

    def manage_magic_constant(self, node: py2neo.Node):
        return MAGIC_CONST_CONVERT_DICT[node['flags'][0]], "string"

    def manage_generic_constant(self, node: py2neo.Node):
        code = self.analysis_framework.code_step.get_ast_const_code(node)
        if code.lower() == "true":
            return True, "boolean"
        elif code.lower() == "false":
            return False, "boolean"
        else:
            return self.gen_formula(
                left=join_var_node(node.identity),
                right=[code],
                op=node[NODE_TYPE],
                node_type=node[NODE_TYPE],
                node_id=node.identity,
                ltype="string",
                rtype=['string']
            )

    def manage_unary_operation(self, node: py2neo.Node):
        expr, expr_type = self.manage_generic_node(self.analysis_framework.find_ast_child_nodes(node)[0])
        if node[NODE_TYPE] == 'AST_UNARY_OP' and set(node['flags']) & {FLAG_UNARY_SILENCE}:
            return expr, expr_type
        if node[NODE_TYPE] == 'AST_UNARY_OP' and set(node['flags']) & {"UNARY_BOOL_NOT"}:
            return self.gen_formula(join_var_node(node.identity), [expr], node['flags'][0], node[NODE_TYPE],
                                    node.identity,
                                    "boolean", ["boolean"])
        elif node[NODE_TYPE] == 'AST_UNARY_OP' and node['flags'][0] == "UNARY_MINUS":
            return self.gen_formula(join_var_node(node.identity), [expr], node['flags'][0], node[NODE_TYPE],
                                    node.identity,
                                    "number", ["number"])

        elif node[NODE_TYPE] == 'AST_POST_INC':
            self.gen_formula(join_var_node(node.identity), [expr], TYPE_ASSIGN, TYPE_ASSIGN, node.identity, "number",
                             ["number"])
            return self.gen_formula(expr, [expr, 1], 'BINARY_ADD', TYPE_BINARY_OP, node.identity, "number",
                                    ["number", "number"])

        elif node[NODE_TYPE] == 'AST_POST_DEC':
            self.gen_formula(join_var_node(node.identity), [expr], TYPE_ASSIGN, TYPE_ASSIGN, node.identity, "number",
                             ["number"])
            return self.gen_formula(expr, [expr, 1], 'BINARY_SUB', TYPE_BINARY_OP, node.identity, "number",
                                    ["number", "number"])

        elif node[NODE_TYPE] == 'AST_PRE_INC':
            return self.gen_formula(expr, [expr, 1], 'BINARY_ADD', TYPE_BINARY_OP, node.identity, "number",
                                    ["number", "number"])

        elif node[NODE_TYPE] == 'AST_PRE_DEC':
            return self.gen_formula(expr, [expr, 1], 'BINARY_SUB', TYPE_BINARY_OP, node.identity, "number",
                                    ["number", "number"])

        elif node[NODE_TYPE] == TYPE_CAST:
            if node['flags'][0] in {FLAG_TYPE_LONG}:
                return self.gen_formula(expr, [expr], 'intval', TYPE_CALL, node.identity, "number", ["number"])
            elif node['flags'][0] in {FLAG_TYPE_DOUBLE}:
                return self.gen_formula(expr, [expr], 'floatval', TYPE_CALL, node.identity, "number", ["number"])
            elif node['flags'][0] in {FLAG_TYPE_STRING}:
                return self.gen_formula(expr, [expr], 'strval', TYPE_CALL, node.identity, "string", ["string"])
            elif node['flags'][0] in {FLAG_TYPE_BOOL}:
                return self.gen_formula(expr, [expr], 'boolval', TYPE_CALL, node.identity, "boolean", ["boolean"])
            elif node['flags'][0] in {FLAG_TYPE_OBJECT}:
                return self.gen_formula(expr, [expr], '(object)', TYPE_CALL, node.identity, "", [""])
            elif node['flags'][0] in {FLAG_TYPE_ARRAY}:
                return self.gen_formula(expr, [expr], '(array)', TYPE_CALL, node.identity, "", [""])
            else:
                logger.warning(f"not support cast type {node['flags']} , use strval instead")
                return self.gen_formula(expr, [expr], 'strval', TYPE_CALL, node.identity, "string", ["string"])

    def manage_assignment_operation(self, node: py2neo.Node):
        assert not set(node[NODE_TYPE]) & {TYPE_ASSIGN, TYPE_ASSIGN_REF, TYPE_ASSIGN_OP}
        l_expr = self.manage_generic_node(self.analysis_framework.find_ast_child_nodes(node)[0])
        r_expr = self.manage_generic_node(self.analysis_framework.find_ast_child_nodes(node)[1])
        if node[NODE_TYPE] == TYPE_ASSIGN_REF:
            return self.gen_formula(
                left=l_expr[0], right=[r_expr[0]], op=TYPE_ASSIGN, node_type=TYPE_ASSIGN, node_id=node.identity,
                ltype=solve_type_conflict(l_expr[1], r_expr[1]), rtype=[solve_type_conflict(l_expr[1], r_expr[1])],
            )
            # raise SymbolicTrackingUnsupportedError(node[NODE_TYPE])
        if node[NODE_TYPE] in {TYPE_ASSIGN, TYPE_STATIC}:
            return self.gen_formula(
                left=l_expr[0], right=[r_expr[0]], op=TYPE_ASSIGN, node_type=TYPE_ASSIGN, node_id=node.identity,
                ltype=solve_type_conflict(l_expr[1], r_expr[1]), rtype=[solve_type_conflict(l_expr[1], r_expr[1])],
            )
        elif node[NODE_TYPE] == TYPE_ASSIGN_OP:
            if node['flags'][0] in {FLAG_BINARY_CONCAT}:
                tmp_expr = self.gen_formula(
                    left=join_var_node(node.identity),
                    right=[l_expr[0], r_expr[0]],
                    op=node['flags'][0],
                    node_type=TYPE_BINARY_OP,
                    node_id=node.identity,
                    ltype='string',
                    rtype=['string', 'string']
                )
                return self.gen_formula(
                    left=l_expr[0], right=[tmp_expr[0]], op=node[NODE_TYPE], node_type=TYPE_ASSIGN,
                    node_id=node.identity,
                    ltype=solve_type_conflict(l_expr[1], tmp_expr[1]),
                    rtype=[solve_type_conflict(l_expr[1], tmp_expr[1])],
                )
            elif node['flags'][0] in {FLAG_BINARY_BITWISE_AND, FLAG_BINARY_BITWISE_XOR, FLAG_BINARY_BITWISE_OR}:
                tmp_expr = self.gen_formula(join_var_node(node.identity), [l_expr[0], r_expr[0]], node['flags'][0],
                                            TYPE_BINARY_OP, node.identity, "boolean", ["boolean", "boolean"])
                return self.gen_formula(l_expr[0], [tmp_expr[0]], node['flags'][0],
                                        TYPE_ASSIGN, node.identity, "boolean", [tmp_expr[1]])
            elif node['flags'][0] in {FLAG_BINARY_ADD, FLAG_BINARY_SUB, FLAG_BINARY_MUL, FLAG_BINARY_DIV,
                                      FLAG_BINARY_MOD, FLAG_BINARY_POW, FLAG_BINARY_SHIFT_LEFT,
                                      FLAG_BINARY_SHIFT_RIGHT}:
                tmp_expr = self.gen_formula(join_var_node(node.identity), [l_expr[0], r_expr[0]], node['flags'][0],
                                            TYPE_BINARY_OP, node.identity, "number", ["number", "number"])
                return self.gen_formula(l_expr[0], [tmp_expr[0]], node['flags'][0],
                                        TYPE_ASSIGN, node.identity, "number", [tmp_expr[1]])
            else:
                raise Exception(node[NODE_TYPE])
        else:
            raise Exception(node[NODE_TYPE])

    def manage_echo_operation(self, node: py2neo.Node):
        expr = self.manage_generic_node(self.analysis_framework.find_ast_child_nodes(node)[0])
        return self.gen_formula(
            left=join_var_node(node.identity),
            right=[expr[0]],
            op='echo',
            node_type=TYPE_CALL,
            node_id=node.identity,
            ltype="string",
            rtype=["string"]
        )

    def manage_unset_operation(self, node: py2neo.Node):
        expr = self.manage_generic_node(self.analysis_framework.find_ast_child_nodes(node)[0])
        return self.gen_formula(
            left=join_var_node(node.identity),
            right=[expr[0]],
            op='unset',
            node_type=TYPE_CALL,
            node_id=node.identity,
            ltype="boolean",
            rtype=[expr[1]]
        )

    def manage_isset_operation(self, node: py2neo.Node):
        expr = self.manage_generic_node(self.analysis_framework.find_ast_child_nodes(node)[0])
        return self.gen_formula(
            left=join_var_node(node.identity),
            right=[expr[0]],
            op='isset',
            node_type=TYPE_CALL,
            node_id=node.identity,
            ltype="boolean",
            rtype=[expr[1]]
        )

    def manage_encapsulated_list(self, node: py2neo.Node):
        pre_tmp = None
        __nodes = self.analysis_framework.find_ast_child_nodes(node)
        for __node in __nodes:
            expr = self.manage_generic_node(__node)
            if pre_tmp is None:
                pre_tmp = expr[0]
            else:
                pre_tmp, _ = self.gen_formula(
                    left=join_var_node(node.identity, ADD_ENC_FLAG=True),
                    right=[pre_tmp, expr[0]],
                    op='BINARY_CONCAT',
                    node_type="AST_BINARY_OP",
                    node_id=node.identity,
                    ltype="string",
                    rtype=["string", "string"]
                )
        assert pre_tmp is not None
        return pre_tmp, "string"

    def manage_static_function_call(self, node: py2neo.Node):
        args = self.analysis_framework.ast_step.find_function_arg_node_list(node)
        resolved_args = []
        resolved_args_types = []
        for arg in args:
            assert isinstance(arg, py2neo.Node)
            res_arg = self.manage_generic_node(arg)
            resolved_args.append(res_arg[0])
            resolved_args_types.append(res_arg[1])
        return self.gen_formula(
            left=join_var_node(node.identity),
            right=resolved_args,
            op=self.analysis_framework.code_step.get_static_call_code(node),
            node_type=TYPE_STATIC_CALL,
            node_id=node.identity,
            ltype="string",
            rtype=resolved_args_types
        )

    def manage_dynamic_function_call(self, node: py2neo.Node):
        """
        $a->func($b,$c) ===>
        L : $t_id
        R : func($a,$b,$c)
        特殊处理，将dy_func的第一位参数扩展为 $
        """
        args = self.analysis_framework.ast_step.find_function_arg_node_list(node)
        resolved_args = []
        resolved_args_types = []
        for arg in args:
            assert isinstance(arg, py2neo.Node)
            res_arg = self.manage_generic_node(arg)
            resolved_args.append(res_arg[0])
            resolved_args_types.append(res_arg[1])
        var_node = self.analysis_framework.get_ast_child_node(node)
        var_expr, var_type = self.manage_generic_node(var_node)
        resolved_args = [var_expr] + resolved_args
        resolved_args_types = [var_type] + resolved_args_types
        return self.gen_formula(
            left=join_var_node(node.identity),
            right=resolved_args,
            op=self.analysis_framework.code_step.get_ast_method_call_code(node),
            node_type=TYPE_METHOD_CALL,
            node_id=node.identity,
            ltype="string",
            rtype=resolved_args_types
        )

    def manage_include_operation(self, node: py2neo.Node):
        expr = self.manage_generic_node(self.analysis_framework.find_ast_child_nodes(node)[0])
        return self.gen_formula(
            left=join_var_node(node.identity),
            right=[expr[0]],
            op='include',
            node_type=TYPE_CALL,
            node_id=node.identity,
            ltype="boolean",
            rtype=["string"]
        )

    def manage_eval_operation(self, node: py2neo.Node):
        expr = self.manage_generic_node(self.analysis_framework.get_ast_child_node(node))
        return self.gen_formula(
            left=join_var_node(node.identity),
            right=[expr[0]],
            op='eval',
            node_type=TYPE_CALL,
            node_id=node.identity,
            ltype="",
            rtype=["string"]
        )

    def manage_type_prop(self, node: py2neo.Node):
        """
        $a->file
        get_param($a,'file')
        L : $t_0
        R : get_param($a,'file')
        """
        resolved_args = []
        resolved_args_types = []
        args = self.analysis_framework.find_ast_child_nodes(node)
        for arg in args:
            assert isinstance(arg, py2neo.Node)
            res_arg = self.manage_generic_node(arg)
            resolved_args.append(res_arg[0])
            resolved_args_types.append(res_arg[1])
        return self.gen_formula(
            left=join_var_node(node.identity),
            right=resolved_args,
            op=TYPE_PROP,
            node_type=TYPE_PROP,
            node_id=node.identity,
            ltype="string",
            rtype=resolved_args_types
        )
