#!/usr/bin/env python3

import argparse
import yaml
import glob
import os

from concurrent.futures import ProcessPoolExecutor

from yaml import FullLoader

from VAD_algorithms.ecovad.make_data import preprocess_file, save_processed_arrays
from VAD_algorithms.ecovad.train_model import trainingApp


def process_file(file, cfg):
    processed_arr, sr = preprocess_file(file,
                                        cfg["LENGTH_SEGMENTS"],
                                        overlap=0,
                                        min_length=cfg["LENGTH_SEGMENTS"],
                                        speech_dir=cfg["SPEECH_DIR"],
                                        noise_dir=cfg["NOISE_DIR"],
                                        proba_speech=cfg["PROBA_SPEECH"],
                                        proba_noise_speech=cfg["PROBA_NOISE_WHEN_SPEECH"],
                                        proba_noise_nospeech=cfg["PROBA_NOISE_WHEN_NO_SPEECH"])
    save_processed_arrays(file, os.path.normpath(cfg["AUDIO_OUT_DIR"]), processed_arr, sr)
    return(len(processed_arr))



if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--config",
                        help='Path to the config file',
                        default="./config_training.yaml",
                        required=False,
                        type=str,
                        )

    cli_args = parser.parse_args()

    # Open the config file
    with open(cli_args.config) as f:
        cfg = yaml.load(f, Loader=FullLoader)
    
    # Run below only if config of "TRAIN_ONLY" is set to False
    if not cfg["TRAIN_ONLY"]:
        num_workers = cfg["NUM_WORKERS"]

        # Prepare the synthetic dataset
        # list_audio_files = glob.glob(cfg["AUDIO_PATH"] + "/*")
        list_audio_files = []
        for dirpath, dirnames, filenames in os.walk(os.path.normpath(cfg["AUDIO_PATH"])):
            for file in filenames:
                if file.endswith(('.wav', '.mp3', '.flac')):
                    list_audio_files.append(os.path.join(dirpath, file))
        print("Found {} files to split into training segments".format(len(list_audio_files)))
        print("Generating the synthetic dataset...")

        synth_dat_len = 0
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            results = executor.map(process_file, list_audio_files, [cfg]*len(list_audio_files))
            for result in results:
                synth_dat_len += result

        if(synth_dat_len == 0):
            raise ValueError("No training segments were generated. Please check your config file.")
        print(f"Created {synth_dat_len} training segments in {cfg['AUDIO_OUT_DIR']}")

    # Train the model
    if cfg["TRAIN"]:
        print("Training the model...")
        trainingApp(cfg["TRAIN_VAL_PATH"],
                cfg["MODEL_SAVE_PATH"],
                cfg["CKPT_SAVE_PATH"],
                cfg["BATCH_SIZE"],
                cfg["NUM_EPOCH"],
                cfg["TB_PREFIX"],
                cfg["TB_COMMENT"],
                cfg["LR"],
                cfg["MOMENTUM"],
                cfg["DECAY"],
                cfg["NUM_WORKERS"],
                cfg["USE_GPU"]
                ).main()