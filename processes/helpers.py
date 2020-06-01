from cv2 import getPerspectiveTransform, warpPerspective
from numpy import array, argsort, newaxis, sqrt
from scipy.spatial.distance import cdist


def _order_points(pts):
    xSorted = pts[argsort(pts[:, 0]), :]
    leftMost = xSorted[:2, :]
    rightMost = xSorted[2:, :]
    leftMost = leftMost[argsort(leftMost[:, 1]), :]
    (tl, bl) = leftMost
    D = cdist(tl[newaxis], rightMost, "euclidean")[0]
    (br, tr) = rightMost[argsort(D)[::-1], :]
    return array([tl, tr, br, bl], dtype="float32")


def _max_width_height(points):
    (tl, tr, br, bl) = points

    top_width = sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    bottom_width = sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    max_width = max(int(top_width), int(bottom_width))

    left_height = sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    right_height = sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    max_height = max(int(left_height), int(right_height))

    return (max_width, max_height)


def _topdown_points(max_width, max_height):
    return array([
        [0, 0],
        [max_width-1, 0],
        [max_width-1, max_height-1],
        [0, max_height-1]], dtype='float32')


def get_topdown_quad(image, src):
    # src and dst points
    src = _order_points(src)
    (max_width,max_height) = _max_width_height(src)
    dst = _topdown_points(max_width, max_height)
    # warp perspective
    matrix = getPerspectiveTransform(src, dst)
    warped = warpPerspective(image, matrix, _max_width_height(src))

    return warped

"""
def get_vectors(image, points, mtx, dist):
    # llamo la funcion de ordenar puntos
    points = _order_points(points)

    # configuro criteria, image, points and axis
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   
    imgp = np.array(points, dtype='float32')

    objp = np.array([[0.,0.,0.],[1.,0.,0.],
            [1.,1.,0.],[0.,1.,0.]], dtype="float32")
 
    corners2 = cv2.cornerSubPix(gray,imgp,(11,11),(-1,-1),criteria)
    corners3 = np.zeros((4, 1, 2), np.float32)

    for x in range(0,4):
        corners3[x,0] = corners2[x]

    _, rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners3, mtx, dist)

    return rvecs, tvecs
"""
