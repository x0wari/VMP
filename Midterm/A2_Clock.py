import numpy as np
import cv2
import datetime as dt

def deg2rad(deg):
    '''
    simply converts the degrees into radians.
    '''
    rad = deg * np.pi / 180.
    return rad


def get_regular_ngon(N):
    '''
    returns the coordinates of the regular N-gon.
    '''
    delta = 360. / N
    points = []
    for i in range(N):
        degree = i * delta
        radian = deg2rad(degree)
        x = np.cos(radian)
        y = np.sin(radian)
        points.append((x, y, 1))
    points = np.array(points)
    return points


def get_line(x0, y0, x1, y1):
    '''
    returns the coordinates of the line connecting (x0,y0) and (x1,y1).
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
    draws the line connecting p and q on the canvas.
    '''
    x0, y0, x1, y1 = p[0], p[1], q[0], q[1]
    xys = get_line(x0, y0, x1, y1)
    for xy in xys:
        x, y = xy
        canvas[y, x, :] = color
    return


def draw_polygon(vertices, canvas, color=(255,255,255)): 
    '''
    draws a polygon on the canvas, according to the color you set.
    * White is the default.
    '''
    for k in range(vertices.shape[0] - 1):
        draw_line(vertices[k], vertices[k+1], canvas, color)
    # Since you need to return to index 0, the last line should be drawn separately.
    draw_line(vertices[-1], vertices[0], canvas, color) 
    return


def makeSmat(scale):
    '''
    generates a scaling matrix.
    '''
    Smat = np.eye(3)
    Smat[0,0] = scale
    Smat[1,1] = scale
    return Smat


def makeRmat(degree):
    '''
    generates a rotation matrix.
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
    generates a translation matrix.
    '''
    Tmat = np.eye(3)
    Tmat[0,2] = tx
    Tmat[1,2] = ty
    return Tmat


def main():
    height, width = 500, 500
    canvas = np.zeros((height, width, 3), dtype='uint8')

    x = dt.datetime.now()
    mintime = x.minute
    hourtime = x.hour
    print(mintime, hourtime)

    msize = 160
    hsize = 100
    minute_degree = 6
    hour_degree = 0.5
    degree1 = mintime * minute_degree
    degree2 = hourtime * hour_degree * 60
    
    # 시계 테두리
    border = get_regular_ngon(36)
    S1 = makeSmat(200)
    T1 = makeTmat(int(width/2), int(height/2))
    qT = T1 @ S1 @ border.T
    border_to_draw = qT.T.astype('int')

    # 분침
    minutehand = np.array([
                        [0, 0, 1],
                        [0, msize, 1]
                        ])

    # 시침
    hourhand = np.array([
                        [0, 0, 1],
                        [0, hsize, 1]
                        ])


    while True:
        canvas[:,:,:] = (255,255,255)
        draw_polygon(border_to_draw, canvas, (100,100,100))

        # 분침
        Tmup = makeTmat(0, -msize)
        T2 = makeTmat(int(width/2), int(height/2))
        R2 = makeRmat(degree1)
        qT = T2 @ R2 @ Tmup @ minutehand.T
        minutehand_to_draw = qT.T.astype('int')
        draw_polygon(minutehand_to_draw, canvas, (255,0,0))

        # 시침
        Thup = makeTmat(0, -hsize)
        T3 = makeTmat(int(width/2), int(height/2))
        R3 = makeRmat(degree2)
        qT = T3 @ R3 @ Thup @ hourhand.T
        hourhand_to_draw = qT.T.astype('int')
        draw_polygon(hourhand_to_draw, canvas, (0,0,255))

        degree1 += minute_degree
        degree2 += hour_degree

        cv2.imshow("Clock", canvas)
        if cv2.waitKey(60000) == 27: break

if __name__ == "__main__": 
    main()
