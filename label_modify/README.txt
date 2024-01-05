```
@inproceedings{chan2019dance,
 title={Everybody Dance Now},
 author={Chan, Caroline and Ginosar, Shiry and Zhou, Tinghui and Efros, Alexei A},
 booktitle={IEEE International Conference on Computer Vision (ICCV)},
 year={2019}
}
```

This code is from the paper "Everybody Dance Now" presented at ICCV 2019.

### Execution Steps ###
1. Start by navigating to the `sample_data/train` folder and create a folder named `mul`.

2. Inside the `mul` folder, create two additional folders: `keypoints_json` and `original_frames`. Place the obtained keypoints from the Multi-Person Pose Estimation process and images with keypoints into their respective folders.

3. Open the terminal and execute the following command:

```
cd .\label_modify\data_prep
python graph_train.py --keypoints_dir ../sample_data/mul/keypoints_json --frames_dir ../sample_data/mul/original_frames --save_dir ./save_json --spread 0 x 1 --facetexts
```

Note: Replace 'x' with the quantity of frames minus 1 before executing.
