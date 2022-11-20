import numpy as np
import cv2

def get_block(h=30, w=120):
    '''
    returns the 4 vertices of the block
    '''
    block_vertices = np.array([
        [0, h, 1], 
        [0, 0, 1], 
        [w, 0, 1], 
        [w, h, 1]])
    return block_vertices

def get_line(x0, y0, x1, y1):
    '''
    returns the coordinates of the line connecting (x0,y0) and (x1,y1)
    '''
    points = []
    if abs(x1 - x0) >= abs(y1 - y0):
        if x0 < x1:
            for x in range(x0, x1+1):
                y = (x - x0) * (y1 - y0) / (x1 - x0) + y0
                yint = int(y)
                points.append((x, yint))
        else:
            for x in range(x1, x0-1):
                y = (x - x0) * (y1 - y0) / (x1 - x0) + y0
                yint = int(y)
                points.append((x, yint)) 
        return points
    else:
        if y0 < y1:
            for y in range(y0, y1+1):
                x = (y - y0) * (x1 - x0) / (y1 - y0) + x0
                xint = int(x)
                points.append((xint, y))
        else:
            for y in range(y1, y0-1):
                x = (y - y0) * (x1 - x0) / (y1 - y0) + x0
                xint = int(x)
                points.append((xint, y))
        return points

def draw_line(p, q, canvas, color):
    '''
    draws the line connecting p and q on the canvas
    '''
    x0, y0, x1, y1 = p[0], p[1], q[0], q[1]
    xys = get_line(x0, y0, x1, y1)
    for xy in xys:
        x, y = xy
        canvas[y, x, :] = color
    return

def draw_polygon(vertices, canvas, color=(255,255,255)): 
    '''
    draws a polygon on the canvas
    '''
    vertices = vertices.astype('int')
    for k in range(vertices.shape[0] - 1):
        draw_line(vertices[k], vertices[k+1], canvas, color)
    draw_line(vertices[-1], vertices[0], canvas, color) 
    return

def deg2rad(deg):
    '''
    converts the degrees into radians
    '''
    rad = deg * np.pi / 180.
    return rad

def makeRmat(degree):
    '''
    generates a rotation matrix
    '''
    r = deg2rad(degree)
    c = np.cos(r)
    s = np.sin(r)
    Rmat = np.eye(3)
    Rmat[0,0] = c
    Rmat[0,1] = -s
    Rmat[1,0] = s
    Rmat[1,1] = c
    return Rmat

def makeTmat(tx, ty):
    '''
    generates a translation matrix
    '''
    Tmat = np.eye(3)
    Tmat[0,2] = tx
    Tmat[1,2] = ty
    return Tmat

def erase(canvas):
    '''
    erases everything drawn on the canvas
    '''
    canvas[:, :, :] = (0,0,0)
    return canvas

def main():
    height, width = 600, 1000
    window = np.zeros((height, width, 3), dtype='uint8')

    block_height, block_width = 100, 30
    block = get_block(block_height, block_width).T

    T0 = makeTmat(width/2, height-block_height-1) # 중앙 하단으로
    T1 = makeTmat(-block_width/2, -block_height) # 왼쪽 위로 밀기
    T2 = makeTmat(block_width/2, block_height) # 오른쪽 아래로 밀기
    T3 = makeTmat(0, -block_height) # 위로 밀기

    degree1 = 0
    degree2 = 0
    degree3 = 0
    degree4 = 0

    v1 = 1
    v2 = 2
    v3 = 3
    v4 = 4

    while True:
        erase(window)

        R1 = makeRmat(degree1)
        R2 = makeRmat(degree2)
        R3 = makeRmat(degree3)
        R4 = makeRmat(degree4)

        H1 = T0
        block1 = (H1 @ block).T
        draw_polygon(block1, window)

        H2 = T3 @ T2 @ R1 @ T1
        block2 = (H1 @ H2 @ block).T
        draw_polygon(block2, window, color=(255, 153, 255))

        H3 = T3 @ T2 @ R2 @ T1
        block3 = (H1 @ H2 @ H3 @ block).T
        draw_polygon(block3, window, color=(255, 150, 183))

        H4 = T3 @ T2 @ R3 @ T1
        block4 = (H1 @ H2 @ H3 @ H4 @ block).T
        draw_polygon(block4, window, color=(255, 190, 102))

        H5 = T3 @ T2 @ R4 @ T1
        block5 = (H1 @ H2 @ H3 @ H4 @ H5 @ block).T
        draw_polygon(block5, window, color=(255, 235, 60))

        if degree1 >= 15 or degree1 <= -15:
            v1 = -v1
        if degree2 >= 30 or degree2 <= -30:
            v2 = -v2
        if degree3 >= 45 or degree3 <= -45:
            v3 = -v3
        if degree4 >= 60 or degree4 <= -60:
            v4 = -v4
            
        degree1 += v1
        degree2 += v2
        degree3 += v3
        degree4 += v4

        cv2.imshow("display", window)
        if cv2.waitKey(20) == 27: break
    return

if __name__ == "__main__": 
    main()
