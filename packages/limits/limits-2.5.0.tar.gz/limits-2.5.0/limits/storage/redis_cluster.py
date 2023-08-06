import urllib
import warnings
from typing import Any, List, Tuple

from deprecated.sphinx import versionchanged
from packaging.version import Version

from ..errors import ConfigurationError
from .redis import RedisStorage


@versionchanged(
    version="2.5.0",
    reason="""
Cluster support was provided by the :pypi:`redis-py-cluster` library
which has been absorbed into the official :pypi:`redis` client. By
default the :class:`~redis.cluster.RedisCluster` client will be used
however if the version of the package is lower than ``4.2.0`` the implementation
will fallback to trying to use :class:`rediscluster.RedisCluster`.
""",
)
class RedisClusterStorage(RedisStorage):
    """
    Rate limit storage with redis cluster as backend

    Depends on :pypi:`redis`.
    """

    STORAGE_SCHEME = ["redis+cluster"]
    """The storage scheme for redis cluster"""

    DEFAULT_OPTIONS = {
        "max_connections": 1000,
    }
    "Default options passed to the :class:`~redis.cluster.RedisCluster`"

    DEPENDENCIES = {"redis": Version("4.2.0"), "rediscluster": Version("2.0.0")}
    FAIL_ON_MISSING_DEPENDENCY = False

    def __init__(self, uri: str, **options):
        """
        :param uri: url of the form
         ``redis+cluster://[:password]@host:port,host:port``
        :param options: all remaining keyword arguments are passed
         directly to the constructor of :class:`redis.cluster.RedisCluster`
        :raise ConfigurationError: when the :pypi:`redis` library is not
         available or if the redis cluster cannot be reached.
        """
        parsed = urllib.parse.urlparse(uri)
        cluster_hosts = []
        for loc in parsed.netloc.split(","):
            host, port = loc.split(":")
            cluster_hosts.append((host, int(port)))

        self.storage = None
        self.using_redis_py = False
        self.__pick_storage(cluster_hosts, **{**self.DEFAULT_OPTIONS, **options})
        assert self.storage
        self.initialize_storage(uri)
        super(RedisStorage, self).__init__()

    def __pick_storage(self, cluster_hosts: List[Tuple[str, int]], **options: Any):
        redis_py = self.dependencies["redis"]
        if redis_py:
            startup_nodes = [redis_py.cluster.ClusterNode(*c) for c in cluster_hosts]
            self.storage = redis_py.cluster.RedisCluster(
                startup_nodes=startup_nodes, **options
            )
            self.using_redis_py = True
            return

        self.__use_legacy_cluster_implementation(cluster_hosts, **options)

        if not self.storage:
            raise ConfigurationError(
                (
                    "Unable to find an implementation for redis cluster"
                    " Cluster support requires either redis-py>=4.2 or"
                    " redis-py-cluster"
                )
            )  # pragma: no cover

    def __use_legacy_cluster_implementation(self, cluster_hosts, **options):
        redis_cluster = self.dependencies["rediscluster"]
        if redis_cluster:
            warnings.warn(
                (
                    "Using redis-py-cluster is deprecated as the library has been"
                    " absorbed by redis-py (>=4.2). The support will be eventually "
                    " removed from the limits library and will no longer be tested "
                    " against beyond limits version: 2.6. To get rid of this warning, "
                    " uninstall redis-py-cluster and ensure redis-py>=4.2.0 is installed"
                )
            )
            self.storage = redis_cluster.RedisCluster(
                startup_nodes=[{"host": c[0], "port": c[1]} for c in cluster_hosts],
                **options
            )

    def reset(self) -> int:
        """
        Redis Clusters are sharded and deleting across shards
        can't be done atomically. Because of this, this reset loops over all
        keys that are prefixed with 'LIMITER' and calls delete on them, one at
        a time.

        .. warning::
         This operation was not tested with extremely large data sets.
         On a large production based system, care should be taken with its
         usage as it could be slow on very large data sets"""

        if self.using_redis_py:
            count = 0
            for primary in self.storage.get_primaries():
                node = self.storage.get_redis_connection(primary)
                keys = node.keys("LIMITER*")
                count += sum([node.delete(k.decode("utf-8")) for k in keys])
            return count
        else:
            keys = self.storage.keys("LIMITER*")
            return sum([self.storage.delete(k.decode("utf-8")) for k in keys])
