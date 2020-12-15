import os
import sys
import cv2
import matplotlib.pyplot as plt
import numpy as np
from __init__ import PYTHON_PATH
from ailibs.detector.dnn.FaceDetector import FaceDetector

dnn_path = os.path.join(PYTHON_PATH, "ailibs_data/detector/dnn")

proto_path = os.path.join(dnn_path, "deploy.prototxt")
model_path = os.path.join(dnn_path,"res10_300x300_ssd_iter_140000.caffemodel")

LOG=True
DETECTOR = FaceDetector(detector_proto=proto_path,detector_model=model_path,log=LOG)

def hsv_histogram_for_window(frame, window):
    # set up the ROI for tracking
    # ROI = Region of interest
    c,r,w,h = window  #c,r,w,h == x,y,w,h #similar to x,y coordinate of a rectangle upper left corner and its width and height
    roi = frame[r:r+h, c:c+w]
    hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
    roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
    cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
    return roi_hist

def resample(weights):
    n = len(weights)
    indices = []
    C = [0.] + [sum(weights[:i+1]) for i in range(n)]
    u0, j = np.random.random(), 0
    for u in [(u0+i)/n for i in range(n)]:
      while u > C[j]:
          j+=1
      indices.append(j-1)
    return indices

# a function that, given a particle position, will return the particle's "fitness"
def particleevaluator(back_proj, particle):
    return back_proj[particle[1],particle[0]]

def particle_tracker(v):    
    # detect face in first frame
    c=0
    r=0
    w=0
    h=0
    while c==0 and r==0 and w==0 and h==0:
        ret ,frame = v.read()
        if ret == False:
            return
        dets = DETECTOR.detect(frame)
        for det in dets:
            [l, t, r, b] = DETECTOR.get_position(det)
            c = l
            r = t
            w = l-r
            h = b-t
        print(c,r,w,h)


    n_particles = 200
    init_pos = np.array([c + w/2.0,r + h/2.0], int) # Initial position

    # Create an array with 200 enteries and each entery is init_pos i.e. [[92 67], [92 67], [92 67]....]
    particles = np.ones((n_particles, 2), int) * init_pos # Init particles to init position

    roi_hist = hsv_histogram_for_window(frame, (c,r,w,h))
    # Create an array with 200 enteries and each entery is 1/200 i.e. [...]
    weights = np.ones(n_particles) / n_particles   # weights are uniform (at first)

    stepsize = 8    # pick a value that performs well.
    while(1):
        ret ,frame = v.read() # read another frame
        if ret == False:
            break
        # perform the tracking
        # Particle motion model: uniform step (TODO: find a better motion model)
        # For particles, each value of particle, add random number from -step to + step
        np.add(particles, np.random.uniform(-stepsize, stepsize, particles.shape), out=particles, casting="unsafe")

        # Clip out-of-bounds particles
        # Clip the particles which goes out of the frame. Set value either 0 of size of frame
        particles = particles.clip(np.zeros(2), np.array((frame.shape[1], frame.shape[0]))-1).astype(int)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # hist_bp = [[0 0 0 ..., 5 7 7]
        # [5 5 5 ..., 6 5 5]
        # [5 5 5 ..., 5 5 5].....]
        hist_bp = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

        # particles.T  [[ 80  95  96...][71  59  66  ...]]
        # f  [206 255 122 116...]
        f = particleevaluator(hist_bp, particles.T) # Evaluate particles
        # f.clip(1) -> Replace all 0 with 1 and weights is basically the values returned by particleevaluator -> float value
        weights = np.float32(f.clip(1))
        weights /= np.sum(weights)                  # Normalize w -> divide weight value by total sum
        # Multiply each value of particle.T with corresponding weight value and add both arrays separately (2 arrays in particles.T). sum is the weighted mean which is the new pos
        pos = np.sum(particles.T * weights, axis=1).astype(int) # expected position: weighted average
        # write the result to the output file

        if 1. / np.sum(weights**2) < n_particles / 2.: # If particle cloud degenerate:
            particles = particles[resample(weights),:]  # Resample particles according to weights

        # Display particles
        for sv in particles:
            cv2.circle(frame,(int(sv[0]),int(sv[1])),3,(100,0,255))
        cv2.circle(frame,(int(pos[0]),int(pos[1])),3,(100,0,255))
        cv2.imshow("frame", frame)                         # Plot the image
        print("Particles: ", particles)
        k = cv2.waitKey(60) & 0xff
        if k == 27:
            break
        
if __name__ == '__main__':
    camera = cv2.VideoCapture(0)

    particle_tracker(camera)