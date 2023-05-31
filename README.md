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
    Make Sure the is no space in the path to InPaint_In_PhotoShop. otherwise there will occur an error when doing inpaint.
    
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
    Make Sure you're in folder of lama before you execute these command.
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

## Usage summary
0. Execute main.py
    ```
    python main.py
    ```
1. Click `Load Image` in `File` and choose Image to open.
2. 
    ![1](https://github.com/shanacon/InPaint_In_PhotoShop/assets/79785416/3217d595-2e6b-4d46-a132-1b53fc348ddb)
    
    Don't forget to select **`Open in PhotoShop`** if you want to edit inpaint result in PhotoShop.
    
    If this is your first time opening this image, it may take **5 ~ 10 minutes** to perform segmentation.
    
2. Move your mouse and check which part of image had been segment.

    ![2](https://github.com/shanacon/InPaint_In_PhotoShop/assets/79785416/ad6292e4-e62e-4b78-913b-3876fc8ea438)
    
    You can only see the mask when the **`Mask brush`** is not selected.
    
3. **Double Click** the mask you want to segment and inpaint to perform segmentation and inapint.

    ![4](https://github.com/shanacon/InPaint_In_PhotoShop/assets/79785416/78f17d97-29e8-4c1b-b853-521ea8a6cc79)
    
    Wait for about 1 minute to perform inapint.
    
    ![8](https://github.com/shanacon/InPaint_In_PhotoShop/assets/79785416/669f7af5-1e97-4f48-be0d-c3d1583c7add)
    
    Sometimes the inpainting results may not be optimal, because of the mask generate by segmentation is too small for inpaint.
    
    In that case it is recommend to modify mask by **`Mask brush`**.
    
    For more details, please refer to the [link].
    
3.1 If **`Open in PhotoShop`** had select in step 1, we can edit the result in PhotoShop.

   ![5](https://github.com/shanacon/InPaint_In_PhotoShop/assets/79785416/2666042a-deb8-4310-8439-02d35edeec1c)
    
   ![6](https://github.com/shanacon/InPaint_In_PhotoShop/assets/79785416/300f82ec-af94-4373-85cc-66d1dd5b8f6e)
 
## Usage detail
Check [link]() for all function.
