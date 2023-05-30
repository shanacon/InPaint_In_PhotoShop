from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
from PIL import Image
from numpy import asarray
import os
import cv2
from typing import Any, Dict, List

def GenerateMask(img_path) :
    sam = sam_model_registry["vit_b"](checkpoint="sam_vit_b_01ec64.pth")
    mask_generator = SamAutomaticMaskGenerator(sam)
    img = Image.open(img_path)
    img = asarray(img)
    masks = mask_generator.generate(img)
    output_path = os.path.join('mask', os.path.splitext(os.path.basename(img_path))[0])
    os.makedirs(output_path, exist_ok=True)
    write_masks_to_folder(masks, output_path)

def write_masks_to_folder(masks: List[Dict[str, Any]], path: str) -> None:
    header = "id,area,bbox_x0,bbox_y0,bbox_w,bbox_h,point_input_x,point_input_y,predicted_iou,stability_score,crop_box_x0,crop_box_y0,crop_box_w,crop_box_h"  # noqa
    metadata = [header]
    for i, mask_data in enumerate(masks):
        mask = mask_data["segmentation"]
        filename = f"{i}.png"
        cv2.imwrite(os.path.join(path, filename), mask * 255)
        mask_metadata = [
            str(i),
            str(mask_data["area"]),
            *[str(x) for x in mask_data["bbox"]],
            *[str(x) for x in mask_data["point_coords"][0]],
            str(mask_data["predicted_iou"]),
            str(mask_data["stability_score"]),
            *[str(x) for x in mask_data["crop_box"]],
        ]
        row = ",".join(mask_metadata)
        metadata.append(row)
    metadata_path = os.path.join(path, "metadata.csv")
    with open(metadata_path, "w") as f:
        f.write("\n".join(metadata))

    return