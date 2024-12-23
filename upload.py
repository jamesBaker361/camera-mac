from datasets import Dataset
import os
import PIL
import PIL.Image
import sys

map={
    "subject_name":[],
    "camera_0":[],
    "camera_1":[],
    "camera_2":[],
    "camera_3":[],
    "timestamp":[]
}
if __name__=='__main__':
    

    # Print all command-line arguments
    print("Command-line arguments:", sys.argv)
    base_dir="/Users/jbaker15/Desktop/camera/"
    if not os.path.exists(base_dir):
        base_dir="/scratch/jlb638/tmp/"

    directory=f"{base_dir}imgdir_1"
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    #print(files)

    subject_set=set()
    for f in files:
        name='_'.join(f.split("_")[:-1])
        subject_set.add(name)

    print("subjects",subject_set)

    def all_exist(files,verbose=False):
        for f in files:
            if not os.path.exists(f):
                if verbose:
                    print(f"{f} does not exist")
                return False
        return True

    for subject_name in subject_set:
        for n in range(0,9999):
            formatted = f"{n:04}"
            files=[f"{base_dir}imgdir_{k}/{subject_name}_{formatted}.jpg" for k in range(4)]

            if all_exist(files):
                map["subject_name"].append(subject_name)
                map["timestamp"].append(formatted)
                for k in range(4):
                    map[f"camera_{k}"].append(PIL.Image.open(f"{base_dir}imgdir_{k}/{subject_name}_{formatted}.jpg"))

    print("len ",len(map))
    Dataset.from_dict(map).push_to_hub("jlbaker361/raw-james")