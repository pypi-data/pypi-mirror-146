"""
Neuraxle Test Case Class
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
import numpy as np

from neuraxle.base import ExecutionMode


class NeuraxleTestCase:
    def __init__(
            self,
            pipeline,
            callbacks,
            expected_callbacks_data,
            hyperparams_space=None,
            hyperparams=None,
            expected_processed_outputs=None,
            execution_mode=None,
            more_arguments=None,
            data_inputs=None,
            expected_outputs=None
    ):
        self.expected_outputs = expected_outputs
        self.data_inputs = data_inputs
        self.execution_mode = execution_mode
        self.pipeline = pipeline
        self.callbacks = callbacks
        self.expected_callbacks_data = expected_callbacks_data
        self.hyperparams = hyperparams
        self.hyperparams_space = hyperparams_space
        self.expected_processed_outputs = expected_processed_outputs
        self.more_arguments = more_arguments

    def assert_callback_data_is_as_expected(self):
        for callback, expected_callback_data in zip(self.callbacks, self.expected_callbacks_data):
            if len(callback.data) > 0:
                if isinstance(callback.data[0], tuple):
                    for (expected_di, expected_eo), (actual_di, actual_eo) in zip(expected_callback_data, callback.data):
                        assert np.array_equal(expected_di, actual_di)
                        assert np.array_equal(expected_eo, actual_eo)
                else:
                    assert np.array_equal(
                        np.array(callback.data),
                        expected_callback_data
                    )
            else:
                assert np.array_equal(
                    np.array([]),
                    np.array(expected_callback_data)
                )

    def assert_expected_processed_outputs(self, processed_outputs):
        if self.execution_mode != ExecutionMode.FIT:
            assert np.array_equal(processed_outputs, self.expected_processed_outputs)

    def execute(self):
        for c in self.callbacks:
            c.reset()

        processed_outputs = None
        if self.execution_mode == ExecutionMode.TRANSFORM:
            processed_outputs = self.pipeline.transform(self.data_inputs)
        if self.execution_mode == ExecutionMode.FIT_TRANSFORM:
            self.pipeline, processed_outputs = self.pipeline.fit_transform(self.data_inputs, self.expected_outputs)
        if self.execution_mode == ExecutionMode.FIT:
            self.pipeline = self.pipeline.fit(self.data_inputs, self.expected_outputs)

        return processed_outputs
