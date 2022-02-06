def object_delta(toponym):
    corners = toponym["boundedBy"]["Envelope"]
    lower_corner = corners["lowerCorner"].split()
    up_corner = corners["upperCorner"].split()
    object_x = str(abs(float(up_corner[0]) - float(lower_corner[0])))
    object_y = str(abs(float(up_corner[1]) - float(lower_corner[1])))
    return object_x, object_y