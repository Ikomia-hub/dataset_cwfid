<div align="center">
  <img src="https://raw.githubusercontent.com/Ikomia-hub/dataset_cwfid/main/icons/cwfid.png" alt="Algorithm icon">
  <h1 align="center">dataset_cwfid</h1>
</div>
<br />
<p align="center">
    <a href="https://github.com/Ikomia-hub/dataset_cwfid">
        <img alt="Stars" src="https://img.shields.io/github/stars/Ikomia-hub/dataset_cwfid">
    </a>
    <a href="https://app.ikomia.ai/hub/">
        <img alt="Website" src="https://img.shields.io/website/http/app.ikomia.ai/en.svg?down_color=red&down_message=offline&up_message=online">
    </a>
    <a href="https://github.com/Ikomia-hub/dataset_cwfid/blob/main/LICENSE.md">
        <img alt="GitHub" src="https://img.shields.io/github/license/Ikomia-hub/dataset_cwfid.svg?color=blue">
    </a>    
    <br>
    <a href="https://discord.com/invite/82Tnw9UGGc">
        <img alt="Discord community" src="https://img.shields.io/badge/Discord-white?style=social&logo=discord">
    </a> 
</p>

Load Crop/Weed Field Image Dataset (CWFID) for semantic segmentation. This algorithm converts the CWFID dataset into Ikomia dataset format. Then, any semantic segmentation training algorithms from the Ikomia HUB can be connected to this converter. 

In Ikomia Studio, once dataset is loaded, all images can be visualized with their respective annotations.

The CWFID dataset comprises field images, vegetation segmentation masks and crop/weed plant type annotations.

![Image example](https://raw.githubusercontent.com/Ikomia-hub/dataset_cwfid/feat/new_readme/icons/example.jpg)

## :rocket: Use with Ikomia API

#### 1. Install Ikomia API

We strongly recommend using a virtual environment. If you're not sure where to start, we offer a tutorial [here](https://www.ikomia.ai/blog/a-step-by-step-guide-to-creating-virtual-environments-in-python).

```sh
pip install ikomia
```

#### 2. Create your workflow

```python
from ikomia.dataprocess.workflow import Workflow

# Init your workflow
wf = Workflow()

# Add dataset loader:auto_connect is set to False because dataset algorithms don't have any input
dataset_loader = wf.add_task(name="dataset_cwfid", auto_connect=False)

dataset_loader.set_parameters({
    "image_folder": "cwfid_dataset_folder/images"
})

# Add semantic segmentation training algorithm (pick one from Ikomia HUB)
train_algo = wf.add_task(name="train_detectron2_deeplabv3plus", auto_connect=True)

# Run the training workflow
wf.run()
```

## :sunny: Use with Ikomia Studio

Ikomia Studio offers a friendly UI with the same features as the API.

- If you haven't started using Ikomia Studio yet, download and install it from [this page](https://www.ikomia.ai/studio).

- For additional guidance on getting started with Ikomia Studio, check out [this blog post](https://www.ikomia.ai/blog/how-to-get-started-with-ikomia-studio).

## :pencil: Set algorithm parameters

```python
dataset_loader.set_parameters({
    "image_folder": "cwfid_dataset_folder/images"
})
```

- **image_folder** (str): Path to the folder containing dataset images.

*Note*: parameter key and value should be in **string format** when added to the dictionary.
