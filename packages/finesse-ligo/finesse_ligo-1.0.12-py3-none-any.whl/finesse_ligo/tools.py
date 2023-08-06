import finesse
import numpy as np
import importlib.resources
from finesse.analysis.actions import OptimiseRFReadoutPhaseDC
from .actions import DARM_RF_to_DC


# URLS where data files are stored
DATAFILES = {
    "LIGO_axialsymmetric_test_mass_reciprocity.npz": "https://zenodo.org/record/6385930/files/LIGO_axialsymmetric_test_mass_reciprocity.npz",
}

CHECKSUM = {
    "LIGO_axialsymmetric_test_mass_reciprocity.npz": "a9ee7fd79609b58cde587e345ee78fd6"
}


def download(datafile):
    if datafile not in DATAFILES:
        raise FileNotFoundError(f"Datafile {datafile} is not an option")
    if datafile not in CHECKSUM:
        raise RuntimeError(f"Datafile {datafile} does not have a checksum specified")

    from tqdm.auto import tqdm
    import requests
    from pathlib import Path
    import shutil
    import hashlib

    # Get data installation path from finesse config
    cfg = finesse.config.config_instance()
    path = Path(cfg["finesse.data"]["path"]).expanduser().absolute() / "finesse-ligo"
    path.mkdir(parents=True, exist_ok=True)
    print(f"Writing data to {path}")
    # make an HTTP request within a context manager
    with requests.get(DATAFILES[datafile], stream=True) as r:
        # check header to get content length, in bytes
        total_length = int(r.headers.get("Content-Length"))
        # implement progress bar via tqdm
        with tqdm.wrapattr(
            r.raw, "read", total=total_length, desc=f"Downloading {DATAFILES[datafile]}"
        ) as raw:
            # save the output to a file
            with open(path / datafile, "wb") as output:
                shutil.copyfileobj(raw, output)

    with open(path / datafile, "rb") as output:
        checksum = hashlib.md5(output.read()).hexdigest()
        if checksum != CHECKSUM[datafile]:
            raise RuntimeError(
                f"Checksum failed, downloaded file probably corrupted: {checksum} != {CHECKSUM[datafile]}"
            )


nl = "- \n"
download.__doc__ = f"""Downloads a datafile from an external source.
This will download the data into the path specified in your usr.ini.
Your usr.ini file can be found py running:

>>> finesse.config.config_instance().user_config_path()

The current data directory being used can be found with:

>>> finesse.config.config_instance()['finesse.data']['path']

Possible datafiles that can be downloaded are:
{nl + nl.join(str(k) for k in DATAFILES.keys())}

Parameters
----------
datafile : str
    Name of datafile to download
"""


# URLS where data files are stored
DATAFILES = {
    "LIGO_axialsymmetric_test_mass_reciprocity.npz": "https://zenodo.org/record/6385930/files/LIGO_axialsymmetric_test_mass_reciprocity.npz",
}

CHECKSUM = {
    "LIGO_axialsymmetric_test_mass_reciprocity.npz": "a9ee7fd79609b58cde587e345ee78fd6"
}


def download(datafile):
    if datafile not in DATAFILES:
        raise FileNotFoundError(f"Datafile {datafile} is not an option")
    if datafile not in CHECKSUM:
        raise RuntimeError(f"Datafile {datafile} does not have a checksum specified")

    from tqdm.auto import tqdm
    import requests
    from pathlib import Path
    import shutil
    import hashlib

    # Get data installation path from finesse config
    cfg = finesse.config.config_instance()
    path = Path(cfg["finesse.data"]["path"]).expanduser().absolute() / "finesse-ligo"
    path.mkdir(parents=True, exist_ok=True)
    print(f"Writing data to {path}")
    # make an HTTP request within a context manager
    with requests.get(DATAFILES[datafile], stream=True) as r:
        # check header to get content length, in bytes
        total_length = int(r.headers.get("Content-Length"))
        # implement progress bar via tqdm
        with tqdm.wrapattr(
            r.raw, "read", total=total_length, desc=f"Downloading {DATAFILES[datafile]}"
        ) as raw:
            # save the output to a file
            with open(path / datafile, "wb") as output:
                shutil.copyfileobj(raw, output)

    with open(path / datafile, "rb") as output:
        checksum = hashlib.md5(output.read()).hexdigest()
        if checksum != CHECKSUM[datafile]:
            raise RuntimeError(
                f"Checksum failed, downloaded file probably corrupted: {checksum} != {CHECKSUM[datafile]}"
            )


nl = "- \n"
download.__doc__ = f"""Downloads a datafile from an external source.
This will download the data into the path specified in your usr.ini.
Your usr.ini file can be found py running:

>>> finesse.config.config_instance().user_config_path()

The current data directory being used can be found with:

>>> finesse.config.config_instance()['finesse.data']['path']

Possible datafiles that can be downloaded are:
{nl + nl.join(str(k) for k in DATAFILES.keys())}

Parameters
----------
datafile : str
    Name of datafile to download
"""


def make_arm():
    """Simple LIGO arm cavity model."""
    base = finesse.Model()
    base.parse(importlib.resources.read_text("finesse_ligo.katscript", "arm.kat"))
    return base


def make_aligo(RF_AS_readout=False, verbose=False):
    base = finesse.Model()
    base.parse(importlib.resources.read_text("finesse_ligo.katscript", "aligo.kat"))
    base.run(
        OptimiseRFReadoutPhaseDC(
            "CARM",
            "REFL9",
            "PRCL",
            "POP9",
            "SRCL",
            "POP45",
            "DARM",
            "AS45",
        )
    )

    set_lock_gains(base, verbose=verbose)

    if not RF_AS_readout:
        base.run(DARM_RF_to_DC())

    return base


def set_lock_gains(model, d_dof=1e-6, gain_scale=1, verbose=False):
    """For the current state of the model each lock will have its gain computed. This is
    done by computing the gradient of the error signal with respect to the set feedback.

    The optical gain is then computed as -1/(slope).

    This function alters the state of the provided model.

    Parameters
    ----------
    model : Model
        Model to set the lock gains of
    d_dof : double
        step size for computing the slope of the error signals
    verbose : boolean
        Prints information when true
    """
    from finesse.analysis.actions import Xaxis, Series
    from finesse.components.readout import ReadoutDetectorOutput

    for lock in model.locks:
        # Make sure readouts being used have their outputs enabled
        if type(lock.error_signal) is ReadoutDetectorOutput:
            lock.error_signal.readout.output_detectors = True

    # Use a flattened series analysis as it only creates one model
    # and xaxis resets all the parameters each time
    analysis = Series(
        *(
            Xaxis(lock.feedback, "lin", -d_dof, d_dof, 1, relative=True, name=lock.name)
            for lock in model.locks
        ),
        flatten=True,
    )
    sol = model.run(analysis)

    for lock in model.locks:
        lock_sol = sol[lock.name]
        x = lock_sol.x1
        error = lock_sol[lock.error_signal.name] + lock.offset
        grad = np.gradient(error, x[1] - x[0]).mean()
        if grad == 0:
            lock.gain = np.NaN
        else:
            lock.gain = -1 / grad * gain_scale

        if verbose:
            print(lock, lock.error_signal.name, lock.gain)


def get_lock_error_signals(model, dof_range, steps=1000, verbose=False):
    from finesse.analysis.actions import Xaxis, Series
    from finesse.components.readout import ReadoutDetectorOutput

    for lock in model.locks:
        # Make sure readouts being used have their outputs enabled
        if type(lock.error_signal) is ReadoutDetectorOutput:
            lock.error_signal.readout.output_detectors = True

    # Use a flattened series analysis as it only creates one model
    # and xaxis resets all the parameters each time
    analysis = Series(
        *(
            Xaxis(
                lock.feedback,
                "lin",
                -dof_range,
                dof_range,
                steps,
                relative=True,
                name=lock.feedback.owner.name,
            )
            for lock in model.locks
        ),
        flatten=True,
    )
    sol = model.run(analysis)
    return sol
