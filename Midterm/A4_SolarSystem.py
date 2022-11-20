import numpy as np
import cv2


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


# Main

def main():
    # Prepare the canvas
    height, width = 600, 1000
    canvas = np.zeros((height,width,3), dtype='uint8')

    # Set the rotation speed
    sun_self = 0.5 
    venus_rev = 1.5
    earth_rev = 1
    moon_rev = 3
    rocket_rev = 0.2

    degree1 = 0
    degree2 = 0
    degree3 = 0
    degree4 = 0
    degree5 = 0

    while True:
        canvas[:,:,:] = (0,0,0)

        # Sun
        sun = get_regular_ngon(N=20)
        S1 = makeSmat(35)
        R1 = makeRmat(degree1)
        T1 = makeTmat(500,300) 
        H_sun = T1 @ R1
        qT = H_sun @ S1 @ sun.T
        sun_to_draw = qT.T.astype('int')
        draw_polygon(sun_to_draw, canvas, color=(150,220,240))

        # Venus
        venus = get_regular_ngon(N=20)
        S2 = makeSmat(20)
        R2 = makeRmat(degree2)
        R1m = makeRmat(-degree1)
        T2 = makeTmat(100,0)
        H_venus = R2 @ T2 @ R1m
        qT = H_sun @ H_venus @ S2 @ venus.T
        venus_to_draw = qT.T.astype('int')
        draw_polygon(venus_to_draw, canvas, color=(70,70,240))

        # Earth
        earth = get_regular_ngon(N=20)
        S3 = makeSmat(22)
        R3 = makeRmat(degree3)
        T3 = makeTmat(200,0)
        H_earth = R3 @ T3 @ R1m
        qT = H_sun @ H_earth @ S3 @ earth.T
        earth_to_draw = qT.T.astype('int')
        draw_polygon(earth_to_draw, canvas, color=(240,180,0))

        # Moon
        moon = get_regular_ngon(N=20)
        S4 = makeSmat(10)
        R4 = makeRmat(degree4)
        R3m = makeRmat(-degree3)
        T4 = makeTmat(50,0)
        H_moon = R4 @ T4 @ R3m
        qT = H_sun @ H_earth @ H_moon @ S4 @ moon.T
        moon_to_draw = qT.T.astype('int')
        draw_polygon(moon_to_draw, canvas, color=(240,240,210))

        # Rocket
        rocket = get_regular_ngon(N=6)
        S5 = makeSmat(8)
        R5 = makeRmat(degree5)
        T5 = makeTmat(130,0)
        H_rocket = R5 @ T5 @ R1m
        qT = H_sun @ H_rocket @ S5 @ rocket.T
        rocket_to_draw = qT.T.astype('int')
        draw_polygon(rocket_to_draw, canvas, color=(200,20,230))

        degree1 += sun_self
        degree2 += venus_rev
        degree3 += earth_rev
        degree4 += moon_rev
        degree5 += rocket_rev

        # Press [Esc] to turn off the window. 
        cv2.imshow("Solar System", canvas)
        if cv2.waitKey(10) == 27: break
    return

if __name__ == "__main__": 
    main()
