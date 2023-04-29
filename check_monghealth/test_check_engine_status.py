import pylint

def test_check_engine_status():
    # Test that the check_engine_status function returns True if the engine is alive.
    engine_url = "https://www.google.com"
    assert check_engine_status(engine_url) is True

    # Test that the check_engine_status function returns False if the engine is not alive.
    engine_url = "https://www.google.com.invalid"
    assert check_engine_status(engine_url) is False


def test_main():
    # Test that the main function prints the correct output if the engine is alive.
    engine_url = "https://www.google.com"
    expected_output = "OK - {}".format(json.dumps({"alive": True}))
    assert main(engine_url) == expected_output

    # Test that the main function prints the correct output if the engine is not alive.
    engine_url = "https://www.google.com.invalid"
    expected_output = "CRITICAL - Engine is not alive!"
    assert main(engine_url) == expected_output


if __name__ == "__main__":
    pylint.test()
