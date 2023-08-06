import copy
import queue
import threading, time
from abc import abstractmethod, ABC
from queue import Queue
from pjscan.const import *
from pjscan.cache.cache_graph import *
from pjscan.neo4j_defauilt_config import *
from typing import *
import py2neo

"""
        可以扩展do_prefetch方法执行特定的预查询策略
"""


class BasePrefetchThread(threading.Thread, ABC):
    '''

    Attributes
    ----------

    queue: queue.Queue
        the queue that the thread fetch the node from

    graph: py2neo.Graph
        the connect to neo4j database

    cache_graph : cache_graph.BasicCacheGraph
        use the cache pool to record the result of prefetch

    Method
    ------
    run()
        the prefetch thread fetch the node from the queue and do your prefetch

    prefetch()
        difinite your prefetch method in this function, include whether do it and how to do that

    stop()
        stop the thread

    Examples
    --------

    This is an example of how to override the prefetch() method.
    You want to prefetch about the PDG relationship,
    and you use the drop out strategy to judge whether the thread should prefetch,
    then difinite the query of database

    >>>  def prefetch(self, node):
    ...      if random.randint(0, 100) * 0.01 >= self.drop_out:
    ...          return
    ...      if node[NODE_TYPE] not in AST_ROOT:
    ...          return
    ...      if self.cache_graph.get_pdg_inflow(node) is None:
    ...          rels = self.graph.relationships.match(nodes=[None, node], r_type=DATA_FLOW_EDGE, ).all()
    ...          self.cache_graph.add_pdg_inflow(node, rels)
    ...      if self.cache_graph.get_pdg_outflow(node) is None:
    ...          rels = self.graph.relationships.match(nodes=[node, None], r_type=DATA_FLOW_EDGE, ).all()
    ...          self.cache_graph.add_pdg_outflow(node, rels)

    Notes
    -----
    You can extend this method your self.

    Otherwise, we provide 4 class which extends it , which used for prefetch different relationships

    You can use it as
        AstBasePrefetchThread

        CfgBasePrefetchThread

        PdgBasePrefetchThread

        CgBasePrefetchThread

    '''

    @abstractmethod
    def __init__(self, queue: Queue, neo4j_graph: py2neo.Graph, cache_graph: BasicCacheGraph, *args, **kwargs):
        """Initial the prefetch thread

        Parameters
        ----------
        new_connector : bool
            if new_connector is True, the thread will establish a new connect with database

        queue : queue.Queue
            queue to be queried

        cache_graph : BasicCacheGraph
            the cache to store prefetch result

        """
        new_connector = kwargs.get("new_connector", True)
        super(BasePrefetchThread, self).__init__()
        self.running = True
        self.queue = queue
        self.cache_graph = cache_graph
        if new_connector:
            self.graph = py2neo.Graph(neo4j_graph.service.profile.uri, auth=neo4j_graph.service.profile.auth)
        else:
            self.graph = neo4j_graph

    def run(self):
        """Fetch a node from queue, and do the prefetch step

        """
        self.running = True
        while self.running:
            node = self.queue.get()
            self.prefetch(node)

    @abstractmethod
    def prefetch(self, node):
        """You should extend this class, and rewrite this method to difinite your prefetch step

        """
        raise NotImplementedError()

    def stop(self):
        """Stop the prefetch thread

        """
        self.running = False


class AstBasePrefetchThread(BasePrefetchThread):

    def __init__(self, *args, **kwargs):
        """

        Parameters
        ----------
        args
        kwargs
        """
        super(AstBasePrefetchThread, self).__init__(*args, **kwargs)

    def prefetch(self, node):
        """Do the prefetch step to query ast relationship of a node

        Parameters
        ----------
        node : py2neo.Node

        """
        self.cache_graph.add_node(node)
        if self.cache_graph.get_ast_inflow(node) is None:
            rels = self.graph.relationships.match(nodes=[None, node], r_type=AST_EDGE, ).all()
            self.cache_graph.add_ast_inflow(node, rels)
        if self.cache_graph.get_ast_outflow(node) is None:
            rels = self.graph.relationships.match(nodes=[node, None], r_type=AST_EDGE, ).all()
            self.cache_graph.add_ast_outflow(node, rels)


class CfgBasePrefetchThread(BasePrefetchThread):
    def __init__(self, *args, **kwargs):
        """

        Parameters
        ----------
        args
        kwargs
        """
        super(CfgBasePrefetchThread, self).__init__(*args, **kwargs)

    def prefetch(self, node):
        """Do the prefetch step to query cfg relationship of a node

        Parameters
        ----------
        node : py2neo.Node

        """
        self.cache_graph.add_node(node)
        if self.cache_graph.get_cfg_inflow(node) is None:
            rels = self.graph.relationships.match(nodes=[None, node], r_type=CFG_EDGE, ).all()
            self.cache_graph.add_cfg_inflow(node, rels)
        if self.cache_graph.get_cfg_outflow(node) is None:
            rels = self.graph.relationships.match(nodes=[node, None], r_type=CFG_EDGE, ).all()
            self.cache_graph.add_cfg_outflow(node, rels)


class PdgBasePrefetchThread(BasePrefetchThread):
    def __init__(self, *args, **kwargs):
        """

        Parameters
        ----------
        args
        kwargs
        """
        super(PdgBasePrefetchThread, self).__init__(*args, **kwargs)

    def prefetch(self, node):
        """Do the prefetch step to query pdg relationship of a node

        Parameters
        ----------
        node : py2neo.Node

        """
        if node[NODE_TYPE] in AST_ROOT:
            self.cache_graph.add_node(node)
            if self.cache_graph.get_pdg_inflow(node) is None:
                # TODO I NEED TO LABEL WHICH IS AST_ROOT.
                rels = self.graph.relationships.match(nodes=[None, node], r_type=DATA_FLOW_EDGE, ).all()
                self.cache_graph.add_pdg_inflow(node, rels)
            if self.cache_graph.get_pdg_outflow(node) is None:
                rels = self.graph.relationships.match(nodes=[node, None], r_type=DATA_FLOW_EDGE, ).all()
                self.cache_graph.add_pdg_outflow(node, rels)


class CgBasePrefetchThread(BasePrefetchThread):
    def __init__(self, *args, **kwargs):
        """

        Parameters
        ----------
        args
        kwargs
        """
        super(CgBasePrefetchThread, self).__init__(*args, **kwargs)

    def prefetch(self, node):
        """Do the prefetch step to query cg relationship of a node

        Parameters
        ----------
        node : py2neo.Node

        """
        self.cache_graph.add_node(node)
        if self.cache_graph.get_cg_inflow(node) is None:
            rels = self.graph.relationships.match(nodes=[None, node], r_type=CALLS_EDGE, ).all()
            self.cache_graph.add_cg_inflow(node, rels)
        if self.cache_graph.get_cg_outflow(node) is None:
            rels = self.graph.relationships.match(nodes=[node, None], r_type=CALLS_EDGE, ).all()
            self.cache_graph.add_cg_outflow(node, rels)


