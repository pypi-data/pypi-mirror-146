import numpy as np 
import cv2

def crinex_edge(img, filter_size=(3,3),  stride=1):
    img_shape = img.shape
    result_shape = tuple(np.int64((np.array(img_shape) - np.array(filter_size))/stride))

    # Generate Zero Matrix
    for i in range(2):
        globals()[f'result{i+1}'] = np.zeros(result_shape)

    global result1 
    global result2 

    # 1st Filter(h, w)
    for h in range(0, result_shape[0], stride):
        for w in range(0, result_shape[1], stride):
            tmp = img[h:h+filter_size[0], w:w+filter_size[1]]
            tmp = np.sort(tmp.ravel())
            result1[h,w] = tmp[int(filter_size[0]*filter_size[1]/2)]
            
    # 2nd Filter(h, w+1)
    for h in range(0, result_shape[0], stride):
        for w in range(0, result_shape[1], stride):
            tmp = img[h:h+filter_size[0], w+1:w+1+filter_size[1]]
            tmp = np.sort(tmp.ravel())
            result2[h,w] = tmp[int(filter_size[0]*filter_size[1]/2)]

    result1 = cv2.resize(result1, (224, 224))
    result2 = cv2.resize(result2, (224, 224))

    result1 = result1.astype('uint16')
    result2 = result2.astype('uint16')

    result12xor = cv2.bitwise_xor(result1, result2)
    ret_xor, th_xor = cv2.threshold(result12xor, 0, 255, cv2.THRESH_OTSU)

    return th_xor