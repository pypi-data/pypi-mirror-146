from finesse.analysis.actions import Action, RunLocks


class DARM_RF_to_DC(Action):
    """Locks a model using DARM RF readout then transitions the model into using a DC
    readout and locks."""

    def __init__(self, name="DarmRF2DC"):
        super().__init__(name)
        self.__lock_rf = RunLocks("DARM_rf_lock")
        self.__lock_dc = RunLocks("DARM_dc_lock")

    def _do(self, state):
        self.__lock_rf._do(state)
        state.model.DARM_rf_lock.disabled = True
        # kick lock away from zero tuning for DC lock to grab with
        state.model.DARM.DC += 0.5e-3
        # take a guess at the gain
        state.model.DARM_dc_lock.gain = -0.01
        state.model.DARM_dc_lock.disabled = False
        self.__lock_dc._do(state)
        return None

    def _requests(self, model, memo, first=True):
        self.__lock_rf._requests(model, memo)
        self.__lock_dc._requests(model, memo)
        return memo


class DRFPMI_state(Action):
    """Assumes a mode has a PRM, SRM, ITMX, ETMX, ITMY, and ETMY mirror elements in.
    This action will change the alignment state of these. The options are:

    'PRMI', 'SRMI', 'MI', 'FPMI', 'PRFPMI', 'SRFPMI', 'DRFPMI', 'XARM', 'YARM'

    This action will change the state of the model.
    """

    def __init__(self, state: str, name="drfpmi_state"):
        super().__init__(name)
        states = (
            "PRMI",
            "SRMI",
            "MI",
            "FPMI",
            "PRFPMI",
            "SRFPMI",
            "DRFPMI",
            "XARM",
            "YARM",
        )
        if state not in states:
            raise ValueError(f"State '{state}' is not a valid option: {states}")
        self.state = state

    def _do(self, state):
        if self.state == "PRMI":
            state.model.PRM.misaligned = 0
            state.model.SRM.misaligned = 1
            state.model.ETMX.misaligned = 1
            state.model.ITMX.misaligned = 0
            state.model.ETMY.misaligned = 1
            state.model.ITMY.misaligned = 0
        elif self.state == "SRMI":
            state.model.PRM.misaligned = 1
            state.model.SRM.misaligned = 0
            state.model.ETMX.misaligned = 1
            state.model.ITMX.misaligned = 0
            state.model.ETMY.misaligned = 1
            state.model.ITMY.misaligned = 0
        elif self.state == "MI":
            state.model.PRM.misaligned = 1
            state.model.SRM.misaligned = 1
            state.model.ETMX.misaligned = 1
            state.model.ITMX.misaligned = 0
            state.model.ETMY.misaligned = 1
            state.model.ITMY.misaligned = 0
        elif self.state == "FPMI":
            state.model.PRM.misaligned = 1
            state.model.SRM.misaligned = 1
            state.model.ETMX.misaligned = 0
            state.model.ITMX.misaligned = 0
            state.model.ETMY.misaligned = 0
            state.model.ITMY.misaligned = 0
        elif self.state == "PRFPMI":
            state.model.PRM.misaligned = 0
            state.model.SRM.misaligned = 1
            state.model.ETMX.misaligned = 0
            state.model.ITMX.misaligned = 0
            state.model.ETMY.misaligned = 0
            state.model.ITMY.misaligned = 0
        elif self.state == "SRFPMI":
            state.model.PRM.misaligned = 1
            state.model.SRM.misaligned = 0
            state.model.ETMX.misaligned = 0
            state.model.ITMX.misaligned = 0
            state.model.ETMY.misaligned = 0
            state.model.ITMY.misaligned = 0
        elif self.state == "DRFPMI":
            state.model.PRM.misaligned = 0
            state.model.SRM.misaligned = 0
            state.model.ETMX.misaligned = 0
            state.model.ITMX.misaligned = 0
            state.model.ETMY.misaligned = 0
            state.model.ITMY.misaligned = 0
        elif self.state == "YARM":
            state.model.PRM.misaligned = 1
            state.model.SRM.misaligned = 1
            state.model.ETMX.misaligned = 1
            state.model.ITMX.misaligned = 1
            state.model.ETMY.misaligned = 0
            state.model.ITMY.misaligned = 0
        elif self.state == "XARM":
            state.model.PRM.misaligned = 1
            state.model.SRM.misaligned = 1
            state.model.ETMX.misaligned = 0
            state.model.ITMX.misaligned = 0
            state.model.ETMY.misaligned = 1
            state.model.ITMY.misaligned = 1
        else:
            raise Exception(f"{self.state} not implemented")

    def _requests(self, model, memo, first=True):
        # changing the mirror misaligned parameter is essentially
        # changing the mirror reflectivity model parameter
        memo["changing_parameters"].extend(
            (
                "PRM.misaligned",
                "SRM.misaligned",
                "ETMX.misaligned",
                "ITMX.misaligned",
                "ETMY.misaligned",
                "ITMY.misaligned",
            )
        )
        return memo
