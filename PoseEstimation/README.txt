```
@article{8765346,
  author = {Z. {Cao} and G. {Hidalgo Martinez} and T. {Simon} and S. {Wei} and Y. A. {Sheikh}},
  journal = {IEEE Transactions on Pattern Analysis and Machine Intelligence},
  title = {OpenPose: Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields},
  year = {2019}
}

@inproceedings{simon2017hand,
  author = {Tomas Simon and Hanbyul Joo and Iain Matthews and Yaser Sheikh},
  booktitle = {CVPR},
  title = {Hand Keypoint Detection in Single Images using Multiview Bootstrapping},
  year = {2017}
}

@inproceedings{cao2017realtime,
  author = {Zhe Cao and Tomas Simon and Shih-En Wei and Yaser Sheikh},
  booktitle = {CVPR},
  title = {Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields},
  year = {2017}
}

@inproceedings{wei2016cpm,
  author = {Shih-En Wei and Varun Ramakrishna and Takeo Kanade and Yaser Sheikh},
  booktitle = {CVPR},
  title = {Convolutional pose machines},
  year = {2016}
}
```
This code is from the paper "OpenPose: Real-time Multi-Person 2D Pose Estimation using Part Affinity Fields" presented at CVPR 2017.

### Execution Steps ###
1.Place the original image or video into this folder: .\PoseEstimation\examples\media

2.Then, use the following command to run the code for multi-person pose estimation.

```
cd .\PoseEstimation
bin\OpenPoseDemo.exe --video examples\media\"VideoName.mp4" --hand --write_json "output_json_folder/" --write_images output_"image_folder/" --net_resolution 320x176 --render_pose 0
```
It will generate two folders, one for keypoint's JSON and another for the original image corresponding to that frame.
Note: Please change the video (or image) name and folder name if necessary.

4.After the program is executed, you can proceed to ../label_modify for the next step.