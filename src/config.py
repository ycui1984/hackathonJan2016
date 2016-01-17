import logging
import socket
import os
import sys

HULU_ENV = os.environ.get("HULU_ENV", "dev")
HULU_DC = os.environ.get("HULU_DC", "els")
DONKI = os.getenv("DONKI", False)
SERVICE_NAME = "hackathonyan"
DOPPLER_NAME = "hackathonyan"

HOSTNAME = socket.gethostname()
BANC_PORT = os.getenv("BANC_PORT")
BANC_HOST = "127.0.0.1"
if HULU_ENV == "els":
    BANC_HOST = "bank.els.prod.hulu.com"
elif HULU_ENV == "iad":
    BANC_HOST = "bank.iad.prod.hulu.com"

if (HULU_DC, HULU_ENV) == ("els", "prod"):
    DOPPLER_HOST = "doppler-ingest.els.prod.hulu.com"
    REDIS_URL, REDIS_PORT = "monaco-db.els.prod.hulu.com", 6720

elif (HULU_DC, HULU_ENV) == ("els", "stage"):
    DOPPLER_HOST = "doppler-ingest.iad.prod.hulu.com"
    REDIS_URL, REDIS_PORT = "monaco-db.els.prod.hulu.com", 6595

elif (HULU_DC, HULU_ENV) == ("els", "dev") or (HULU_DC, HULU_ENV) == ("els", "test"):
    DOPPLER_HOST = None
    REDIS_URL, REDIS_PORT = "127.0.0.1", 6379

else:
    raise Exception("Invalid Config Requested: HULU_DC = %s and HULU_ENV = %s" % (HULU_DC, HULU_ENV))

# Setup Stats #
from hpc.metrics_client import get_stats
track_stats = get_stats(SERVICE_NAME, HULU_ENV, HULU_DC, BANC_HOST, BANC_PORT,
                        no_send=HULU_ENV in ["test", "dev"])

def setup_logging():
    from hpc.requeststore import ContextFilter
    format = logging.Formatter('%(asctime)s : {0} : <%(process)d> : %(name)-12s : Track-%(tracking_id)s : %(levelname)-8s : %(message)s'.format(HOSTNAME), datefmt="%Y-%m-%d %H:%M:%S")
    ctx_filter = ContextFilter()

    root_logger = logging.getLogger("")
    root_logger.setLevel(logging.NOTSET)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    root_logger.addHandler(stream_handler)

    if DOPPLER_HOST:
        from hpc.doppler import UDPHandler, get_flask_request_info_for_doppler
        from hpc.requeststore import get_trace

        doppler_udp_handler = UDPHandler(host=DOPPLER_HOST, port=50001,
                                         datacenter=HULU_DC, env=HULU_ENV,
                                         hostname=HOSTNAME, codebasename=DOPPLER_NAME,
                                         get_request_info=get_flask_request_info_for_doppler,
                                         get_trace=get_trace)
        doppler_udp_handler.setLevel(level=logging.ERROR)
        root_logger.addFilter(ctx_filter)
        root_logger.addHandler(doppler_udp_handler)
    

def setup_sso(app):
    if HULU_ENV == "test": return
    from hpc.sso.flask_client import HuluSSO

    app.config['SSO_LOGIN_GROUPS'] = ['Devs']
    app.config['SSO_HIJACK_PROTECTION'] = False
    app.config['SSO_VIA_IP_IS_CLIENTS_FAULT'] = True
    hulu_sso = HuluSSO(app)
    return hulu_sso

