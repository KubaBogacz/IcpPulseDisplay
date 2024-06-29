import os
from pathlib import Path
from typing import List

import gc
import yaml
import torch

import numpy as np
import scipy.interpolate as sp_int

from backend.classification_model.ResnetModel import ResNet


class PulseClassifier:
    """
    Helper class that performs pulse classification using a residual neural network.
    """

    def __init__(self) -> None:
        """
        Initializes a Classifier instance and loads the ResNet neural network model.
        """
        self._load_parameters()
        curr_path = Path(os.path.dirname(__file__))
        self.model_weights = self.params["classification"]["model_weights"]
        self.model_weights = curr_path / self.model_weights
        self.batch_size = self.params["classification"]["batch_size"]
        self.gpu = self.params["classification"]["gpu"]

        self.device = torch.device('cuda:' + str(0) if torch.cuda.is_available() and self.gpu else 'cpu')
        self.model = ResNet(5).to(self.device)
        self.model.load_state_dict(torch.load(self.model_weights, map_location=self.device)["state_dict"])
        self.model.eval()

        self.resampling = True
        self.resampling_samples = 180
        self.normalization = True

    def _load_parameters(self) -> None:
        """
        Loads the parameters of the ResNet model from file.
        """
        params_path = Path(os.path.dirname(__file__)) / 'params.yaml'
        with open(params_path, 'r') as stream:
            try:
                self.params = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def classify_batch(self, input_pulses: List[np.ndarray]) -> List[int]:
        """
        Classifies the pulses using the ResNet model.

        This function takes a list of pulses as input and performs the classification using the ResNet neural
        network model (using CUDA if available, otherwise CPU). The classification approach is described in detail in:
        C. Mataczynski, A. Kazimierska, A. Uryga, M. Burzy´nska, A. Rusiecki, and M. Kasprowicz, “End-to-end
        automatic morphological classification of intracranial pressure pulse waveforms using deep learning,”
        IEEE Journal of Biomedical and Health Informatics, vol. 26, no. 2, pp. 494–504, 2022.

        Args:
            input_pulses (List[numpy array]): List of one-dimensional vectors corresponding to individual pulses.

        Returns:
            List[int]: List of predicted classes for individual pulses.
        """

        predictions = []
        pulses = []
        for idp in range(0, len(input_pulses)):
            data = self.preprocess(input_pulses[idp])
            pulses.append(data)
            if len(pulses) % self.batch_size == self.batch_size - 1:
                tensors = torch.tensor(pulses, dtype=torch.float).to(self.device)
                tensors = tensors.unsqueeze(1)
                outputs = self.model(tensors).detach().cpu().tolist()

                del tensors
                torch.cuda.empty_cache()
                gc.collect()

                predictions += outputs
                pulses = []

        if len(pulses) > 0:
            tensors = torch.tensor(pulses, dtype=torch.float).to(self.device)
            tensors = tensors.unsqueeze(1)
            outputs = self.model(tensors).detach().cpu().tolist()

            del tensors
            torch.cuda.empty_cache()
            gc.collect()

            predictions += outputs

        classes = [np.argmax(prediction) + 1 for prediction in predictions]

        return classes

    def preprocess(self, pulse: np.ndarray) -> np.ndarray:
        """
        Performs the preprocessing of a single pulse for classification.

        This function takes an individual pulse as input and performs the preprocessing operations:
        cubic interpolation (resampling to 180 samples) and normalization to 0-1 range.

        Args:
            pulse (numpy array): The one-dimensional pulse vector.

        Returns:
            numpy array: The one-dimensional pulse vector after preprocessing.
        """
        data = pulse
        if self.resampling:
            interp = sp_int.interp1d(np.arange(0, len(data), 1), data, kind="cubic")
            new_t = np.linspace(0, len(data)-1, self.resampling_samples)
            data = interp(new_t)
        if self.normalization:
            data = data - np.min(data)
            if np.max(data) != 0:
                data = data / np.max(data)
        return data


