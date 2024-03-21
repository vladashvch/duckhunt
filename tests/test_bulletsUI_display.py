import pytest
from Main import bulletsUI, SCREEN, FONT
from unittest.mock import patch


@pytest.mark.parametrize(
    "bulletsCount", [0, 1, 5, 10])
def test_bulletsUI_display(bulletsCount):
    with patch("Main.renderText") as mocked_renderText:

        bulletsUI(bulletsCount)
        expected_text = "R = " + str(bulletsCount)

        mocked_renderText.assert_called_once()
        args, _ = mocked_renderText.call_args

        assert args[0:] == (SCREEN, FONT, expected_text,
                            25, "White", (135, 790))
