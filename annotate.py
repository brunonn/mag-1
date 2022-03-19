from PIL import Image
import pytesseract
import argparse
import cv2
import os
import json



def read_from_frame(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)
    text = pytesseract.image_to_string(Image.open(filename), lang="pol")
    os.remove(filename)
    return text



def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dir", required=True,
        help="path to input directory to be OCR'd")
    args = vars(ap.parse_args())
    json_file = {
        "frames": []        
    }
    for file_path in os.listdir(args['dir']):
        full_path = args['dir'] + '/' + file_path
        text = read_from_frame(full_path)
        json_file['frames'].append({
            "file_name": file_path,
            "text": text
        })
    f = open(args['dir']+".json", "w")
    f.write(json.dumps(json_file))
    f.close()


if __name__ == "__main__":
    main()