KEYS = {
    'width' : 'Camera.newWidth',
    'height' : 'Camera.newHeight',
    'n_features' : 'ORBextractor.nFeatures',
    'scale_factor' : 'ORBextractor.scaleFactor',
    'n_levels' : 'ORBextractor.nLevels'  
}

def create_config(base_config_path, config_save_path, image_scale, n_features, scale_factor, n_levels):
    with open(base_config_path, 'r') as f:
        lines = f.readlines()
        get_idx = lambda key : [i for i, l in enumerate(lines) if key in l][0]
        get_val = lambda key, type : type(lines[get_idx(key)].split()[1])

        indices = {}
        for k, v in KEYS.items():
            indices[k] = get_idx(v)
        
        lines[indices['width']] = f"{KEYS['width']}: {int(image_scale * get_val('Camera.width', int))}\n"
        lines[indices['height']] = f"{KEYS['height']}: {int(image_scale * get_val('Camera.height', int))}\n"
        lines[indices['n_features']] = f"{KEYS['n_features']}: {n_features}\n"
        lines[indices['scale_factor']] = f"{KEYS['scale_factor']}: {scale_factor}\n"
        lines[indices['n_levels']] = f"{KEYS['n_levels']}: {n_levels}\n"
    
    with open(config_save_path, 'w') as f:
        f.writelines(lines)
            

if __name__ == '__main__':
    create_config('orbslam_configs/madmax.yaml', 'tmp.yaml', 0.5, 0, 0, 0)