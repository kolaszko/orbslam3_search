import hydra
from hydra.utils import get_original_cwd
from omegaconf import DictConfig
import os

from command_utils import *
from config_utils import *



@hydra.main(config_name="config")
def main(cfg: DictConfig) -> None:
    print(cfg.orb.nFeatures)
    print(cfg.orb.scaleFactor)
    print(cfg.orb.nLevels)

    print(cfg.image.scale)

    print(cfg.stereo.ThDepth)
    print(cfg.bag.path)

    print(os.getcwd())

    create_config(os.path.join(get_original_cwd(), 'orbslam_configs/madmax.yaml'), os.path.join(os.getcwd(), 'orb_config.yaml'), cfg.image.scale,
                  cfg.orb.nFeatures, cfg.orb.scaleFactor, cfg.orb.nLevels, cfg.stereo.ThDepth)
    run_experiment(config_file=os.path.join(os.getcwd(), 'orb_config.yaml'), bag_path=cfg.bag.path, delay=5)


if __name__ == "__main__":
    main()