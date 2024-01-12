# python graph_mul_train.py --keypoints_dir ../sample_data/mul/keypoints_json  --frames_dir ../sample_data/mul/original_frames --save_dir ./save_json --spread 0 2 1 --facetexts
import cv2 as cv 
import numpy as np
from PIL import Image
from renderopenpose import *
import os
import argparse


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

##### Must specifcy these parameters
parser.add_argument('--keypoints_dir', type=str, default='keypoints', help='directory where target keypoint files are stored, assumes .yml format for now.')
parser.add_argument('--frames_dir', type=str, default='frames', help='directory where source frames are stored. Assumes .png files for now.')
parser.add_argument('--save_dir', type=str, default='save', help='directory where to save generated files')
parser.add_argument('--spread', nargs='+', type=int, help='range of frames to use for target video plus step size [start end step] e.g. 0 10000 1')

#### Optional (have defaults)
parser.add_argument('--facetexts', action='store_true', help='use this flag to also save face 128x128 bounding boxes')
parser.add_argument('--boxbuffer', type=int, default=70, help='face bounding box width/height')
parser.add_argument('--num_face_keypoints', type=int, default=8, help='number of face keypoints to plot. Acceptable values are 8, 9, 22, 70. \
	If another value is specified, the default number of points will be plotted.')
parser.add_argument('--output_dim', type=int, default=512, help='default width of output images. Output images will have size output_dim, 2*output_dim')
parser.add_argument('--map_25_to_23', action='store_true', help='load body keypoints in 25 OpenPose format, but graph in 23 keypoint OpenPose format')
parser.add_argument('--debug', action='store_true', help='use this flag for debugging')

opt = parser.parse_args()

myshape = (1080, 1920, 3)
disp = False

spread = tuple(opt.spread)
start = spread[0]
end = spread[1]
step = spread[2]
SIZE = opt.output_dim #512
numkeypoints = opt.num_face_keypoints
get_factexts = opt.facetexts #True
boxbuffer = opt.boxbuffer #70

numframesmade = 0
n = start

print (step)

startx = 0
endx = myshape[1]
starty = 0
endy = myshape[0]

tary = SIZE
tarx = 2*SIZE

scaley = float(tary) / float(endy - starty)
scalex = float(tarx) / float(endx - startx)

poselen = [23, 54, 69, 75]

keypoints_dir = opt.keypoints_dir #"/data/scratch/caroline/keypoints/jason_keys"
frames_dir = opt.frames_dir #"/data/scratch/caroline/frames/jason_frames"
savedir = opt.save_dir #"/data/scratch/caroline/omegalul"

if not os.path.exists(savedir):
	os.makedirs(savedir)
if not os.path.exists(savedir + '/train_label'):
	os.makedirs(savedir + '/train_label')
if not os.path.exists(savedir + '/train_img'):
	os.makedirs(savedir + '/train_img')
if not os.path.exists(savedir + '/train_facetexts128'):
	os.makedirs(savedir + '/train_facetexts128')

if opt.debug and (not os.path.exists(savedir + '/debug')):
	os.makedirs(savedir + '/debug')


print('----------------- Loading Frames -----------------')
frames = sorted(os.listdir(frames_dir))
print (frames)
print('----------------- All Loaded -----------------')

while n <= end:
	print (n)
	framesmadestr = '%06d' % numframesmade

	filebase_name = os.path.splitext(frames[n])[0]
	print('keypoints_dir: ', keypoints_dir)
	print('filebase name: ', filebase_name)

	key_name = os.path.join(keypoints_dir, filebase_name)
	print('key name: ', key_name)
	frame_name = os.path.join(frames_dir, frames[n])

	posepts = []

	json_file_name = key_name.split("_rendered")[0]

	print('json_file_name: ', json_file_name)
	posepts, r_handpts, l_handpts = readkeypointsfile(json_file_name + "_keypoints")
	if posepts is None:
		print('unable to read keypoints file')
		import sys
		sys.exit(0)

	if not (len(posepts[0]) in poselen):
		# empty or contains multiple detections
		print ("empty", len(posepts))
		n += 1
		continue
	else:
		print ('graphing file %s' % filebase_name)
		if opt.map_25_to_23:
			posepts = map_25_to_23(posepts)

		oriImg = cv.imread(frame_name)
		curshape = oriImg.shape

		### scale and resize:
		sr = scale_resize(curshape, myshape=(1080, 1920, 3), mean_height=0.0)
		if sr:
			scale = sr[0]
			translate = sr[1]

			oriImg = fix_scale_image(oriImg, scale, translate, myshape)
			posepts1 = fix_scale_coords(posepts[0], scale, translate)
			posepts2 = fix_scale_coords(posepts[1], scale, translate)

			# facepts = fix_scale_coords(facepts, scale, translate)
			r_handpts1 = fix_scale_coords(r_handpts[0], scale, translate)
			l_handpts1 = fix_scale_coords(l_handpts[0], scale, translate)
			r_handpts2 = fix_scale_coords(r_handpts[1], scale, translate)
			l_handpts2 = fix_scale_coords(l_handpts[1], scale, translate)

		pose_len = len(posepts)
		print('pose_len: ', pose_len)
		canvas = None
		for i in range(pose_len):
			if i == 0:
				canvas = renderpose(posepts[0], 255 * np.ones(myshape, dtype='uint8'))
			else:
				canvas = renderpose(posepts[i], canvas)
		
		r_handpts_len = len(r_handpts)
		print('r_handpts_len: ', r_handpts_len)
		for i in range(r_handpts_len):
			canvas = renderhand(r_handpts[i], canvas)

		l_handpts_len = len(l_handpts)
		print('l_handpts_len: ', l_handpts_len)
		for i in range(l_handpts_len):
			canvas = renderhand(l_handpts[i], canvas)

		
		# canvas = renderface_sparse(facepts, canvas, numkeypoints, disp=False)


		oriImg = Image.fromarray(oriImg[:, :, [2,1,0]])
		canvas = Image.fromarray(canvas[:, :, [2,1,0]])

		oriImg = oriImg.resize((2*SIZE,SIZE), Image.Resampling.LANCZOS)
		canvas = canvas.resize((2*SIZE,SIZE), Image.Resampling.LANCZOS)

		oriImg.save(savedir + '/train_img/' + filebase_name + '.png')
		canvas.save(savedir + '/train_label/' + filebase_name + '.png')

		numframesmade += 1
	n += step
