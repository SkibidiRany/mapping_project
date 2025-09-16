import numpy as np

def normalize(v):
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v

def rotate(v, angle_rad):
    """Rotate vector v by angle_rad (in radians)."""
    c, s = np.cos(angle_rad), np.sin(angle_rad)
    rot_matrix = np.array([[c, -s], [s, c]])
    return rot_matrix @ v

def project_point(origin, direction, distance):
    """Given origin O, direction v, and distance d → return new point P."""
    v = normalize(direction)
    return origin + distance * v
