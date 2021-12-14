from libdrm.common import iter_in_batches


def test_iter_in_batches(valid_raw_input):
    """Test if input data is split into the expected number of baches.
    Each of which with the expected number of elements."""
    fake_batches = iter_in_batches([valid_raw_input]*32, batch_size=7)
    for index, batch in enumerate(fake_batches, start=1):
        if index < 5:
            assert len(batch) == 7
        else:
            # ensure batches smaller than the batch_size are returned
            assert len(batch) == 4
    assert index == 5
