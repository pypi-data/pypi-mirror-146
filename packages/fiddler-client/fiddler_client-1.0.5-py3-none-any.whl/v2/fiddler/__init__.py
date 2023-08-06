import logging

from client.v2.fiddler.api.api import Client  # noqa

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
