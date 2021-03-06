import argparse
import os, sys
import pydicom as dicom
import numpy as np
from PIL import Image

def getDICOMFiles(dicom_dir:str):
    files = os.listdir(dicom_dir)
    dicom_files = list(filter(lambda file: file.endswith(".dcm"), files))
    return dicom_files

def prepareParser(parser:argparse.ArgumentParser):
    parser.add_argument(
        '--dicom_dir',
        type=str,
        default='.',
        help='Path to DICOM folder'
    )

def saveDICOMFilesToImage(dicom_dir:str):
    for dicom_file in getDICOMFiles(dicom_dir):
        ds = dicom.dcmread(os.path.join(dicom_dir, dicom_file))
        np_data = ds.pixel_array 
        if len(np_data.shape) < 3:
            np_data = np_data.astype(np.uint32)
            Image.fromarray(np_data, 'I').save(os.path.join(dicom_dir, dicom_file.replace('.dcm', '.png')))
        else:
            Image.fromarray(np_data).save(os.path.join(dicom_dir, dicom_file.replace('.dcm', '.png')))
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    prepareParser(parser)
    FLAGS, _ = parser.parse_known_args()
    
    dicom_dir = os.path.abspath(FLAGS.dicom_dir)
    if not os.path.exists(dicom_dir) or not os.listdir(dicom_dir):
        print("DICOM directory does not exist. Use --dicom_dir to indicate a specific directory where DICOM are contain")
        sys.exit(-1)

    saveDICOMFilesToImage(dicom_dir)
