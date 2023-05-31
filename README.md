# InPaint In PhotoShop
## Introduction
This is a tool to inpaint in PhotoShop.\
We use [segment-anything](https://github.com/facebookresearch/segment-anything), [LaMa](https://github.com/advimman/lama) and [photoshop-python-api](https://github.com/loonghao/photoshop-python-api) in our work.
## Environment setting
1. Clone this repo
    ```
    git clone https://github.com/shanacon/InPaint_In_PhotoShop.git
    cd InPaint_In_PhotoShop
    ```
2. Install packages
    ```
    pip install torch torchvision torchaudio
    ```
    Remind that only the version with cuda is support is this tool.
    ```
    pip install git+https://github.com/facebookresearch/segment-anything.git
    pip install photoshop-python-api
    ```
3. Set up LaMa
    ```
    git clone https://github.com/advimman/lama.git
    cd lama
    pip install -r requirements.txt
   ```
    **If your Python version is > 3.9, you need to install `scikit-image` and `scikit-learn` separately.**\
    After install `scikit-image` and `scikit-learn` separately, remove them from `requirements.txt` and call
    ```
    pip install -r requirements.txt
    ```
4. Set environment variable for lama
    Add path to lama to `TORCH_HOME` and `PYTHONPATH` in Environment Variables.\
    **It is recommend to do it in windows setting instead of the command below.**\
    In cmd:
    ```
    setx TORCH_HOME %TORCH_HOME%;%cd%
    setx PYTHONPATH %PYTHONPATH%;%cd%
    ```
    or in PowerShell:
    
    ```
    setx PYTHONPATH "$env:PYTHONPATH;$(PWD)"
    setx TORCH_HOME "$env:TORCH_HOME;$(PWD)"
    ```
    Make Sure you're in foler of lama before you execute these command.
5. Comment one line in lama
    Comment `register_debug_signal_handlers()` in `\lama\bin\predict.py` (line 41)
6. Download checkpoint of lama
    ```
    curl $(yadisk-direct https://disk.yandex.ru/d/ouP6l8VJ0HpMZg) -o big-lama.zip
    ```
    Then unzip big-lama.zip (unzip in \lama)
7. Download checkpoint of segment-anything.

    Back to folder of InPaint_In_PhotoShop
    ```
    cd ..
    ```
    Download checkopoint of `ViT-B SAM model` at [here](https://github.com/facebookresearch/segment-anything#model-checkpoints).
