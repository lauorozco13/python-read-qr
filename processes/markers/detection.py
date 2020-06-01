"""This module looks for markers through images processing taken from camera frames"""

from cv2 import cvtColor, createCLAHE, threshold, \
                GaussianBlur, Canny, findContours, contourArea, arcLength, \
                approxPolyDP, drawContours, flip, countNonZero, \
                COLOR_BGR2GRAY, THRESH_OTSU, RETR_TREE, CHAIN_APPROX_SIMPLE, RETR_LIST
from . import markers
from processes.constants import QUADRILATERAL_POINTS, BLACK_THRESHOLD, THRESHOLD_PERCENT
from processes.helpers import get_topdown_quad

def detect(image):
    """Detect marker from the camera image"""
    markers = []
    # Stage 1: Detect edges in image
    gray = cvtColor(image, COLOR_BGR2GRAY)
    clahe = createCLAHE(clipLimit=1, tileGridSize=(6, 6))
    cl1 = clahe.apply(gray)
    _, thresh = threshold(cl1, 60, 255, THRESH_OTSU)
    blurred = GaussianBlur(thresh, (5, 5), 0)
    edges = Canny(blurred, 75, 100)

    # Stage 2: Find contours
    contours = findContours(edges, RETR_TREE, CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=contourArea, reverse=True)[:]

    for contour in contours:
        # Stage 3: Shape check
        perimeter = arcLength(contour, True)
        approx = approxPolyDP(contour, 0.01*perimeter, True)

        if len(approx) == QUADRILATERAL_POINTS:
            area = contourArea(approx)
            # (x, y, w, h) = boundingRect(approx)
            # ar = float(h) / float(w)
            # if area > 100 and ar >= 0.8 and ar <= 1.2:
            if area > 700:
                # putText(image, str(area), (10, 30), FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                drawContours(image, [contour], -1, (0, 255, 0), 1)

                # Stage 4: Perspective warping
                topdown_quad = get_topdown_quad(thresh, approx.reshape(4, 2))

                # Stage 5: Border check
                if topdown_quad[int((topdown_quad.shape[0]/100.0)*5), int((topdown_quad.shape[1]/100.0)*5)] > BLACK_THRESHOLD:
                    continue

                # Stage 6: Get marker pattern
                marker_pattern = None

                try:
                    marker_pattern = get_marker_pattern(topdown_quad, THRESHOLD_PERCENT)
                except:
                    continue

                if not marker_pattern:
                    continue

                # Stage 7: Match marker pattern
                marker_found, marker_rotation, marker_name = match_marker_pattern(marker_pattern)

                if marker_found:
                    markers.append([marker_name, marker_rotation])

    return markers, image


def get_marker_pattern(image, threshold_percent):
    """Construct marker pattern"""
    # recolecto puntos de cada celda (left to right, top to bottom)
    cells = []
    anchoBorde = int(image.shape[1] * 0.075)

    image = image[anchoBorde:-anchoBorde, anchoBorde:-anchoBorde]
    wCell = int(round(image.shape[1] / 5.0))
    hCell = int(round(image.shape[0] / 5.0))

    margen = 0
    c = []
    for h in range(1,4):
        for w in range (1,4):
            tempIM = image [
                hCell*h+margen: -1*(image.shape[0]-hCell*(h+1))-margen,
                wCell*w+margen: -1*(image.shape[1]-wCell*(w+1))-margen
            ]
            total = (float(countNonZero(tempIM))/float((wCell-margen)*(hCell-margen)))*100       
            c.append ([tempIM, total])
            cells.append (total)

    # print "INICIAL"
    # for i in range(0, len(c)):
    #     print i, c[i][1]
    #     # imshow("c" + str(i)  , c[i][0])
    #     # resizeWindow("c" + str(i), int(300), int(100))
    # print "FINAL"

    for idx, val in enumerate(cells):
        if val < threshold_percent:
            cells[idx] = 0
        else:
            cells[idx] = 1

    return cells


def match_marker_pattern(marker_pattern):
    """Match marker pattern to database record"""
    marker_found = False
    marker_rotation = None
    marker_name = None
    for marker_record in MARKER_TABLE:
        for idx, val in enumerate(marker_record[0]):
            if marker_pattern == val:
                marker_found = True
                marker_rotation = idx
                marker_name = marker_record[1]
                break
        if marker_found:
            break
    return (marker_found, marker_rotation, marker_name)
