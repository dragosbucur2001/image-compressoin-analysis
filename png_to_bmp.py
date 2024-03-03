#!/bin/python3
import imagecodecs
from PIL import Image
import cv2
from skimage.metrics import structural_similarity as ssim
from pathlib import Path
import os
import numpy as np

def calculate_ssim(original_img, decompressed_img):
    original_gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    decompressed_gray = cv2.cvtColor(decompressed_img, cv2.COLOR_BGR2GRAY)

    # Calculate SSIM
    ssim_index, _ = ssim(original_gray, decompressed_gray, full=True)

    return ssim_index


def calculate_ssim_color(original_img, decompressed_img):
    ssim_r, _ = ssim(original_img[:,:,0], decompressed_img[:,:,0], full=True)
    ssim_g, _ = ssim(original_img[:,:,1], decompressed_img[:,:,1], full=True)
    ssim_b, _ = ssim(original_img[:,:,2], decompressed_img[:,:,2], full=True)

    # Take the average or weighted average
    ssim_index = (ssim_r + ssim_g + ssim_b) / 3.0

    return ssim_index


print("image,method,params,SSIM,SSIM_C,compression_ratio")
for filename in os.scandir("png_images"):
    if not filename.is_file():
        continue

    # print(f"Converting {filename.name}")

    stem = Path(filename.path).stem;
    img = Image.open(filename.path).convert("RGB")

    bmp_path = os.path.join("bmp_images", f"{stem}.bmp")
    img.save(bmp_path)
    original_img = cv2.imread(bmp_path)

    # compressed_path = os.path.join("compressed_images", f"{stem}.jls")
    # imagecodecs.jpegls_encode(img.tobytes(), compressed_path)

    # decompressed_img = Image.open(compressed_path).convert("RGB")

    # decompressed_path = os.path.join("decompressed_images", f"{stem}_jls.bmp")
    # decompressed_img.save(decompressed_path)
    # decompressed_img = cv2.imread(decompressed_path)

    # ssim_res = calculate_ssim(original_img, decompressed_img)
    # ssim_color_res = calculate_ssim_color(original_img, decompressed_img)
    # compression_ratio = os.path.getsize(bmp_path) / os.path.getsize(compressed_path)

    # print(f"Compressed with JPEG-LS, quality level {quality_level}: SSIM={ssim_res:.3f}, SSIM_C={ssim_color_res:.3f}, compression_ratio={compression_ratio:.3f}")


    for resample_method in [Image.LANCZOS, Image.BICUBIC]:
        # print("------------------------")
        for resize_ratio in [.95, .90, .80, .70, .60, .50]:
            compressed_path = os.path.join("compressed_images", f"{stem}_{resize_ratio}.bmp")
            old_size, _ = img.size
            new_size = round(old_size * resize_ratio)

            img.resize((new_size, new_size), resample=resample_method).save(compressed_path)

            decompressed_img = Image.open(compressed_path).resize((old_size, old_size), resample=resample_method)

            decompressed_path = os.path.join("decompressed_images", f"{stem}_{old_size}_{new_size}_{resample_method}.bmp")
            decompressed_img.save(decompressed_path)
            decompressed_img = cv2.imread(decompressed_path)

            ssim_res = calculate_ssim(original_img, decompressed_img)
            ssim_color_res = calculate_ssim_color(original_img, decompressed_img)
            compression_ratio = os.path.getsize(bmp_path) / os.path.getsize(compressed_path)
            word = "LANCZOS" if resample_method == 1 else "BICUBIC"
            print(f"{stem},resize,{old_size}_{new_size}_{word},{ssim_res},{ssim_color_res},{compression_ratio}")

            # print(f"Downscaled from {old_size}x{old_size} to {new_size}x{new_size}, with {resample_method}: SSIM={ssim_res:.3f}, SSIM_C={ssim_color_res:.3f}, compression_ratio={compression_ratio:.3f}")

    # print("------------------------")
    for compression_level in [1, 9]:
        compressed_path = os.path.join("compressed_images", f"{stem}_{compression_level}.png")
        img.save(compressed_path, "PNG", compression_level=compression_level)

        decompressed_img = Image.open(compressed_path).convert("RGB")

        decompressed_path = os.path.join("decompressed_images", f"{stem}_{compression_level}_png.bmp")
        decompressed_img.save(decompressed_path)
        decompressed_img = cv2.imread(decompressed_path)

        ssim_res = calculate_ssim(original_img, decompressed_img)
        ssim_color_res = calculate_ssim_color(original_img, decompressed_img)
        compression_ratio = os.path.getsize(bmp_path) / os.path.getsize(compressed_path)
        print(f"{stem},PNG,{compression_level},{ssim_res},{ssim_color_res},{compression_ratio}")

        # print(f"Compressed with PNG, compression level {compression_level}: SSIM={ssim_res:.3f}, SSIM_C={ssim_color_res:.3f}, compression_ratio={compression_ratio:.3f}")


    # print("------------------------")
    for quality_level in [100, 95, 90, 85, 80, 70, 50]:
        compressed_path = os.path.join("compressed_images", f"{stem}_{quality_level}.jpeg")
        img.save(compressed_path, "JPEG", quality=quality_level)

        decompressed_img = Image.open(compressed_path).convert("RGB")

        decompressed_path = os.path.join("decompressed_images", f"{stem}_{quality_level}_jpeg.bmp")
        decompressed_img.save(decompressed_path)
        decompressed_img = cv2.imread(decompressed_path)

        ssim_res = calculate_ssim(original_img, decompressed_img)
        ssim_color_res = calculate_ssim_color(original_img, decompressed_img)
        compression_ratio = os.path.getsize(bmp_path) / os.path.getsize(compressed_path)
        print(f"{stem},JPEG,{quality_level},{ssim_res},{ssim_color_res},{compression_ratio}")

        # print(f"Compressed with JPEG, quality level {quality_level}: SSIM={ssim_res:.3f}, SSIM_C={ssim_color_res:.3f}, compression_ratio={compression_ratio:.3f}")

    # print()
    # print()

