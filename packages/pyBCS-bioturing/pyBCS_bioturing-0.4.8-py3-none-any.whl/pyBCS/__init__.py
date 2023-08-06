from .light_transpose import bcs_transpose
from .scanpy2bcs import format_data
from .dsp import OME

def test():
    ome_dir = '/mnt2/ginny/jnj_spatial'
    excel_path = '/mnt2/ginny/jnj_spatial/NGS RNA Tonsil Pilot_BioQC_no exclusion.xlsx'
    ome = OME(excel_path, ome_dir)
    # ome.write('jnj_ome')
    return ome