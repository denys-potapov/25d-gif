import argparse
import cv2
import os
import numpy as np
import glob
import math

def join(input, output):
    FULL_SIZE = 4096
    FRAME_WIDTH = 512
    COLUMNS_PER_ROW = int(math.floor(FULL_SIZE / FRAME_WIDTH))

    inputs = sorted(glob.glob(input))
    
    # get size from first frame
    frame = cv2.imread(inputs[0], cv2.IMREAD_COLOR)
    height, width, _ = frame.shape

    # double
    width = width * 2
    height = round(height / (width / FRAME_WIDTH))
    width = FRAME_WIDTH

    print("max count", int(math.floor(FULL_SIZE / height)) * COLUMNS_PER_ROW - 1)
    print("""h w
    color: {{
        source: "{}",
        width: {} / {},
        height: {} / {},
        per_row: {}
    }}
    """.format(output, width, FULL_SIZE, height, FULL_SIZE, COLUMNS_PER_ROW))

    # prepare the result
    result = np.zeros((FULL_SIZE, FULL_SIZE, 3), np.uint8)

    for i, input in enumerate(inputs):
        print('frame', i)
        frame = cv2.imread(input, cv2.IMREAD_COLOR)
        frame = cv2.resize(frame, (width, height))

        # place image
        row, col = divmod(i, COLUMNS_PER_ROW)
        y = row * height
        x = col * width
        result[y:y+height, x:x+width] = frame

    cv2.imwrite(output, result)

if __name__ == '__main__':
    desc = """color frame joiner"""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=desc)

    parser.add_argument('input', type=str, help='input file pattern')

    parser.add_argument('output', type=str, help='output image file')

    args = parser.parse_args()
    join(args.input, args.output)
