import cv2
 
import numpy as np
 
# BGR -> HSV
 
def BGR2HSV(_img):
 
    img = _img.copy() / 255.
 
    hsv = np.zeros_like(img, dtype=np.float32)
 
    # get max and min
 
    max_v = np.max(img, axis=2).copy()
 
    min_v = np.min(img, axis=2).copy()
 
    min_arg = np.argmin(img, axis=2)
 
    # H
 
    hsv[..., 0][np.where(max_v == min_v)]= 0
 
    ## if min == B
 
    ind = np.where(min_arg == 0)
 
    hsv[..., 0][ind] = 60 * (img[..., 1][ind] - img[..., 2][ind]) / (max_v[ind] - min_v[ind]) + 60
 
    ## if min == R
 
    ind = np.where(min_arg == 2)
 
    hsv[..., 0][ind] = 60 * (img[..., 0][ind] - img[..., 1][ind]) / (max_v[ind] - min_v[ind]) + 180
 
    ## if min == G
 
    ind = np.where(min_arg == 1)
 
    hsv[..., 0][ind] = 60 * (img[..., 2][ind] - img[..., 0][ind]) / (max_v[ind] - min_v[ind]) + 300
 
    # S
 
    hsv[..., 1] = max_v.copy() - min_v.copy()
 
    # V
 
    hsv[..., 2] = max_v.copy()
 
    return hsv
 
def HSV2BGR(_img, hsv):
 
    img = _img.copy() / 255.
 
    # get max and min
 
    max_v = np.max(img, axis=2).copy()
 
    min_v = np.min(img, axis=2).copy()
 
    out = np.zeros_like(img)
 
    H = hsv[..., 0]
 
    S = hsv[..., 1]
 
    V = hsv[..., 2]
 
    C = S
 
    H_ = H / 60.
 
    X = C * (1 - np.abs( H_ % 2 - 1))
 
    Z = np.zeros_like(H)
 
    vals = [[Z,X,C], [Z,C,X], [X,C,Z], [C,X,Z], [C,Z,X], [X,Z,C]]
 
    for i in range(6):
 
        ind = np.where((i <= H_) & (H_ < (i+1)))
 
        out[..., 0][ind] = (V - C)[ind] + vals[i][0][ind]
 
        out[..., 1][ind] = (V - C)[ind] + vals[i][1][ind]
 
        out[..., 2][ind] = (V - C)[ind] + vals[i][2][ind]
 
    out[np.where(max_v == min_v)] = 0
 
    out = np.clip(out, 0, 1)
 
    out = (out * 255).astype(np.uint8)
 
    return out


def rgb_to_hsv(arr):
    """
    convert float rgb values (in the range [0, 1]), in a numpy array to hsv
    values.

    Parameters
    ----------
    arr : (..., 3) array-like
       All values must be in the range [0, 1]

    Returns
    -------
    hsv : (..., 3) ndarray
       Colors converted to hsv values in range [0, 1]
    """
    # make sure it is an ndarray
    arr = np.asarray(arr)

    # check length of the last dimension, should be _some_ sort of rgb
    if arr.shape[-1] != 3:
        raise ValueError("Last dimension of input array must be 3; "
                         "shape {shp} was found.".format(shp=arr.shape))

    in_ndim = arr.ndim
    if arr.ndim == 1:
        arr = np.array(arr, ndmin=2)

    # make sure we don't have an int image
    if arr.dtype.kind in ('iu'):
        arr = arr.astype(np.float32)

    out = np.zeros_like(arr)
    arr_max = arr.max(-1)
    ipos = arr_max > 0
    delta = arr.ptp(-1)
    s = np.zeros_like(delta)
    s[ipos] = delta[ipos] / arr_max[ipos]
    ipos = delta > 0
    # red is max
    idx = (arr[..., 0] == arr_max) & ipos
    out[idx, 0] = (arr[idx, 1] - arr[idx, 2]) / delta[idx]
    # green is max
    idx = (arr[..., 1] == arr_max) & ipos
    out[idx, 0] = 2. + (arr[idx, 2] - arr[idx, 0]) / delta[idx]
    # blue is max
    idx = (arr[..., 2] == arr_max) & ipos
    out[idx, 0] = 4. + (arr[idx, 0] - arr[idx, 1]) / delta[idx]

    out[..., 0] = (out[..., 0] / 6.0) % 1.0
    out[..., 1] = s
    out[..., 2] = arr_max

    if in_ndim == 1:
        out.shape = (3,)

    return out

def hsv_to_rgb(hsv):
    """
    convert hsv values in a numpy array to rgb values
    all values assumed to be in range [0, 1]

    Parameters
    ----------
    hsv : (..., 3) array-like
       All values assumed to be in range [0, 1]

    Returns
    -------
    rgb : (..., 3) ndarray
       Colors converted to RGB values in range [0, 1]
    """
    hsv = np.asarray(hsv)

    # check length of the last dimension, should be _some_ sort of rgb
    if hsv.shape[-1] != 3:
        raise ValueError("Last dimension of input array must be 3; "
                         "shape {shp} was found.".format(shp=hsv.shape))

    # if we got pased a 1D array, try to treat as
    # a single color and reshape as needed
    in_ndim = hsv.ndim
    if in_ndim == 1:
        hsv = np.array(hsv, ndmin=2)

    # make sure we don't have an int image
    if hsv.dtype.kind in ('iu'):
        hsv = hsv.astype(np.float32)

    h = hsv[..., 0]
    s = hsv[..., 1]
    v = hsv[..., 2]

    r = np.empty_like(h)
    g = np.empty_like(h)
    b = np.empty_like(h)

    i = (h * 6.0).astype(np.int)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))

    idx = i % 6 == 0
    r[idx] = v[idx]
    g[idx] = t[idx]
    b[idx] = p[idx]

    idx = i == 1
    r[idx] = q[idx]
    g[idx] = v[idx]
    b[idx] = p[idx]

    idx = i == 2
    r[idx] = p[idx]
    g[idx] = v[idx]
    b[idx] = t[idx]

    idx = i == 3
    r[idx] = p[idx]
    g[idx] = q[idx]
    b[idx] = v[idx]

    idx = i == 4
    r[idx] = t[idx]
    g[idx] = p[idx]
    b[idx] = v[idx]

    idx = i == 5
    r[idx] = v[idx]
    g[idx] = p[idx]
    b[idx] = q[idx]

    idx = s == 0
    r[idx] = v[idx]
    g[idx] = v[idx]
    b[idx] = v[idx]

    rgb = np.empty_like(hsv)
    rgb[..., 0] = r
    rgb[..., 1] = g
    rgb[..., 2] = b

    if in_ndim == 1:
        rgb.shape = (3, )

    return rgb


def hsv2rgb(h, s, v):
    h60 = int(h * 6.0)
    hi = h60 % 6
    f = h *6.0 - h60
    p = v * (1.0 - s)
    q = v * (1.0 - f * s)
    t = v * (1.0 - (1.0 - f) * s)
    if hi == 0:
        return v, t, p
    elif hi == 1:
        return q, v, p
    elif hi == 2:
        return p, v, t
    elif hi == 3:
        return p, q, v
    elif hi == 4:
        return t, p, v
    else:  #  hi == 5:
        return v, p, q

def rgb2hsv(r, g, b):
    mx = np.max([r, g, b])
    mn = np.min([r, g, b])
    df = mx-mn
    if mx == mn:
        h = 0.0
    elif mx == r:
        h = (((g-b)/df))
    elif mx == g:
        h = (((b-r)/df) + 2.0)
    else:  # mx == b
        h = (((r-g)/df) + 4.0)
    if mx == 0:
        s = 0.0
    else:
        s = df/mx
    h = h/6.0%1.0
    v = mx
    return h, s, v
