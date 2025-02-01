""# MIT License
# 
# Copyright (c) 2025 EAST TIMOR GHOST SECURITY
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import base64
import hashlib
import os
import cv2
import numpy as np
import pytesseract
from stegano import lsb

# Konfigurasi Tesseract (Opsional, hanya jika dibutuhkan)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def convert_file_to_base64(file_path):

    if not os.path.exists(file_path):
        print("❌File not found!")
        return None

    with open(file_path, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode()
    return encoded_string

def convert_base64_to_file(encoded_string, output_path):

    with open(output_path, "wb") as file:
        file.write(base64.b64decode(encoded_string))
    print(f"✅ The file was successfully saved in {output_path}")

def convert_file_to_hash(file_path):

    if not os.path.exists(file_path):
        print("❌ File not found!")
        return None

    hasher = hashlib.sha256()
    with open(file_path, "rb") as file:
        buf = file.read()
        hasher.update(buf)
    return hasher.hexdigest()

def verify_file_with_hash(file_path, expected_hash):

    if not os.path.exists(file_path):
        print("❌ File not found!")
        return False

    return convert_file_to_hash(file_path) == expected_hash

def embed_message_in_image(image_path, message, output_path):

    if not os.path.exists(image_path):
        print("❌ Image not found!")
        return

    secret_image = lsb.hide(image_path, message)
    secret_image.save(output_path)
    print(f"✅ The message has embed in the image {output_path}")

def extract_message_from_image(image_path):
  
    if not os.path.exists(image_path):
        print("❌ Image not found!")
        return None

    return lsb.reveal(image_path)

def embed_message_in_video(video_path, message, output_path):
   
    if not os.path.exists(video_path):
        print("❌ Video not found!!")
        return

    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    # Pisahkan teks panjang menjadi beberapa baris
    formatted_message = message.replace(" ", r'\ ')
    
    os.system(
        f'ffmpeg -i "{video_path}" -vf "drawtext=fontfile={font_path}:text=\'{formatted_message}\':x=(w-text_w)/2:y=(h-text_h)/2:fontsize=70:fontcolor=white:borderw=6:bordercolor=black" -codec:a copy "{output_path}"'
    )

    print(f"✅ The message has embed in video {output_path}")

def extract_text_from_video(video_path):
   
    if not os.path.exists(video_path):
        print("❌ Video not found!")
        return

    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    extracted_text = []

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        if frame_count % 5 == 0:  # Ambil frame lebih sering untuk pesan panjang
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)
            _, gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            temp_image = f"temp_frame_{frame_count}.png"
            cv2.imwrite(temp_image, gray)

            # Menggunakan mode --psm 3 agar lebih optimal untuk teks panjang
            text = pytesseract.image_to_string(temp_image, config="--psm 3")
            os.remove(temp_image)

            cleaned_text = text.strip()
            if cleaned_text:
                extracted_text.append(cleaned_text)

        frame_count += 1

    cap.release()

    if extracted_text:
        print("\n🔍 **Messages found:**\n")
        for line in extracted_text:
            print(f"➡️ {line}")
    else:
        print("❌ No text can be extracted from the video.")

# ASCII Banner
ascii_banner = """
\033[93m███████╗ █████╗ ███████╗████████╗    ████████╗██╗███╗   ███╗ ██████╗ ██████╗      ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗███████╗███████╗ ██████╗
\033[93m██╔════╝██╔══██╗██╔════╝╚══██╔══╝    ╚══██╔══╝██║████╗ ████║██╔═══██╗██╔══██╗    ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝██╔════╝
\033[97m█████╗  ███████║███████╗   ██║          ██║   ██║██╔████╔██║██║   ██║██████╔╝    ██║  ███╗███████║██║   ██║███████╗   ██║   ███████╗█████╗  ██║     
\033[97m██╔══╝  ██╔══██║╚════██║   ██║          ██║   ██║██║╚██╔╝██║██║   ██║██╔══██╗    ██║   ██║██╔══██║██║   ██║╚════██║   ██║   ╚════██║██╔══╝  ██║     
\033[91m███████╗██║  ██║███████║   ██║          ██║   ██║██║ ╚═╝ ██║╚██████╔╝██║  ██║    ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   ███████║███████╗╚██████╗
\033[91m╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝          ╚═╝   ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚══════╝ ╚═════╝
                                   version: 1.1
"""

print(ascii_banner)
                                               
def main():
   
    while True:
        print("""
=======TOOLS BASE64, HASH & STEGANOGRAPHY=========
[1] Convert file to Base64
[2] Convert Base64 to file
[3] Convert file to Hash (SHA-256)
[4] Verify file with hash
[5] Embed secret message in image
[6] Extract secret message from image
[7] Embed secret message in video
[8] Extract secret message from video
[9] Exit
""")
        option = input("Select options [1-9]: ")

        if option == "1":
            file_path = input("Input file path: ")
            result = convert_file_to_base64(file_path)
            if result:
                print("Base64 Encoded:", result)

        elif option == "2":
            encoded_string = input("Input Base64 string: ")
            output_path = input("Input path file output: ")
            convert_base64_to_file(encoded_string, output_path)

        elif option == "3":
            file_path = input("Input file path: ")
            result = convert_file_to_hash(file_path)
            if result:
                print("SHA-256 Hash:", result)

        elif option == "4":
            file_path = input("Input file path: ")
            expected_hash = input("Enter the expected hash: ")
            if verify_file_with_hash(file_path, expected_hash):
                print("✅ Hash matches!")
            else:
                print("❌ Hashes don't match!")

        elif option == "5":
            image_path = input("Enter image path: ")
            message = input("Embed a secret message: ")
            output_path = input("input image output path: ")
            embed_message_in_image(image_path, message, output_path)

        elif option == "6":
            image_path = input("Enter image path: ")
            extracted_message = extract_message_from_image(image_path)
            if extracted_message:
                print("Extracted messages:", extracted_message)
            else:
                print("❌ No messages found.")

        elif option == "7":
            video_path = input("Enter video path: ")
            message = input("Embed secret message: ")
            output_path = input("Enter video output path: ")
            embed_message_in_video(video_path, message, output_path)

        elif option == "8":
            video_path = input("Input video path: ")
            extract_text_from_video(video_path)

        elif option == "9":
            print("👋 THANK YOU FOR USING THE TOOLS.")
            break

        else:
            print("❌ INVALID OPTIONS, PLEASE TRY AGAIN.")

if __name__ == "__main__":
    main()
