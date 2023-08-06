import numpy as np

from neuraxle.data_container import DACT, ListDataContainer


def test_data_container_iter_method_should_iterate_with_none_ids():
    data_container = DACT(
        di=np.array(list(range(100))),
        eo=np.array(list(range(100, 200)))
    ).set_ids(None)

    for i, (_id, data_input, expected_outputs) in enumerate(data_container):
        assert _id == i
        assert data_input == i
        assert expected_outputs == i + 100


def test_data_container_iter_method_should_iterate_with_none_expected_outputs():
    data_container = DACT(
        ids=[str(i) for i in range(100)],
        data_inputs=np.array(list(range(100))),
        expected_outputs=None
    )

    for i, (_, data_input, expected_outputs) in enumerate(data_container):
        assert data_input == i
        assert expected_outputs is None


def test_data_container_len_method_should_return_data_inputs_len():
    data_container = DACT.from_di(np.array(list(range(100))))

    assert len(data_container) == 100


def test_data_container_should_iterate_through_data_using_minibatches():
    data_container = DACT(
        ids=[str(i) for i in range(100)],
        data_inputs=np.array(list(range(100))),
        expected_outputs=np.array(list(range(100, 200)))
    )

    batches = []
    for b in data_container.minibatches(batch_size=10):
        batches.append(b)

    for i, batch in enumerate(batches):
        assert np.array_equal(np.array(batch.data_inputs), np.array(list(range(i * 10, (i * 10) + 10))))
        assert np.array_equal(
            np.array(batch.expected_outputs),
            np.array(list(range((i * 10) + 100, (i * 10) + 100 + 10)))
        )


def test_list_data_container_concat():
    # Given
    data_container = ListDataContainer(
        ids=[str(i) for i in range(100)],
        data_inputs=np.array(list(range(100))),
        expected_outputs=np.array(list(range(100, 200)))
    )

    # When
    data_container.concat(DACT(
        ids=[str(i) for i in range(100, 200)],
        data_inputs=np.array(list(range(100, 200))),
        expected_outputs=np.array(list(range(200, 300)))
    ))

    # Then
    assert np.array_equal(np.array(data_container.ids), np.array(list(range(0, 200))).astype(np.str))

    expected_data_inputs = np.array(list(range(0, 200))).astype(np.int)
    actual_data_inputs = np.array(data_container.data_inputs).astype(np.int)
    assert np.array_equal(actual_data_inputs, expected_data_inputs)

    expected_expected_outputs = np.array(list(range(100, 300))).astype(np.int)
    assert np.array_equal(np.array(data_container.expected_outputs).astype(np.int), expected_expected_outputs)
