from typing import Optional, List, Tuple
from pathlib import Path

from numpy import ndarray, exp, savetxt, loadtxt, argmax, array, flatnonzero, zeros
from numpy.linalg import pinv
from numpy.random import uniform, seed

from windML.utils.label_encoding import one_hot_encode_batch

class ELMClassifier:
    """
    Extreme Learning Machine
    """
    def __init__(self, input_dimension:int, hidden_dimension:int=1000, load_path:Optional[str]=None) -> None:
        seed(0)
        self.random_projection = uniform(
            low=-.1, high=.1, 
            size =(input_dimension, hidden_dimension)
        )
        if load_path is None:
            self.LABELS = list()
            self.weights = None
        else:
            self.LABELS = loadtxt(f"{load_path}/LABELS.txt",dtype=str)
            positive_indexes = loadtxt(f"{load_path}/positive_weight_indexes.txt",dtype=int)
            negative_indexes = loadtxt(f"{load_path}/negative_weight_indexes.txt",dtype=int)
            self.weights = self._reconstruct_weights(positive_indexes,negative_indexes,(hidden_dimension,len(self.LABELS)))

    def fit(self, inputs: List[ndarray], labels: List[int]) -> None:
        self.LABELS = sorted(set(labels))
        label_vectors = one_hot_encode_batch(labels,self.LABELS)
        hidden = self._hidden_layer(inputs)
        self.weights = self._learn_weights(hidden, label_vectors)
    
    def save(self, name:str) -> str:
        path = f"{Path.cwd()}/{name}"
        Path(path).mkdir(parents=True, exist_ok=True)
        savetxt(f"{path}/LABELS.txt",self.LABELS,fmt="%s")
        positive_indexes, negative_indexes = self._deconstruct_weights(self.weights)
        savetxt(f"{path}/positive_weight_indexes.txt",positive_indexes,fmt="%d")
        savetxt(f"{path}/negative_weight_indexes.txt",negative_indexes,fmt="%d")

    def predict(self, inputs: ndarray) -> ndarray:
        return self._output_layer(self._hidden_layer(inputs))
    
    def classify(self, inputs: ndarray) -> str:
        class_id = argmax(self.predict(inputs))
        return self.LABELS[class_id]

    def _hidden_layer(self, inputs: ndarray) -> ndarray: 
        return self.activation_function(inputs @ self.random_projection)
  
    def _output_layer(self, hidden: ndarray) -> ndarray: 
        return hidden @ self.weights
    
    @staticmethod
    def _learn_weights(hidden:ndarray, label_vectors:List[ndarray]) -> ndarray:
        return pinv(hidden) @ label_vectors

    @staticmethod
    def _deconstruct_weights(weights:ndarray, binary_threshold:float=0.0) -> Tuple[ndarray,ndarray]:
        positive_weights = array(weights > binary_threshold,dtype=int)
        negative_weights = array(weights < binary_threshold,dtype=int)
        return flatnonzero(positive_weights), flatnonzero(negative_weights)
    
    @staticmethod
    def _reconstruct_weights(positive_indexes:List[int],negative_indexes:List[int],shape:Tuple[int,int]) -> ndarray:
        positive_weights = ELMClassifier._convert_indexes_to_weights(positive_indexes,shape)
        negative_weights = ELMClassifier._convert_indexes_to_weights(negative_indexes,shape)
        return positive_weights - negative_weights

    @staticmethod
    def _convert_indexes_to_weights(indexes:List[int],shape:Tuple[int,int]) -> ndarray:
        weights = zeros(shape[0]*shape[1],dtype=int)
        weights[indexes] = 1
        return weights.reshape(shape)

    @staticmethod
    def activation_function(x: ndarray) -> ndarray: 
        return ELMClassifier.sigmoid(x)
    
    @staticmethod
    def sigmoid(x: ndarray) -> ndarray:
        return 1. / (1. + exp(-x))