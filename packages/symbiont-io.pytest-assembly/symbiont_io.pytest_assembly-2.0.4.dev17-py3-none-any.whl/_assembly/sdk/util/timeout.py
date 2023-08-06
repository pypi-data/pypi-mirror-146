from contextlib import contextmanager


@contextmanager
def network_timeout_as(ka, timeout):
    """Manually set the network timeout globally."""
    old_timeout = ka.network_client.timeout
    ka.network_client.timeout = timeout
    yield
    ka.network_client.timeout = old_timeout
