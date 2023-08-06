from pjscan.cache.prefetch_thread import *


class PrefetchThreadPool(object):
    def __init__(self, cache_pool: BasicCacheGraph,
                 graph: py2neo.Graph,
                 astThreadCount: int = 0, cfgThreadCount: int = 0, pdgThreadCount: int = 0, cgThreadCount: int = 0,
                 **kwargs):
        """PrefetchThreadPool is the manager of all the PrefetchThreads

        PrefetchThreadPool will be created in AnalysisFramework instance , with the input prefetch_setting

        PrefetchThreadPool contains 4 kind of PrefetchThread,

        Attributes
        ----------
        cache_pool : BasicCacheGraph
            the cache_graph ref
        graph : py2neo.Graph
            the AnalysisFramework.neo4j_graph ref
        astQueue : queue.Queue
            stores ast-related nodes , astTreads will get node from this query and do `prefetch` function
        cfgQueue : queue.Queue
            stores cfg-related nodes , cfgTreads will get node from this query and do `prefetch` function
        pdgQueue : queue.Queue
            stores pdg-related nodes , pdgThreads will get node from this query and do `prefetch` function
        cgQueue : queue.Queue
            stores cg-related nodes , cgThreads will get node from this query and do `prefetch` function
        astThreads :  List[BasePrefetchThread]
            List of ast threads, get input from astQueue
        cfgThreads :  List[BasePrefetchThread]
            List of cfg threads, get input from cfgQueue
        pdgThreads :  List[BasePrefetchThread]
            List of pdg threads, get input from pdgQueue
        cgThreads :  List[BasePrefetchThread]
            List of cg threads, get input from cgQueue

        Method
        ------
        start_all()
            start all the thread

        stop_all()
            stop all the thread

        put_entity()
            difinite how to put the node in queue

        Notes
        -----
        This is a demo of thread pool.
        You can write your own thread pool according to your need,
        include queues,threads and put_entity() method

        """
        self.cache_pool = cache_pool
        self.graph = graph
        self.astQueue = queue.Queue()
        self.cfgQueue = queue.Queue()
        self.pdgQueue = queue.Queue()
        self.cgQueue = queue.Queue()
        self.astThreads: List[BasePrefetchThread] = []
        self.cfgThreads: List[BasePrefetchThread] = []
        self.pdgThreads: List[BasePrefetchThread] = []
        self.cgThreads: List[BasePrefetchThread] = []  # TODO 这些应该是线程池（threadpool实现，而不是 thread列表实现)
        if astThreadCount > 0:
            for i in range(astThreadCount):
                prefetch_thread_configure = kwargs.get("ast_prefetch_thread_configure", {})
                prefetch_thread_instance = prefetch_thread_configure.pop("class_name", AstBasePrefetchThread)
                thread = prefetch_thread_instance(self.astQueue, self.graph, self.cache_pool,
                                                  **prefetch_thread_configure)
                self.astThreads.append(thread)
                thread.daemon = True
                # thread.join()

        if cfgThreadCount > 0:
            for i in range(cfgThreadCount):
                prefetch_thread_configure = kwargs.get("cfg_prefetch_thread_configure", {})
                prefetch_thread_instance = prefetch_thread_configure.pop("class_name", CfgBasePrefetchThread)
                thread = prefetch_thread_instance(self.astQueue, self.graph, self.cache_pool,
                                                  **prefetch_thread_configure)
                self.cfgThreads.append(thread)
                thread.daemon = True
                # thread.join()

        if pdgThreadCount > 0:
            for i in range(pdgThreadCount):
                prefetch_thread_configure = kwargs.get("pdg_prefetch_thread_configure", {})
                prefetch_thread_instance = prefetch_thread_configure.pop("class_name", PdgBasePrefetchThread)
                thread = prefetch_thread_instance(self.astQueue, self.graph, self.cache_pool,
                                                  **prefetch_thread_configure)
                self.pdgThreads.append(thread)
                thread.daemon = True
                # thread.join()

        if cgThreadCount > 0:
            for i in range(cgThreadCount):
                prefetch_thread_configure = kwargs.get("cg_prefetch_thread_configure", {})
                prefetch_thread_instance = prefetch_thread_configure.pop("class_name", CgBasePrefetchThread)
                thread = prefetch_thread_instance(self.astQueue, self.graph, self.cache_pool,
                                                  **prefetch_thread_configure)
                self.cgThreads.append(thread)
                thread.daemon = True
                # thread.join()

        self.start_all()

    def start_all(self):
        """Start all the thread

        """
        for i in self.astThreads:
            i.start()
        for i in self.cfgThreads:
            i.start()
        for i in self.pdgThreads:
            i.start()
        for i in self.cgThreads:
            i.start()

    def __del__(self):
        self.stop_all()

    def stop_all(self) -> None:
        """Stop all the thread

        """
        # stop all the thread
        for i in self.astThreads:
            i.stop()
        for i in self.cfgThreads:
            i.stop()
        for i in self.pdgThreads:
            i.stop()
        for i in self.cgThreads:
            i.stop()

    def put_entity(self, res:List[py2neo.Node]):
        '''Put the entity to corresponding Queue.
        which will be used for prefetchThread query.

        Notes
        -----

        `put_entity` function will be called to put the given list of node to `self.xxxQueue`
        This method is called in each step.

        Parameters
        ----------
        res : List[py2neo.Node]
        '''
        for node in res:
            self.pdgQueue.put(node)
            self.cfgQueue.put(node)
            self.astQueue.put(node)
            self.cgQueue.put(node)
