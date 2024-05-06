import numpy as np

DATA_PATH="MP_Data"
existing_label_map = {'merhaba':1,'tamam':2,'seni seviyorum':3}
new_actions_with_labels = {}
# Number of videos to collect
no_sequences = 30
# Videos are going to be 30 frames in length
sequence_length = 30
actions = np.array(list(existing_label_map.keys()))

epoch_count = 10000
keras_model_name = 'sign_language.keras'