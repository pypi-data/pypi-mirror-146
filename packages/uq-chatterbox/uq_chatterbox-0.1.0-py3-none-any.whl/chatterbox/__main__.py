#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import secrets

from pathlib import Path

import click
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer


def filter_input_sentence(sentence):
    sentence = "".join(filter(lambda character: character.isalpha() or character in "., ", sentence))
    return sentence.strip().strip(".")

def filter_input(input):
    return ". ".join(filter(None, map(filter_input_sentence, input))) + "."

@click.group()
def cli():
    pass

@cli.command()
@click.option('--model', default='tts_models/en/ljspeech/glow-tts')
def download(model: str):
    path = Path(__file__).parent / ".models.json"
    manager = ModelManager(path)

    _, _, model_item = manager.download_model(model)
    manager.download_model(model_item["default_vocoder"])


@cli.command()
@click.option('--model', default='tts_models/en/ljspeech/glow-tts')
@click.option('--input-file', required=True)
@click.option('--output-path', default="out")
@click.option('--run-id', default=secrets.token_hex(8))
def run(model: str, input_file: str, output_path: str, run_id: str):
    status = {}

    output = os.path.abspath(output_path)

    # Prep the output folder since we might need to output errors
    if not os.path.exists(output):
        os.makedirs(output)

    destination = os.path.join(output, run_id)
    wav_destination = destination + '.wav'
    report_destination = destination + '.json'

    try:
        run_model(model, input_file, wav_destination)
    except Exception as err:
        status['error'] = {
            'tldr': 'Unable to process the request',
            'message': f'{err}'
        }

    if 'error' not in status:
        status['result'] = {
            'wav': wav_destination
        }

    with open(report_destination, 'w') as report:
        json.dump(status, report, indent=4, sort_keys=True)


def run_model(model: str, input_file: str, output: str):
    # load model manager
    path = Path(__file__).parent / ".models.json"
    manager = ModelManager(path)

    model_path, config_path, model_item = manager.download_model(model)
    vocoder_path, vocoder_config_path, _ = manager.download_model(model_item["default_vocoder"])

    # load models
    synthesizer = Synthesizer(
        tts_checkpoint=model_path,
        tts_config_path=config_path,
        vocoder_checkpoint=vocoder_path,
        vocoder_config=vocoder_config_path
    )

    with open(input_file) as f:
        contents = filter_input(f.readlines())

    print(" > Text: {}".format(contents))
    wav = synthesizer.tts(contents)

    output_path = output if output.endswith(".wav") else output + ".wav"
    print(" > Saving output to {}".format(output_path))
    synthesizer.save_wav(wav, output_path)


if __name__ == "__main__":
    cli()
