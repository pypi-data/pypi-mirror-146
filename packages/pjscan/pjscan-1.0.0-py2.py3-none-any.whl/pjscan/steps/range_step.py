from typing import List, Union, Dict, Set, Tuple
import py2neo
from .abstract_step import AbstractStep
from pjscan.const import *
import logging

logger = logging.getLogger(__name__)


class RangeStep(AbstractStep):
    def __init__(self, parent):
        super().__init__(parent, "range_step")

    def get_ast_method_range(self, node: py2neo.Node) -> Tuple[int, int]:
        """Given AST_METHOD node and return the node range belongs to this METHOD
        """
        assert node[NODE_TYPE] == TYPE_METHOD
        RR = self.parent.basic_step.match_first(LABEL_AST,
                                                **{NODE_FILEID: node[NODE_FILEID], NODE_LINENO: node[NODE_ENDLINENO]})
        if not RR:
            RR = self.parent.basic_step.match_first(LABEL_AST, **{NODE_FILEID: node[NODE_FILEID],
                                                                  NODE_LINENO: node[NODE_ENDLINENO] - 1})
        if not RR:
            logger.fatal("endlineno is wriong or need enhancement")
        end_line_root_node = self.parent.basic_step.get_ast_root_node(RR)
        last_node = self.parent.basic_step.filter_ast_child_nodes(end_line_root_node)[-1]
        return node[NODE_INDEX], last_node[NODE_INDEX]
