There are README.txt in every model's folders , please check and follow the instructions to executing the program.
hope you enjoy it ! :)

1.PoseEstimation

```
cd .\PoseEstimation
bin\OpenPoseDemo.exe --video examples\media\"VideoName.mp4" --hand --write_json "output_json_folder/" --write_images output_"image_folder/" --net_resolution 320x176 --render_pose 0
```

2.EveryBodyDanceNow

```
cd .\EveryBodyDanceNow\data_prep
python graph_train.py --keypoints_dir ../sample_data/mul/keypoints_json --frames_dir ../sample_data/mul/original_frames --save_dir ./save_json --spread 0 x 1 --facetexts
```

3.Train global
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

4.Train local
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

5.Test final model
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

6.Produce video with the generated results. Modify the image_folder and video_name in the code before executing the following command:
```
python images_to_video.py
```
