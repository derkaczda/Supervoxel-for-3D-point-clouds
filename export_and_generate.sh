#!/bin/bash

set -o pipefail -u

DATA_ROOT=~/work/exchange/danield/atlas_images_export_2
TRIAL=210811_animal_trial_01
PHASE=$1
RESOLUTION=$2

XYZ_DEST_PATH=$DATA_ROOT/$TRIAL/$PHASE/xyz_data
echo $PHASE
if [ ! -d "$XYZ_DEST_PATH" ]; then
	# convert to xyz data
	python3 convert_atlas_to_xyz.py \
		--dir $DATA_ROOT/$TRIAL \
		--phase $PHASE \
		--dest_path $XYZ_DEST_PATH
fi

#generate the supervoxel
SUPERPOINT_DEST_PATH=$DATA_ROOT/$TRIAL/$PHASE/superpoints_$RESOLUTION
CAMERA=cn01
python3 generate_supervoxel.py \
	--dir $XYZ_DEST_PATH/$CAMERA \
	--dest $SUPERPOINT_DEST_PATH/$CAMERA \
	--res $RESOLUTION
CAMERA=cn02
python3 generate_supervoxel.py \
	--dir $XYZ_DEST_PATH/$CAMERA \
	--dest $SUPERPOINT_DEST_PATH/$CAMERA \
	--res $RESOLUTION
CAMERA=cn03
python3 generate_supervoxel.py \
	--dir $XYZ_DEST_PATH/$CAMERA \
	--dest $SUPERPOINT_DEST_PATH/$CAMERA \
	--res $RESOLUTION
CAMERA=cn04
python3 generate_supervoxel.py \
	--dir $XYZ_DEST_PATH/$CAMERA \
	--dest $SUPERPOINT_DEST_PATH/$CAMERA \
	--res $RESOLUTION
