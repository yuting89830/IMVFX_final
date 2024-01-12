```
@inproceedings{chan2019dance,
 title={Everybody Dance Now},
 author={Chan, Caroline and Ginosar, Shiry and Zhou, Tinghui and Efros, Alexei A},
 booktitle={IEEE International Conference on Computer Vision (ICCV)},
 year={2019}
}
```
This code is from the paper "Everybody Dance Now" presented at ICCV 2019.

Model code adapted from [pix2pixHD](https://github.com/NVIDIA/pix2pixHD) and [pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix)

Data Preparation code adapted from [Realtime_Multi-Person_Pose_Estimation](https://github.com/ZheC/Realtime_Multi-Person_Pose_Estimation)

Data Preparation code based on outputs from [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)

### Execution Steps ###
1. You can build the enviroment with the requirements.txt or the environment.yaml provided.

2. Start by navigating to the `sample_data/train` folder and create a folder named `mul`.

3. Inside the `mul` folder, create two additional folders: `keypoints_json` and `original_frames`. Place the obtained keypoints from the Multi-Person Pose Estimation process and their original image into their respective folders.

4. Open the terminal and execute the following command:

```
cd .\EveryBodyDanceNow\data_prep
python graph_train.py --keypoints_dir ../sample_data/mul/keypoints_json --frames_dir ../sample_data/mul/original_frames --save_dir ./save_json --spread 0 x 1 --facetexts
```

Note: Replace 'x' with the quantity of frames minus 1 before executing.

5. Start training the model
## Global stage
Follow similar stage training as in pix2pixHD, first train a "global" stage model at 512x256 resolution
```
python train_fullts.py \
--name MY_MODEL_NAME_global \
--dataroot MY_TRAINING_DATASET_PATH \
--checkpoints_dir WHERE_TO_SAVE_CHECKPOINTS \
--loadSize 512 \
--no_instance \
--no_flip \
--tf_log \
--label_nc 6
```
## Local stage
Followed by a "local" stage model with 1024x512 resolution.
```
python train_fullts.py \
--name MY_MODEL_NAME_local \
--dataroot MY_TRAINING_DATASET_PATH \
--checkpoints_dir WHERE_TO_SAVE_CHECKPOINTS \
--load_pretrain MY_MODEL_NAME_global_PATH \
--netG local \
--ngf 32 \
--num_D 3 \
--resize_or_crop none \
--no_instance \
--no_flip \
--tf_log \
--label_nc 6
```

6. Testing on the model
## Global stage
test model at 512x256 resolution
```
python test_fullts.py \
--name MY_MODEL_NAME_global \
--dataroot MY_TESTING_DATASET_PATH \
--checkpoints_dir WHERE_TO_SAVE_CHECKPOINTS \
--results_dir WHERE_TO_SAVE_RESULTS \
--loadSize 512 \
--no_instance \
--how_many TOTAL_NUMBER_OF_TESTING_DATA \
--label_nc 6
```

## Local stage
test model at 1024x512 resolution
```
python test_fullts.py \
--name MY_MODEL_NAME_local \
--dataroot MY_TESTING_DATASET_PATH \
--checkpoints_dir WHERE_TO_SAVE_CHECKPOINTS \
--results_dir WHERE_TO_SAVE_RESULTS \
--netG local \
--ngf 32 \
--resize_or_crop none \
--no_instance \
--how_many TOTAL_NUMBER_OF_TESTING_DATA \
--label_nc 6
```

7. Use the code images_to_video.py to turn the results image into video. Modify the image_folder and video_name before executing the following command:
```
python images_to_video.py
```

