# -*- coding: utf-8 -*-
import os

from honeybee_radiance_folder import ModelFolder as Folder
from honeybee_radiance_folder.folderutil import _nukedir


def test_scene_mapping():
    folder_path = r'./tests/assets/model_folders/simple/model'
    model_folder = Folder.from_model_folder(folder_path)

    # two phase
    scene_mapping = model_folder.octree_scene_mapping(exclude_static=False, phase=2)
    os.remove(r'./tests/assets/model_folders/simple/scene_mapping.json')
    assert 'two_phase' in scene_mapping
    assert 'three_phase' not in scene_mapping
    assert 'five_phase' not in scene_mapping
    assert len(scene_mapping['two_phase']) == 11

    # three phase
    scene_mapping = model_folder.octree_scene_mapping(exclude_static=False, phase=3)
    os.remove(r'./tests/assets/model_folders/simple/scene_mapping.json')
    assert 'two_phase' in scene_mapping
    assert 'three_phase' in scene_mapping
    assert 'five_phase' not in scene_mapping
    assert len(scene_mapping['two_phase']) == 3

    # five phase
    scene_mapping = model_folder.octree_scene_mapping(exclude_static=False, phase=5)
    os.remove(r'./tests/assets/model_folders/simple/scene_mapping.json')
    assert 'two_phase' in scene_mapping
    assert 'three_phase' in scene_mapping
    assert 'five_phase' in scene_mapping
    assert len(scene_mapping['two_phase']) == 3
    assert len(scene_mapping['five_phase']) == 8

def test_scene_mapping_static_model():
    folder_path = r'./tests/assets/model_folders/static/model'
    model_folder = Folder.from_model_folder(folder_path)

    # exclude static apertures
    scene_mapping = model_folder.octree_scene_mapping(exclude_static=False, phase=5)
    os.remove(r'./tests/assets/model_folders/static/scene_mapping.json')
    assert len(scene_mapping['two_phase']) == 1
    assert len(scene_mapping['three_phase']) == 0
    assert len(scene_mapping['five_phase']) == 0

    # do not exclude static apertures
    scene_mapping = model_folder.octree_scene_mapping(exclude_static=True, phase=5)
    os.remove(r'./tests/assets/model_folders/static/scene_mapping.json')
    assert len(scene_mapping['two_phase']) == 0
    assert len(scene_mapping['three_phase']) == 0
    assert len(scene_mapping['five_phase']) == 0
