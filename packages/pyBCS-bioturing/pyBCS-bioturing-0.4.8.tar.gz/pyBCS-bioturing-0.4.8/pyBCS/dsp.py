import os
import pandas as pd
import numpy as np
import tifffile
import xmltodict
import shutil
import json
import cv2

class OME:
    '''A class that handle data from OME-TIFF'''
    def __init__(self, excel_path, ome_dir):
        '''
        Create a OME object given an excel and a list of OME-TIF

        Parameters
        ----------
        excel_path: string
            location of the excel file. This file must have "SegmentProperties" and "TargetCountMatrix"
        ome_dir: string
            location of the folder with OME-TIFF files
        '''
        excel = pd.read_excel(excel_path, ['SegmentProperties', 'TargetCountMatrix'], converters={"ROILabel": str})

        # count
        self.count = excel['TargetCountMatrix'].iloc[:, 1:excel['TargetCountMatrix'].shape[1]]
        self.count.index = excel['TargetCountMatrix'].iloc[:, 0]

        # metadata
        roi, tif = self.extract_ome_tiff(ome_dir)
        self.metadata = pd.merge(excel['SegmentProperties'], roi, on=["SlideName", "ROILabel", "SegmentLabel"])
        self.metadata['ROILabel'] = self.metadata['ROILabel'].astype('category')
        # tif
        self.tif = tif
        
    def write(self, output_dir):
        '''Write OME to a folder that is accepted by BBrowser'''
        # spatial
        for tif in self.tif:
            print('Writing %s ...' % tif['name'])
            
            # init folder
            batch_path = os.path.join(output_dir, tif['name'])
            spatial_dir = os.path.join(batch_path, "spatial")
            if os.path.isdir(batch_path):
                shutil.rmtree(batch_path)
            os.makedirs(spatial_dir)

            # write metadata and count
            metadata = self.metadata[self.metadata['SlideName'] == tif['name']]
            count = self.count[metadata['SegmentDisplayName']]
            metadata.to_csv(os.path.join(batch_path, "metadata.csv.gz"), float_format='%.3f', compression='gzip')
            count.to_csv(os.path.join(batch_path, 'counts.csv.gz'), float_format='%.3f', compression='gzip')

            # write tiff file
            tifffile.imwrite(os.path.join(spatial_dir, '%s.tif' % tif['name']), tif['content'],
                    bigtiff=True, photometric="minisblack", compression=("zlib", 9))

            # spatial info
            json_file = open(os.path.join(spatial_dir, 'info.json'), 'w+')
            json.dump({
                "diameter": list(metadata["Diameter"]),
                "diameter_micron": list(metadata["DiameterMicron"]),
                "width": tif['content'].shape[2], # channel first (channels/rows/cols)
                "height": tif['content'].shape[1], # channel first
                "version": 1
            }, json_file)
            json_file.close()
        
        print('Done')

    def extract_ome_tiff(self, ome_dir):
        '''Extract OME to ROI metadata and normal TIFF'''
        roi_info = []
        tifs = []
        for tiff_name in os.listdir(ome_dir):
            if not tiff_name.endswith('.ome.tif') and not tiff_name.endswith('.ome.tiff'):
                continue

            tiff_path = os.path.join(ome_dir, tiff_name)
            tif = tifffile.TiffFile(tiff_path)
            omexml_string = tif.ome_metadata
            dom = xmltodict.parse(omexml_string)
            
            image_info = dom['OME']['Image']
            sample = image_info['@Name']
            pixels = image_info["Pixels"]
            physical_size_x = float(pixels["@PhysicalSizeX"])
            # size_x = float(pixels["@SizeX"])
            # size_y = float(pixels["@SizeY"])
            # ratio = physical_size_x / size_x
            
            rois = dom['OME']['ROI']
            
            # get ROIs
            print('Loading ROIs from %s ...' % tiff_name)
            for roi in rois:
                union = roi['Union']
                if not union:
                    continue

                label = union['Label']
                roi_label = label['@Text']
                mask = union["Mask"]
                if not label or not mask:
                    continue

                roi_label = label['@Text']

                def get_mask(mask):
                    '''Wraper to get mask info'''
                    width = float(mask["@Width"])
                    diameter = width / 2
                    diameter_micron = diameter * physical_size_x
                    return {
                        "SlideName": sample,
                        "ROILabel": roi_label,
                        "SegmentLabel": mask["@Text"],
                        "X": mask["@X"],
                        "Y": mask["@Y"],
                        "Width": mask["@Width"],
                        "Height": mask["@Height"],
                        "Diameter": diameter,
                        "DiameterMicron": diameter_micron,
                    }

                if type(union["Mask"]) == list:
                    [roi_info.append(get_mask(m)) for m in mask]
                else:
                    roi_info.append(get_mask(mask))

            # get tif
            print('Loading TIFF from %s ...' % tiff_name)
            image = tif.asarray()

            print("Convert channel first to channel last...")
            # convert channel first to channel last
            image = np.moveaxis(image, 0, -1).astype(np.uint16)

            if image.shape[2] == 2:
                more_channel = np.zeros((image.shape[1], image.shape[0]), dtype=np.uint16)
                image = cv2.merge((image[:,:,0], image[:,:,1], more_channel))
            
            print("Quantile...")
            # quantile
            x = np.quantile(image, 0.99)
            # y = np.quantile(image, 0.05)
            
            print("Filter...")
            image[image > x] = x
            # image[image < y] = y

            print("Normalize...")
            # normalize
            image = cv2.normalize(image, None, 0, 2 ** 16 - 1, cv2.NORM_MINMAX)
            image = image.astype(np.uint16)
            
            print("Convert channel last to channel first...")
            # conver channel last to channel first for saving tiff file
            image = np.moveaxis(image, -1, 0)
            
            # append image
            tifs.append({"name": sample, 'content': image})
            tif.close()
        
        return pd.DataFrame(roi_info), tifs
