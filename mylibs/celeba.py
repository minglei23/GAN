# This built-in library is used for handling file and directory 
# paths and interacting with the operating system.
import os
import gdown
import zipfile
# For generating random numbers
# Used to randomly split the dataset
import random

def download_google_drive_file(file_id, output_filename):
    url = f'https://drive.google.com/uc?id={file_id}'
    gdown.download(url, output_filename, quiet=False)

def unzip_file(zip_filename, output_directory):
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall(output_directory)

def split_dataset(root_dir, train_dir, test_dir):
    files = os.listdir(root_dir)

    # create the train and test directory if not exist
    if not os.path.exists(train_dir):
        os.mkdir(train_dir)
    if not os.path.exists(test_dir):
        os.mkdir(test_dir)

    # Calculate the number of elements for the train and test lists
    train_len = int(0.9 * len(files))

    # Shuffle the elements
    random.shuffle(files)

    # Split the elements into the train and test lists
    train_lst = files[:train_len]
    test_lst = files[train_len:]

    for file in train_lst:
        src_path = os.path.join(root_dir + file)
        dest_path = os.path.join(train_dir + file)
        os.rename(src_path, dest_path)

    for file in test_lst:
        src_path = os.path.join(root_dir + file)
        dest_path = os.path.join(test_dir + file)
        os.rename(src_path, dest_path)

def download_celeba_dataset(root):
    file_id = '1E23HCNL-v9c54Wnzkm9yippBW8IaLUXp'
    zip_filename = f'{root}.zip'
    output_directory = '.'

    # download the dataset from google drive folder and unzip it
    download_google_drive_file(file_id, zip_filename)
    unzip_file(zip_filename, output_directory)
    os.rename('data512x512', f'{root}')

    # your dataset structure should look like after downloading:
    # dataset/
    # │
    # ├── image1.png
    # ├── image2.png
    # ├── image3.png
    # ├── ....

    train_dir = f'./{root}/train/'
    test_dir = f'./{root}/test/'

    # run this function to split your dataset to training dataset and evaluate dataset
    if not os.path.exists(train_dir) or not os.path.exists(test_dir):
      split_dataset(root + '/', train_dir, test_dir)
    else:
      print(train_dir + " or " + test_dir + " already exist")
    # then you should have data structure:
    # dataset/
    # │
    # ├── train/
    # │   ├── image1.png
    # │   ├── image2.png
    # │   └── ...
    # │   
    # ├── test/
    # │   ├── image27000.png
    # │   ├── image27001.png
    # │   └── ...

