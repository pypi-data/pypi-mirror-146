"""
Tests for Hyperparameters Distribution Spaces
=============================================

..
    Copyright 2019, Neuraxio Inc.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
import copy
import pytest
from collections import OrderedDict
import scipy

from neuraxle.hyperparams.distributions import *
from neuraxle.hyperparams.scipy_distributions import *
from neuraxle.hyperparams.space import HyperparameterSpace, HyperparameterSamples, RecursiveDict

hyperparams_flat_and_dict_pairs = [
    # Pair 1:
    ({
         "a__learning_rate": 7
     },
     {
         "a": {
             "learning_rate": 7
         }
     }),
    # Pair 2:
    ({
         "b__a__learning_rate": 7,
         "b__learning_rate": 9
     },
     {
         "b": {
             "a": {
                 "learning_rate": 7
             },
             "learning_rate": 9
         }
     }),
]


@pytest.mark.parametrize("class_to_test", [RecursiveDict, HyperparameterSamples])
@pytest.mark.parametrize("flat,expected_dic", hyperparams_flat_and_dict_pairs)
def test_flat_to_dict_hyperparams(flat: dict, expected_dic: dict, class_to_test):
    from_flat_dic = class_to_test(flat)
    from_nested_dic = class_to_test(expected_dic)

    assert from_flat_dic == from_nested_dic
    assert from_flat_dic.to_flat_dict() == flat
    assert from_nested_dic.to_flat_dict() == flat
    assert from_nested_dic.to_nested_dict() == expected_dic
    assert from_flat_dic.to_nested_dict() == expected_dic


HYPE_SPACE = HyperparameterSpace(OrderedDict({
    "a__test": Boolean(),
    "a__lr": Choice([0, 1, False, "Test"]),
    "a__b__c": PriorityChoice([0, 1, False, "Test"]),
    "a__b__q": Quantized(Uniform(-10, 10)),
    "d__param": RandInt(-10, 10),
    "d__u": Uniform(-10, 10),
    "e__other": LogUniform(0.001, 10),
    "e__alpha": Normal(0.0, 1.0),
    "e__f__g": LogNormal(0.0, 2.0),
    "p__could_also_be_as_fixed": FixedHyperparameter("also hey"),
    "scipy__poisson": Poisson(1.0, 2.0),
    "scipy__gaussian": Gaussian(-1, 1),
    "scipy__scipy__gaussian": scipy.stats.randint(0, 10)
}))


def test_hyperparams_space_rvs_outputs_samples():
    space = copy.deepcopy(HYPE_SPACE)

    samples = space.rvs()

    assert isinstance(samples, HyperparameterSamples)
    assert len(samples) == len(space)
    for k, v in samples.iter_flat():
        assert k in space
        assert not isinstance(v, HyperparameterDistribution)


@pytest.mark.parametrize("hd", list(HYPE_SPACE.to_flat_dict().values()))
def test_hyperparams_space_rvs_outputs_in_range(hd: HyperparameterDistribution):
    for _ in range(20):

        sample = hd.rvs()

        assert sample in hd
