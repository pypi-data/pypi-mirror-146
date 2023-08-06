import nibabel as nib
import os.path as op
from time import time
import logging

from AFQ.definitions.mapping import SlrMap
from AFQ.api.utils import wf_sections, add_method_descriptions
from AFQ.viz.utils import viz_import_msg_error

from AFQ.tasks.data import get_data_plan
from AFQ.tasks.mapping import get_mapping_plan
from AFQ.tasks.tractography import get_tractography_plan
from AFQ.tasks.segmentation import get_segmentation_plan
from AFQ.tasks.viz import get_viz_plan


__all__ = ["ParticipantAFQ"]


@add_method_descriptions
class ParticipantAFQ(object):
    def __init__(self,
                 dwi_data_file,
                 bval_file, bvec_file,
                 output_dir,
                 bids_info=None,
                 **kwargs):
        """
        Initialize a ParticipantAFQ object from a BIDS dataset.

        Parameters
        ----------
        dwi_data_file : str
            Path to DWI data file.
        bval_file : str
            Path to bval file.
        bvec_file : str
            Path to bvec file.
        output_dir : str
            Path to output directory.
        bids_info : dict or None, optional
            This is used by GroupAFQ to provide information about
            the BIDS layout to each participant.
        kwargs : additional optional parameters
            You can set additional parameters for any step
            of the process. See :ref:`usage/kwargs` for more details.

        Examples
        --------
        api.ParticipantAFQ(
            dwi_data_file, bval_file, bvec_file, output_dir,
            csd_sh_order=4)
        api.ParticipantAFQ(
            dwi_data_file, bval_file, bvec_file, output_dir,
            reg_template_spec="mni_t2", reg_subject_spec="b0")

        Notes
        -----
        In tracking_params, parameters with the suffix mask which are also
        a mask from AFQ.definitions.mask will be handled automatically by
        the api.

        It is recommended that you leave the bids_info parameter as None,
        and instead pass in the paths to the files you want to use directly.
        """
        if not isinstance(output_dir, str):
            raise TypeError(
                "output_dir must be a str")
        if not isinstance(dwi_data_file, str):
            raise TypeError(
                "dwi_data_file must be a str")
        if not isinstance(bval_file, str):
            raise TypeError(
                "bval_file must be a str")
        if not isinstance(bvec_file, str):
            raise TypeError(
                "bvec_file must be a str")
        if not op.exists(output_dir):
            raise ValueError(
                f"output_dir does not exist: {output_dir}")

        self.logger = logging.getLogger('AFQ.api')

        kwargs["bids_info"] = bids_info
        kwargs["subses_dict"] = {
            "dwi_file": dwi_data_file,
            "results_dir": output_dir}

        # construct pimms plans
        if "mapping_definition" in kwargs and isinstance(
                kwargs["mapping_definition"], SlrMap):
            plans = {  # if using SLR map, do tractography first
                "data": get_data_plan(kwargs),
                "tractography": get_tractography_plan(kwargs),
                "mapping": get_mapping_plan(kwargs, use_sls=True),
                "segmentation": get_segmentation_plan(kwargs),
                "viz": get_viz_plan(kwargs)}
        else:
            plans = {  # Otherwise, do mapping first
                "data": get_data_plan(kwargs),
                "mapping": get_mapping_plan(kwargs),
                "tractography": get_tractography_plan(kwargs),
                "segmentation": get_segmentation_plan(kwargs),
                "viz": get_viz_plan(kwargs)}

        img = nib.load(dwi_data_file)

        input_data = dict(
            dwi_img=img,
            dwi_affine=img.affine,
            bval_file=bval_file,
            bvec_file=bvec_file,
            **kwargs)

        # chain together a complete plan from individual plans
        previous_data = {}
        for name, plan in plans.items():
            previous_data[f"{name}_imap"] = plan(
                **input_data,
                **previous_data)
            last_name = name

        self.wf_dict =\
            previous_data[f"{last_name}_imap"]

    def __getattribute__(self, attr):
        # check if normal attr exists first
        try:
            return object.__getattribute__(self, attr)
        except AttributeError:
            pass

        # find what name to use
        attr_file = attr + "_file"
        if attr in self.wf_dict:
            return self.wf_dict[attr]
        elif attr_file in self.wf_dict:
            return self.wf_dict[attr_file]
        else:
            for sub_attr in wf_sections:
                if attr in self.wf_dict[sub_attr]:
                    return self.wf_dict[sub_attr][attr]
                elif attr_file in self.wf_dict[sub_attr]:
                    return self.wf_dict[sub_attr][attr_file]

        # attr not found, allow typical AttributeError
        return object.__getattribute__(self, attr)

    def export_all(self, viz=True, xforms=True,
                   indiv=True):
        """ Exports all the possible outputs

        Parameters
        ----------
        viz : bool
            Whether to output visualizations. This includes tract profile
            plots, a figure containing all bundles, and, if using the AFQ
            segmentation algorithm, individual bundle figures.
            Default: True
        xforms : bool
            Whether to output the reg_template image in subject space and,
            depending on if it is possible based on the mapping used, to
            output the b0 in template space.
            Default: True
        indiv : bool
            Whether to output individual bundles in their own files, in
            addition to the one file containing all bundles. If using
            the AFQ segmentation algorithm, individual ROIs are also
            output.
            Default: True
        """
        start_time = time()
        seg_algo = self.segmentation_params.get("seg_algo", "AFQ")

        if xforms:
            try:
                self.b0_warped
            except Exception as e:
                self.logger.warning((
                    "Failed to export warped b0. This could be because your "
                    "mapping type is only compatible with transformation "
                    f"from template to subject space. The error is: {e}"))
            self.template_xform
        if indiv:
            self.indiv_bundles
            if seg_algo == "AFQ":
                self.rois
        self.sl_counts
        self.profiles

        if viz:
            try:
                self.tract_profile_plots
            except ImportError as e:
                plotly_err_message = viz_import_msg_error("plot")
                if str(e) != plotly_err_message:
                    raise
                else:
                    self.logger.warning(plotly_err_message)
            self.all_bundles_figure
            if seg_algo == "AFQ":
                self.indiv_bundles_figures
        self.logger.info(
            "Time taken for export all: " + str(time() - start_time))
