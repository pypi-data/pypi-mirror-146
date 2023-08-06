from AFQ.definitions.utils import Definition
from AFQ.definitions.mask import MaskFile

from AFQ.data.s3bids import write_json
from AFQ.tasks.utils import get_fname

import nibabel as nib
import os.path as op

from dipy.align import resample

# For scalar defintions, each class should have a name parameter

__all__ = ["ScalarFile", "TemplateScalar"]


class ScalarMixin():
    def get_for_subses(self):
        def get_for_subses_getter(
                subses_dict, bids_info, dwi_affine, data_imap, mapping):
            reg_template = data_imap["reg_template"]
            scalar_file = get_fname(
                subses_dict,
                f'_model-{self.name}.nii.gz')
            if not op.exists(scalar_file):
                scalar_data, meta = self.get_data(
                    subses_dict, bids_info, dwi_affine, reg_template, mapping)

                nib.save(
                    nib.Nifti1Image(scalar_data, dwi_affine),
                    scalar_file)
                meta_fname = get_fname(
                    subses_dict,
                    f'_model-{self.name}.json')
                write_json(meta_fname, meta)
            return scalar_file
        return get_for_subses_getter


class ScalarFile(MaskFile):
    """
    Define a scalar based on a file for each subject.
    Assumes the scalar is already in subject space.

    Parameters
    ----------
    name : str
        name of the scalar.
    path : str, optional
        path to file to get scalar from. Use this or suffix.
        Default: None
    suffix : str, optional
        suffix to pass to bids_layout.get() to identify the file.
        Default: None
    filters : str, optional
        Additional filters to pass to bids_layout.get() to identify
        the file.
        Default: {}

    Examples
    --------
    my_scalar = ScalarFile(
        "my_scalar",
        suffix="scalarSuffix",
        filters={"scope": "dmriprep"})
    api.GroupAFQ(scalars=["dti_fa", "dti_md", my_scalar])
    """

    def __init__(self, name, path=None, suffix=None, filters={}):
        MaskFile.__init__(self, path, suffix, filters)
        self.name = name

    def get_data(self, subses_dict, bids_info, dwi_affine,
                 reg_template, mapping):
        if self.from_path:
            return self.fname
        else:
            return self.fnames[bids_info['session']][bids_info['subject']]


class TemplateScalar(ScalarMixin, Definition):
    """
    Define a scalar based on a template.
    This template will be transformed into subject space before use.

    Parameters
    ----------
    name : str
        name of the scalar.
    path : str
        path to the template.

    Examples
    --------
    my_scalar = TemplateScalar(
        "my_scalar", "path/to/my_scalar_in_MNI.nii.gz")
    api.GroupAFQ(scalars=["dti_fa", "dti_md", my_scalar])
    """

    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.img = nib.load(self.path)
        self.is_resampled = False

    def find_path(self, bids_layout, from_path, subject, session):
        pass

    def get_data(self, subses_dict, bids_info, dwi_affine,
                 reg_template, mapping):
        if mapping is None:
            raise ValueError((
                "You cannot use a TemplateScalar to generate "
                "the subject image for mapping."))
        if not self.is_resampled:
            self.img = resample(
                self.img.get_fdata(),
                reg_template,
                self.img.affine,
                reg_template.affine).get_fdata()
            self.is_resampled = True

        scalar_data = mapping.transform_inverse(self.img)

        return scalar_data, dict(source=self.path)
