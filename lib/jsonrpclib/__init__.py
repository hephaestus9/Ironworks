from lib.jsonrpclib.config import Config
config = Config.instance()
from lib.jsonrpclib.history import History
history = History.instance()
from lib.jsonrpclib.jsonrpc import Server, MultiCall, Fault
from lib.jsonrpclib.jsonrpc import ProtocolError, loads, dumps
