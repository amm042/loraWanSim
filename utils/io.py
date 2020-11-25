import os
import os.path
from .exception import ApplicationException
import pandas

raise DeprecationWarning("This isn't used.")
def ensure_exists(path, file):
    os.makedirs(path, exist_ok=True)

    pfile = os.path.join(path, file)
    if not os.path.exists(pfile):
        raise ApplicationException("No configuration file at {}".format(pfile))
    return pfile
def load_config(path, file):
    "read the config"
    pfile = ensure_exists(path,file)
    try:
        return pandas.read_csv(pfile)
    except pandas.errors.EmptyDataError:
        return pandas.DataFrame()
