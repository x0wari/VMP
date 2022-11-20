import numpy as np
import cv2

def main():
    height, width = 600, 1000
    canvas = np.zeros((height, width, 3), dtype='uint8')

    ys = np.random.randint(0, height, 100)
    xs = np.random.randint(0, width, 100)

    while True:
        canvas[:,:,:] = (0,0,0)
        
        for xy in zip(xs, ys):
            x = xy[0]
            y = xy[1]
            canvas[y,x,:] = np.random.randint(0, 255, 3)

        cv2.imshow("Twinkle Stars", canvas)
        if cv2.waitKey(50) == 27: break

if __name__ == "__main__": 
    main()
