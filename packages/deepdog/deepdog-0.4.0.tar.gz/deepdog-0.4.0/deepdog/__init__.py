import logging
from deepdog.meta import __version__
from deepdog.bayes_run import BayesRun
from deepdog.alt_bayes_run import AltBayesRun
from deepdog.diagnostic import Diagnostic


def get_version():
	return __version__


__all__ = ["get_version", "BayesRun", "AltBayesRun", "Diagnostic"]


logging.getLogger(__name__).addHandler(logging.NullHandler())
