# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nekton',
 'nekton.externals.dcmqi.doc.segContexts.resources',
 'nekton.externals.dcmqi.util',
 'nekton.externals.dcmqi.util.junit',
 'nekton.externals.dcmqi.util.measurementReportUtils',
 'nekton.utils']

package_data = \
{'': ['*'],
 'nekton': ['bins/*',
            'externals/dcmqi/*',
            'externals/dcmqi/.circleci/*',
            'externals/dcmqi/CMake/*',
            'externals/dcmqi/CMakeExternals/*',
            'externals/dcmqi/Design/*',
            'externals/dcmqi/apps/*',
            'externals/dcmqi/apps/paramaps/*',
            'externals/dcmqi/apps/paramaps/Testing/*',
            'externals/dcmqi/apps/seg/*',
            'externals/dcmqi/apps/seg/Testing/*',
            'externals/dcmqi/apps/sr/*',
            'externals/dcmqi/apps/sr/Testing/*',
            'externals/dcmqi/data/paramaps/*',
            'externals/dcmqi/data/segmentations/*',
            'externals/dcmqi/data/segmentations/23x38x3/image/*',
            'externals/dcmqi/data/segmentations/23x38x3/multiframe/*',
            'externals/dcmqi/data/segmentations/23x38x3/nrrd/*',
            'externals/dcmqi/data/segmentations/23x38x3/screenshots/*',
            'externals/dcmqi/data/segmentations/23x38x3/seg/*',
            'externals/dcmqi/data/segmentations/24x38x3/image/*',
            'externals/dcmqi/data/segmentations/24x38x3/multiframe/*',
            'externals/dcmqi/data/segmentations/24x38x3/nrrd/*',
            'externals/dcmqi/data/segmentations/24x38x3/screenshots/*',
            'externals/dcmqi/data/segmentations/24x38x3/seg/*',
            'externals/dcmqi/data/segmentations/ct-3slice/*',
            'externals/dcmqi/data/sr-example/*',
            'externals/dcmqi/doc/*',
            'externals/dcmqi/doc/definitions/*',
            'externals/dcmqi/doc/examples/*',
            'externals/dcmqi/doc/pmContexts/*',
            'externals/dcmqi/doc/schemas/*',
            'externals/dcmqi/doc/segContexts/*',
            'externals/dcmqi/docker/*',
            'externals/dcmqi/docker/dcmqi/*',
            'externals/dcmqi/docker/dcmqi/imagefiles/*',
            'externals/dcmqi/include/dcmqi/*',
            'externals/dcmqi/jsoncpp/*',
            'externals/dcmqi/jsoncpp/json/*',
            'externals/dcmqi/libsrc/*']}

install_requires = \
['SimpleITK==2.1.1',
 'nibabel>=3.2.2,<4.0.0',
 'numpy==1.19.5',
 'pydicom-seg==0.3.0',
 'pydicom>=2.3.0,<3.0.0']

setup_kwargs = {
    'name': 'nekton',
    'version': '0.2.3',
    'description': 'A python package for DICOM to NifTi and NifTi to DICOM-SEG and GSPS conversion',
    'long_description': '# Nekton\n[![Python Application Testing](https://github.com/deepc-health/nekton/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/deepc-health/nekton/actions/workflows/tests.yml)[![Test and Release](https://github.com/deepc-health/nekton/actions/workflows/release.yml/badge.svg?branch=master)](https://github.com/deepc-health/nekton/actions/workflows/release.yml)\n[![Python Versions](https://img.shields.io/pypi/pyversions/nekton.svg)](https://pypi.org/project/nekton/)[![Package version](https://img.shields.io/pypi/v/nekton?color=%2334D058&label=pypi%20package)](https://pypi.org/project/nekton/)\n\n> A python package for DICOM to NifTi and NifTi to DICOM-SEG and GSPS conversion\n\n## SETUP\n\nThe python package is available for use on PyPI. It can be setup simply via pip\n\n```bash\npip install nekton\n```\n\nTo the check the setup, simply check the version number of the `nekton` package by\n\n```bash\npython -c \'import nekton; print(nekton.__version__)\'\n```\n\n## DICOM to NifTi\n\nThe DICOM to NifTi conversion in the package is based on a wrapper around the [dcm2niix](https://github.com/rordenlab/dcm2niix) software.\n\n### Usage\n\n```python\nfrom nekton.dcm2nii import Dcm2Nii\nconverter = Dcm2Nii()\nconverted_files = converter.run(dicom_directory=\'/test_files/CT5N\', name=\'Test\')\n# Converted 5 DCM to Nifti; Output stored @ /test_files/CT5N\nprint(converted_files)\n# [\'/test_files/CT5N/Test_SmartScore_-_Gated_0.5_sec_20010101000000_5.nii.gz\']\n```\n\nParameters `converter.run`:\n\n- `dicom_directory (Path)`: path to directory with Dicoms\n- `name (str, optional)`: Name to be given to the output file. Defaults to "".\n\nReturns:\n\n- `List[Path]`: output list of Nifti files\n\n\n### Notes\n\n- The renaming functionality retains the [suffixes](https://github.com/rordenlab/dcm2niix/blob/master/FILENAMING.md) from the original program.\n- The BIDS sidecar json is retained as well.\n\n## NifTi to DICOM-SEG\n\nThe NifTi to DICOM-SEG within nekton converts incoming segmentation NifTi to DICOM-SEG. The matching of the segmentation index to a text label is \ndone via json file using the schema suggested by `dcmqi`. The json can be generated using the [gui](http://qiicr.org/dcmqi/#/seg) also an example can be seen [here](https://github.com/deepc-health/nekton/blob/master/tests/test_data/sample_segmentation/mapping.json). \n\nCurrently, `nekton` supports creation of multiclass DICOM-SEG of two types-\n\n- single layer DICOM-SEG, where each non-empty slice has an individual file\n- multi layer DICOM-SEG, where all the n slices are rolled into a single file\n\n### Usage\n\n1. NifTi to single layer DICOM-SEG\n\n```python\nfrom nekton.nii2dcm import Nii2DcmSeg\nimport glob\nconverter = Nii2DcmSeg()\npath_dcms = [path for path in glob.glob(dir_dcms)]\npath_mapping = "mapping.json"\npath_seg_nifti = "CT5N_segmentation.nii.gz"\ndcmsegs = converter_dcmseg.multiclass_converter(\n        segfile = path_seg_nifti, segMapping= path_mapping, dcmfiles =path_dcms, multiLayer=False\n    )\nprint (len(dcmsegs))\n# 3\n```\n\n2. NifTi to multi layer DICOM-SEG\n\n```python\nfrom nekton.nii2dcm import Nii2DcmSeg\nimport glob\nconverter = Nii2DcmSeg()\npath_dcms = [path for path in glob.glob(dir_dcms)]\npath_mapping = "mapping.json"\npath_seg_nifti = "CT5N_segmentation.nii.gz"\ndcmsegs = converter.multiclass_converter(\n        segfile = path_seg_nifti, segMapping= path_mapping, dcmfiles =path_dcms, multiLayer=True\n    )\nprint (len(dcmsegs))\n# 1\n```\n\nParameters `converter.multiclass_converter`:\n\n- `segfile (Path)`: path to the nifti segmentation file\n- `segMapping (Path)`: path to the dcmqii format segmentation mapping json\n- `dcmfiles (List[Path])`: list of paths of all the source dicom files\n- `multiLayer (bool, optional)`: create a single multilayer dicomseg. Defaults to False.\n\nReturns:\n\n- `List[Path]`: list of paths of all generated dicomseg files\n\n### Notes\n\n- Multilabel NifTi(in the form of a NifTi file for a single label) to DICOM-SEG is under development.\n\n## NifTi to GSPS\n\n```\nThis feature will be available in a future release of the nekton\n```\n',
    'author': 'a-parida12',
    'author_email': 'abhijeet@deepc.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/deepc-health/nekton',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
