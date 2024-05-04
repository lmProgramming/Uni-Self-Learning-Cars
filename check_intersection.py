from shapely.geometry import LineString, Point

def onSegment(p, q, r): 
    if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and 
           (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))): 
        return True
    return False
  
def orientation(p, q, r): 
    # to find the orientation of an ordered triplet (p,q,r) 
    # function returns the following values: 
    # 0 : Collinear points 
    # 1 : Clockwise points 
    # 2 : Counterclockwise 
      
    # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/  
    # for details of below formula.  
      
    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y)) 
    if (val > 0): 
          
        # Clockwise orientation 
        return 1
    elif (val < 0): 
          
        # Counterclockwise orientation 
        return 2
    else: 
          
        # Collinear orientation 
        return 0
  
# The main function that returns true if  
# the line segment 'p1q1' and 'p2q2' intersect. 
def doIntersect(p1,q1,p2,q2): 
      
    # Find the 4 orientations required for  
    # the general and special cases 
    o1 = orientation(p1, q1, p2) 
    o2 = orientation(p1, q1, q2) 
    o3 = orientation(p2, q2, p1) 
    o4 = orientation(p2, q2, q1) 
  
    # General case 
    if ((o1 != o2) and (o3 != o4)): 
        return True
  
    # If none of the cases 
    return False

def overlap_point_distance(p1, p2, q1, q2):
    def on_segment(p, q, r):
        if (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
                q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])):
            return True
        return False

    # Check for overlap
    if not (min(p1[0], p2[0]) <= max(q1[0], q2[0]) and max(p1[0], p2[0]) >= min(q1[0], q2[0]) and
            min(p1[1], p2[1]) <= max(q1[1], q2[1]) and max(p1[1], p2[1]) >= min(q1[1], q2[1])):
        return None  # Segments don't overlap

    # Calculate the intersection point (assuming segments overlap)
    x_diff_p = p2[0] - p1[0]
    y_diff_p = p2[1] - p1[1]
    x_diff_q = q2[0] - q1[0]
    y_diff_q = q2[1] - q1[1]

    determinant = x_diff_p * y_diff_q - y_diff_p * x_diff_q
    if determinant == 0:
        return None  # Parallel segments

    t = ((q1[0] - p1[0]) * y_diff_q - (q1[1] - p1[1]) * x_diff_q) / determinant
    overlap_point = (p1[0] + t * x_diff_p, p1[1] + t * y_diff_p)

    # Check if the overlap point lies on both segments
    if not (on_segment(p1, overlap_point, p2) and on_segment(q1, overlap_point, q2)):
        return None  # Overlap point does not lie on both segments

    # Calculate distance between p1 and overlap point
    distance = ((p1[0] - overlap_point[0]) ** 2 + (p1[1] - overlap_point[1]) ** 2) ** 0.5
    return distance

# Example usage
p1 = (1, 1)
p2 = (4, 4)
q1 = (2, 3)
q2 = (5, 2)

distance = overlap_point_distance(p1, p2, q1, q2)
if distance is not None:
    print("Distance between p1 and overlap point:", distance)
else:
    print("Segments do not overlap.")



def check_if_intersect(car_ray, border):
    A = Point(car_ray.get_origin_position().x, car_ray.get_origin_position().y)
    B = Point(car_ray.get_end_position().x, car_ray.get_end_position().y)

    C = Point(border.start_position.x, border.start_position.y)
    D = Point(border.end_position.x, border.end_position.y)
    distance = overlap_point_distance(p1, p2, q1, q2)
    #if distance is not None:
    #return 

    line1 = LineString([A, B])
    line2 = LineString([C, D])
#
    int_pt = line1.intersection(line2)
#
    if int_pt.is_empty:
        return False, 0, 0
    else:
        return True, int_pt.x, int_pt.y