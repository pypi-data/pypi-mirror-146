
import json
from spikeinterface import load_extractor
from spikeinterface.sorters import run_sorter_local

# load recorsding in docker
recording = load_extractor('/home/samuel/Documents/SpikeInterface/spikeinterface/spikeinterface/sorters/tests/in_container_recording.json')

# load params in docker
with open('/home/samuel/Documents/SpikeInterface/spikeinterface/spikeinterface/sorters/tests/in_container_params.json', encoding='utf8', mode='r') as f:
    sorter_params = json.load(f)

# run in docker
output_folder = '/home/samuel/Documents/SpikeInterface/spikeinterface/spikeinterface/sorters/tests/tridesclous_output'
run_sorter_local('tridesclous', recording, output_folder=output_folder,
            remove_existing_folder=True, delete_output_folder=False,
            verbose=False, raise_error=True, **sorter_params)
