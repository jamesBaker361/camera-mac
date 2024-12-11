import ctypes
import os

# Path to EDSDK.framework (update to your actual path)
EDSDK_PATH = "/Users/jbaker15/Downloads/edsdk/EDSDK/Framework/EDSDK.framework/Versions/A/EDSDK"

# Load the library
edsdk = ctypes.CDLL(EDSDK_PATH)

# Define function prototypes (example)
#edsdk.EDS_Init.argtypes = []
#dsdk.EDS_Init.restype = ctypes.c_int

print(dir(edsdk))

def initialize_sdk():
    result = edsdk.EDS_Init()
    if result != 0:
        raise Exception(f"Failed to initialize EDSDK. Error code: {result}")
    print("EDSDK initialized successfully.")

initialize_sdk()