from typing import List, Union, Dict, Set
import py2neo
from pjscan.const import *
from .abstract_step import AbstractStep


class CHGStep(AbstractStep):
    def __init__(self, parent):
        super().__init__(parent, "chg_step")

    def get_class_defined_node_by_name(self, name: str):
        """
        根据类名，找到类定义节点

        :param name:
        """
        return self.parent.neo4j_graph.nodes.match("AST").where(
            f"_.name='{name}' AND _.type='AST_CLASS'"
        ).first()

    def get_class_construct_function(self, node: py2neo.Node):
        """
        根据类定义节点，找到类构造方法

        :param node:
        """
        class_top_level_node = self.parent.find_ast_child_nodes(node, include_type=[TYPE_TOPLEVEL])[0]
        class_stmt_list_node = self.parent.find_ast_child_nodes(class_top_level_node, include_type=[TYPE_STMT_LIST])[0]
        for i in self.parent.find_ast_child_nodes(class_stmt_list_node, include_type=[TYPE_METHOD]):
            if i[NODE_NAME] == "__construct":
                return i
        return None
