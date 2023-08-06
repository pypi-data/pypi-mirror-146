from .enumerates import ReferenceFrame

class CovarianceParameters(dict):

    def __init__(self, epoch=None, ref_frame=None):
        super().__setitem__("EPOCH", epoch)
        super().__setitem__("COV_REF_FRAME", ref_frame)
        super().__setitem__("matrix", None)

    def get_epoch(self):
        """Return the epoch of this covariance"""
        return self["EPOCH"]

    def get_reference_frame(self):
        """Return the reference frame of the covariance"""
        return ReferenceFrame(self["COV_REF_FRAME"])

    def get_covariance_matrix(self):
        """Return the 6x6 covariance matrix"""
        return self["matrix"]

