import numpy as np

from neuraxle.data_container import ZipDataContainer, DACT


def test_zip_data_container_should_merge_two_data_sources_together():
    data_inputs_3d, expected_outputs_3d = _create_data_source((10, 10, 2))
    data_inputs_2d, expected_outputs_2d = _create_data_source((10, 10))
    data_container_2d = DACT(data_inputs=data_inputs_2d, expected_outputs=expected_outputs_2d)
    data_container = DACT(data_inputs=data_inputs_3d, expected_outputs=expected_outputs_3d)

    zip_data_container = ZipDataContainer.create_from(data_container, data_container_2d)

    assert zip_data_container.ids == data_container.ids
    for i, di in enumerate(zip_data_container.data_inputs):
        assert np.array_equal(di[0], data_inputs_3d[i])
        assert np.array_equal(di[1], data_inputs_2d[i])


def test_zip_data_container_should_merge_1d_with_2d():
    data_inputs_3d, expected_outputs_3d = _create_data_source((10, 10, 2))
    data_inputs_1d, expected_outputs_1d = _create_data_source((10,))
    data_container_1d = DACT(data_inputs=data_inputs_1d, expected_outputs=expected_outputs_1d)
    data_container = DACT(data_inputs=data_inputs_3d, expected_outputs=expected_outputs_3d)

    zip_data_container = ZipDataContainer.create_from(data_container, data_container_1d)

    assert zip_data_container.ids == data_container.ids
    for i, di in enumerate(zip_data_container.data_inputs):
        assert np.array_equal(di[0], data_inputs_3d[i])
        assert np.array_equal(di[1], data_inputs_1d[i])


def test_zip_data_container_should_merge_multiple_data_sources_together():
    data_inputs_3d, expected_outputs_3d = _create_data_source((10, 10, 2))
    data_inputs_2d, expected_outputs_2d = _create_data_source((10, 10))
    data_inputs_1d, expected_outputs_1d = _create_data_source((10,))
    data_container_1d = DACT(data_inputs=data_inputs_1d, expected_outputs=expected_outputs_1d)
    data_container_2d = DACT(data_inputs=data_inputs_2d, expected_outputs=expected_outputs_2d)
    data_container = DACT(data_inputs=data_inputs_3d, expected_outputs=expected_outputs_3d)

    zip_data_container = ZipDataContainer.create_from(data_container, data_container_2d, data_container_1d)

    assert zip_data_container.ids == data_container.ids
    for i, di in enumerate(zip_data_container.data_inputs):
        assert np.array_equal(di[0], data_inputs_3d[i])
        assert np.array_equal(di[1], data_inputs_2d[i])


def test_zip_data_container_should_concatenate_inner_features():
    data_inputs_3d, expected_outputs_3d = _create_data_source((10, 10, 2))
    data_inputs_2d, expected_outputs_2d = _create_data_source((10, 10))
    data_container_2d = DACT(data_inputs=data_inputs_2d, expected_outputs=expected_outputs_2d)
    data_container = DACT(data_inputs=data_inputs_3d, expected_outputs=expected_outputs_3d)

    zip_data_container = ZipDataContainer.create_from(data_container, data_container_2d)
    zip_data_container.concatenate_inner_features()

    assert np.array_equal(np.array(zip_data_container.data_inputs)[..., -1], data_container_2d.data_inputs)
    assert np.array_equal(np.array(zip_data_container.expected_outputs), expected_outputs_3d)


def _create_data_source(shape):
    data_inputs = np.random.random(shape).astype(np.float32)
    expected_outputs = np.random.random(shape).astype(np.float32)
    return data_inputs, expected_outputs
