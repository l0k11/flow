import waitress, logging
import threads.client_api as api

logger = logging.getLogger('waitress')
logger.setLevel(logging.CRITICAL)

waitress.serve(api.app, host = "0.0.0.0", port = 5000)

