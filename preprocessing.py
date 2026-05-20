from PIL import Image
from pathlib import Path
import random
import shutil
from torchvision import transforms

# path to dataset
dataset_path = Path("dataset")

# --------------------------------------------------------------------------------
# Checking for corrupted images
# --------------------------------------------------------------------------------
flag = 0
for folder in dataset_path.iterdir():   # iterdir loops through folders and files
    for image in folder.iterdir():
        try:
            img = Image.open(image)
            img.verify()    # check file
        except:
            print("Corrupted image:", image)
            flag = 1
if flag == 0:
    print("Status: All images read correctly!")


# --------------------------------------------------------------------------------
# Basic EDA
# --------------------------------------------------------------------------------
images = 0  # total images count
class_counts = {}  # per class counts
widths, heights = [], []

for folder in dataset_path.iterdir():
    count = 0
    for image in folder.iterdir():
        img = Image.open(image)
        w, h = img.size

        widths.append(w)    # add heights and widths to list
        heights.append(h)

        count += 1
        images += 1

    class_counts[folder.name] = count

# print stats
print("\nDataset Statistics\n------------------")
print("Total images:", images)
print("Total classes:", 6)

print("\nImages per class\n----------------")
for i in class_counts:
    print(f"Face {i}: {class_counts[i]}")

print("\nImage Size Statistics\n---------------------")
print(f"Min Height: {min(heights)}\nMax Height: {max(heights)}")
print(f"Min Width: {min(widths)}\nMax Width: {max(widths)}")


# --------------------------------------------------------------------------------
# Splitting dataset
# --------------------------------------------------------------------------------
# making split on 80/10/10 and then on 70/15/15
train, valid, test = 0.7, 0.15, 0.15
train_path = Path("split2_701515/train")
valid_path = Path("split2_701515/val")
test_path = Path("split2_701515/test")

for folder in dataset_path.iterdir():
    images = list(folder.iterdir()) # list of images
    random.shuffle(images)  # shuffle images
    n = len(images) #total images

    train_end = int(train * n)  # last img no i.e. 80
    valid_end = train_end + int(valid * n)  # 80 + 10 = 90

    train_imgs = images[:train_end]     # slicing image list
    valid_imgs = images[train_end:valid_end]
    test_imgs = images[valid_end:]

    (train_path/folder.name).mkdir(parents=True, exist_ok=True) #make new folders for classes as 1,2,3
    (valid_path/folder.name).mkdir(parents=True, exist_ok=True) #check parent directory and data if exists
    (test_path/folder.name).mkdir(parents=True, exist_ok=True)

    for img in train_imgs:
        shutil.copy(img, train_path / folder.name / img.name)   # copy images to the path
    for img in valid_imgs:
        shutil.copy(img, valid_path / folder.name / img.name)
    for img in test_imgs:
        shutil.copy(img, test_path / folder.name / img.name)



# --------------------------------------------------------------------------------
# Training Data - Resizing > Augmentation > Normalization
# --------------------------------------------------------------------------------
# first split1 and then split2 will be used
# making transforms which will be used later on images
train_transform = transforms.Compose([

    # Resize (dynamic resizing)
    # resizing shorter side of image to 256 px
    # cropping at center to better preserve aspect ratio
    transforms.Resize(256),
    transforms.CenterCrop(224),
    
    # Augmentation (dynamic augmentation)
    transforms.RandomHorizontalFlip(p=0.5), #50% chance of flipping image
    transforms.RandomRotation(20),  # rotates left/right randomly between -20 or +20 degrees
    transforms.ColorJitter(
        # random property changes as between +0.2 and -0.2
        brightness=0.2,
        contrast=0.2,
        saturation=0.2
    ),
    
    # Convert image to tensor for the model
    # scales pixel values to 0-1 (from 0-255)
    transforms.ToTensor(),
    
    # Normalization
    # applies formula: (pixel - mean) / standard deviation
    # now pixel values become between [-1, +1] (from 0-1)
    transforms.Normalize(
        mean=[0.5, 0.5, 0.5], # assuming 0.5 mean for each channel
        std=[0.5, 0.5, 0.5]   # standard dev for each channel
    )
])


# --------------------------------------------------------------------------------
# Valid and Test Data - Resizing > Normalization
# --------------------------------------------------------------------------------
valid_test_transform = transforms.Compose([
    
    #Resize and crop
    transforms.Resize(256),
    transforms.CenterCrop(224),
    
    # image to tensor values
    transforms.ToTensor(),
    
    # Normalization
    transforms.Normalize(
        mean=[0.5, 0.5, 0.5],
        std=[0.5, 0.5, 0.5]
    )
])