from multiprocessing import Pool

from ports import *

if __name__=="__main__":
    ports=get_camera_ports()
    inputs=[(port,f"camera_{n}",3) for n,port in enumerate(ports)]
    with Pool(1) as pool:
        # Use starmap to pass multiple arguments
        results = pool.starmap(take_multiple_photos_from_camera, inputs)

    print("Results:", results)