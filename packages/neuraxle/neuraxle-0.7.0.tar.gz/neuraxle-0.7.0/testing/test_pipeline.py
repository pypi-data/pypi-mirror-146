"""
Tests for Pipelines
========================================

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

from typing import Generic
import numpy as np
import pytest

from neuraxle.base import (_FittableStep, _HasChildrenMixin, BaseStep, BaseTransformer,
                           CX, NonTransformableMixin)
from neuraxle.hyperparams.distributions import RandInt, LogUniform
from neuraxle.hyperparams.space import HyperparameterSpace
from neuraxle.pipeline import Pipeline
from neuraxle.steps.misc import TransformCallbackStep, TapeCallbackFunction
from neuraxle.steps.numpy import NumpyTranspose
from neuraxle.union import Identity, AddFeatures, ModelStacking
from testing.mocks.step_mocks import SomeStep, AN_INPUT, AN_EXPECTED_OUTPUT

steps_lists = [
    [("just_one_step", SomeStep())],
    [
        ("some_step_1", SomeStep()),
        ("some_step_2", SomeStep()),
        ("some_step_3", SomeStep())
    ]
]


@pytest.mark.parametrize("steps_list", steps_lists)
def test_pipeline_fit_transform(steps_list):
    data_input_ = [AN_INPUT]
    expected_output_ = [AN_EXPECTED_OUTPUT]
    p = Pipeline(steps_list)

    p, result = p.fit_transform(data_input_, expected_output_)

    assert tuple(result) == tuple(expected_output_)


@pytest.mark.parametrize("steps_list", steps_lists)
def test_pipeline_fit_then_transform(steps_list):
    data_input_ = [AN_INPUT]
    expected_output_ = [AN_EXPECTED_OUTPUT]
    p = Pipeline(steps_list)

    p = p.fit(data_input_, expected_output_)
    result = p.transform(data_input_)

    assert tuple(result) == tuple(expected_output_)


def test_pipeline_slicing_before():
    p = Pipeline([
        ("a", SomeStep()),
        ("b", SomeStep()),
        ("c", SomeStep())
    ])

    r = p["b":]

    assert "a" not in r
    assert "b" in r
    assert "c" in r


def test_pipeline_slicing_after():
    p = Pipeline([
        ("a", SomeStep()),
        ("b", SomeStep()),
        ("c", SomeStep())
    ])

    r = p[:"c"]

    assert "a" in r
    assert "b" in r
    assert "c" not in r


def test_pipeline_slicing_both():
    p = Pipeline([
        ("a", SomeStep()),
        ("b", SomeStep()),
        ("c", SomeStep())
    ])

    r = p["b":"c"]

    assert "a" not in r
    assert "b" in r
    assert "c" not in r


def test_pipeline_set_one_hyperparam_level_one_flat():
    p = Pipeline([
        ("a", SomeStep()),
        ("b", SomeStep()),
        ("c", SomeStep())
    ])

    p.set_hyperparams({
        "a__learning_rate": 7
    })

    assert p["a"].hyperparams.to_flat_dict()["learning_rate"] == 7
    assert p["b"].hyperparams.to_flat_dict() == dict()
    assert p["c"].hyperparams.to_flat_dict() == dict()


def test_pipeline_set_one_hyperparam_level_one_dict():
    p = Pipeline([
        ("a", SomeStep()),
        ("b", SomeStep()),
        ("c", SomeStep())
    ])

    p.set_hyperparams({
        "b": {
            "learning_rate": 7
        }
    })

    assert p["a"].hyperparams == dict()
    assert p["b"].hyperparams["learning_rate"] == 7
    assert p["c"].hyperparams == dict()


def test_pipeline_set_one_hyperparam_level_two_flat():
    p = Pipeline([
        ("a", SomeStep()),
        ("b", Pipeline([
            ("a", SomeStep()),
            ("b", SomeStep()),
            ("c", SomeStep())
        ])),
        ("c", SomeStep())
    ])

    p.set_hyperparams({
        "b__a__learning_rate": 7
    })
    print(p.get_hyperparams())

    assert p["b"]["a"].hyperparams["learning_rate"] == 7
    assert p["b"]["c"].hyperparams.to_flat_dict() == dict()
    assert p["b"].hyperparams.to_flat_dict() == {'a__learning_rate': 7}
    assert p["c"].hyperparams.to_flat_dict() == dict()


def test_pipeline_set_one_hyperparam_level_two_dict():
    p = Pipeline([
        ("a", SomeStep()),
        ("b", Pipeline([
            ("a", SomeStep()),
            ("b", SomeStep()),
            ("c", SomeStep())
        ])),
        ("c", SomeStep())
    ])

    p.set_hyperparams({
        "b": {
            "a": {
                "learning_rate": 7
            },
            "learning_rate": 9
        }
    })
    print(p.get_hyperparams())

    assert p["b"]["a"].get_hyperparams()["learning_rate"] == 7
    assert p["b"]["c"].get_hyperparams() == dict()
    assert p["b"].get_hyperparams()["learning_rate"] == 9
    assert p["c"].get_hyperparams() == dict()


def test_pipeline_update_hyperparam_level_one_flat():
    p = Pipeline([
        ("a", SomeStep()),
        ("b", SomeStep()),
        ("c", SomeStep())
    ])
    p.set_hyperparams({
        "a__learning_rate": 7,
        "a__other_hp": 8
    })

    p.update_hyperparams({
        "a__learning_rate": 0.01
    })

    assert p["a"].hyperparams["learning_rate"] == 0.01
    assert p["a"].hyperparams["other_hp"] == 8
    assert p["b"].hyperparams == dict()
    assert p["c"].hyperparams == dict()


def test_pipeline_update_hyperparam_level_one_dict():
    p = Pipeline([
        ("a", SomeStep()),
        ("b", SomeStep()),
        ("c", SomeStep())
    ])
    p.set_hyperparams({"b": {"learning_rate": 7, "other_hp": 8}})

    p.update_hyperparams({"b": {"learning_rate": 0.01}})

    assert p["b"].hyperparams["learning_rate"] == 0.01
    assert p["b"].hyperparams["other_hp"] == 8
    assert p["a"].hyperparams == dict()
    assert p["c"].hyperparams == dict()


def test_pipeline_update_hyperparam_level_two_flat():
    p = Pipeline([
        ("a", SomeStep()),
        ("b", Pipeline([
            ("a", SomeStep()),
            ("b", SomeStep()),
            ("c", SomeStep())
        ])),
        ("c", SomeStep())
    ])
    p.set_hyperparams({
        "b__a__learning_rate": 7,
        "b__a__other_hp": 8,
    })

    p.update_hyperparams({
        "b__a__learning_rate": 0.01
    })

    assert p["b"]["a"].hyperparams["learning_rate"] == 0.01
    assert p["b"]["a"].hyperparams["other_hp"] == 8
    assert p["b"]["c"].hyperparams == dict()
    assert p["b"].hyperparams.to_flat_dict() == {
        'a__learning_rate': 0.01,
        'a__other_hp': 8
    }
    assert p["c"].hyperparams == dict()


def test_pipeline_update_hyperparam_level_two_dict():
    p = Pipeline([
        ("a", SomeStep()),
        ("b", Pipeline([
            ("a", SomeStep()),
            ("b", SomeStep()),
            ("c", SomeStep())
        ])),
        ("c", SomeStep())
    ])
    p.set_hyperparams({"b": {"a": {"learning_rate": 7, "other_hp": 8}, "learning_rate": 9}})

    p.update_hyperparams({"b": {"a": {"learning_rate": 0.01}}})

    assert p["b"]["a"].hyperparams["learning_rate"] == 0.01
    assert p["b"]["a"].hyperparams["other_hp"] == 8
    assert p["b"]["c"].hyperparams == dict()
    assert p["b"].hyperparams["learning_rate"] == 9
    assert p["c"].hyperparams == dict()


def test_pipeline_simple_inverse_transform():
    expected_tape = ["1", "2", "3", "4", "4", "3", "2", "1"]
    tape = TapeCallbackFunction()

    p = Pipeline([
        Identity(),
        TransformCallbackStep(tape.callback, ["1"]),
        TransformCallbackStep(tape.callback, ["2"]),
        TransformCallbackStep(tape.callback, ["3"]),
        TransformCallbackStep(tape.callback, ["4"]),
        Identity()
    ])

    p, _ = p.fit_transform(np.ones((1, 1)))
    p.inverse_transform(np.ones((1, 1)))

    assert expected_tape == tape.get_name_tape()


def test_pipeline_nested_inverse_transform():
    expected_tape = ["1", "2", "3", "4", "5", "6", "7", "7", "6", "5", "4", "3", "2", "1"]
    tape = TapeCallbackFunction()

    p = Pipeline([
        Identity(),
        TransformCallbackStep(tape.callback, ["1"]),
        TransformCallbackStep(tape.callback, ["2"]),
        Pipeline([
            Identity(),
            TransformCallbackStep(tape.callback, ["3"]),
            TransformCallbackStep(tape.callback, ["4"]),
            TransformCallbackStep(tape.callback, ["5"]),
            Identity()
        ]),
        TransformCallbackStep(tape.callback, ["6"]),
        TransformCallbackStep(tape.callback, ["7"]),
        Identity()
    ])

    p, _ = p.fit_transform(np.ones((1, 1)))  # will add range(1, 8) to tape.

    p.inverse_transform(np.ones((1, 1)))  # will add reversed(range(1, 8)) to tape.

    print(expected_tape)
    print(tape.get_name_tape())
    assert expected_tape == tape.get_name_tape()


def test_pipeline_nested_inverse_transform_without_identities():
    """
    This test was required for a strange bug at the border of the pipelines
    that happened when the identities were not used.
    """
    expected_tape = ["1", "2", "3", "4", "5", "6", "7", "7", "6", "5", "4", "3", "2", "1"]
    tape = TapeCallbackFunction()

    p = Pipeline([
        TransformCallbackStep(tape.callback, ["1"]),
        TransformCallbackStep(tape.callback, ["2"]),
        Pipeline([
            TransformCallbackStep(tape.callback, ["3"]),
            TransformCallbackStep(tape.callback, ["4"]),
            TransformCallbackStep(tape.callback, ["5"]),
        ]),
        TransformCallbackStep(tape.callback, ["6"]),
        TransformCallbackStep(tape.callback, ["7"]),
    ])

    p, _ = p.fit_transform(np.ones((1, 1)))  # will add range(1, 8) to tape.

    p.inverse_transform(np.ones((1, 1)))  # will add reversed(range(1, 8)) to tape, calling inverse_transforms.

    print(expected_tape)
    print(tape.get_name_tape())
    assert expected_tape == tape.get_name_tape()


def test_hyperparam_space():
    p = Pipeline([
        AddFeatures([
            SomeStep(hyperparams_space=HyperparameterSpace({"n_components": RandInt(1, 5)})),
            SomeStep(hyperparams_space=HyperparameterSpace({"n_components": RandInt(1, 5)}))
        ]),
        ModelStacking([
            SomeStep(hyperparams_space=HyperparameterSpace({"n_estimators": RandInt(1, 1000)})),
            SomeStep(hyperparams_space=HyperparameterSpace({"n_estimators": RandInt(1, 1000)})),
            SomeStep(hyperparams_space=HyperparameterSpace({"max_depth": RandInt(1, 100)})),
            SomeStep(hyperparams_space=HyperparameterSpace({"max_depth": RandInt(1, 100)}))
        ],
            joiner=NumpyTranspose(),
            judge=SomeStep(hyperparams_space=HyperparameterSpace({"alpha": LogUniform(0.1, 10.0)}))
        )
    ])

    rvsed = p.get_hyperparams_space()
    p.set_hyperparams(rvsed)

    hyperparams = p.get_hyperparams()
    flat_hyperparams_keys = hyperparams.to_flat_dict().keys()

    assert 'AddFeatures' in hyperparams
    assert 'SomeStep' in hyperparams["AddFeatures"]
    assert "n_components" in hyperparams["AddFeatures"]["SomeStep"]
    assert 'SomeStep1' in hyperparams["AddFeatures"]
    assert "n_components" in hyperparams["AddFeatures"]["SomeStep1"]

    assert 'ModelStacking' in hyperparams
    assert 'SomeStep' in hyperparams["ModelStacking"]
    assert 'n_estimators' in hyperparams["ModelStacking"]["SomeStep"]
    assert 'SomeStep1' in hyperparams["ModelStacking"]
    assert 'n_estimators' in hyperparams["ModelStacking"]["SomeStep1"]
    assert 'SomeStep2' in hyperparams["ModelStacking"]
    assert 'max_depth' in hyperparams["ModelStacking"]["SomeStep2"]
    assert 'SomeStep3' in hyperparams["ModelStacking"]
    assert 'max_depth' in hyperparams["ModelStacking"]["SomeStep3"]

    assert 'AddFeatures__SomeStep1__n_components' in flat_hyperparams_keys
    assert 'AddFeatures__SomeStep__n_components' in flat_hyperparams_keys
    assert 'ModelStacking__SomeStep__n_estimators' in flat_hyperparams_keys
    assert 'ModelStacking__SomeStep1__n_estimators' in flat_hyperparams_keys
    assert 'ModelStacking__SomeStep2__max_depth' in flat_hyperparams_keys
    assert 'ModelStacking__SomeStep3__max_depth' in flat_hyperparams_keys


def test_pipeline_setup_incrementally():
    class SomeStepThatFits(NonTransformableMixin, BaseStep):
        def __init__(self):
            BaseStep.__init__(self)
            self.has_fitted = False

        def fit(self, data_inputs, expected_outputs=None) -> _FittableStep:
            self.has_fitted = True
            return self

    class StepWithSensitiveSetup(Identity):
        """ Asserts that step given in argument has fitted before performing setup"""

        def __init__(self):
            Identity.__init__(self)

        def setup(self, context: CX = None) -> BaseTransformer:
            assert some_step.has_fitted is True
            assert some_step2.has_fitted is False
            return self

    some_step = SomeStepThatFits()
    some_step2 = SomeStepThatFits()

    p = Pipeline([some_step,
                  StepWithSensitiveSetup(),
                  some_step2])

    p.fit_transform(None, None)


def test_subtyping_of_pipeline_works_correctly():
    p: Pipeline[Identity] = Pipeline([Identity(), Identity()])

    assert issubclass(Pipeline, Generic)
    assert isinstance(p, _HasChildrenMixin)
    assert isinstance(p[-1], Identity)
