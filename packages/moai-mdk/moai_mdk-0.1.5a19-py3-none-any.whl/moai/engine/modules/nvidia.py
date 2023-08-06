import os
import torch
import logging

__all__ = ['NvidiaSMI', 'DebugCUDA']

log = logging.getLogger(__name__)
class NvidiaSMI(object):
    def __init__(self):
        if 'PROGRAMFILES' in os.environ.keys():
            nvidia_smi_path = os.path.join(
                os.environ['PROGRAMFILES'],
                'NVIDIA Corporation',
                'NVSMI'
            )
            if nvidia_smi_path not in os.environ['PATH']:
                os.environ['PATH'] = os.environ['PATH'] + ";" + nvidia_smi_path

class DebugCUDA(object):
    def __init__(self):
        os.environ['CUDA_LAUNCH_BLOCKING'] = str(1)

class DisableCuDNN(object):
    def __init__(self):
        log.info("Disabling CuDNN.")
        torch.backends.cudnn.enabled = False