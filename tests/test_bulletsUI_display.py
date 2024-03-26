import pytest
from Main import bulletsUI, SCREEN, FONT


@pytest.mark.parametrize("bulletsCount", [0, 1, 5, 10])
def test_bulletsUI(bulletsCount, monkeypatch):

    def mock_renderText(screen, font, text, size, color, position):
        mock_renderText.called = True
        mock_renderText.args = (screen, font, text, size, color, position)

    mock_renderText.called = False

    monkeypatch.setattr("Main.renderText", mock_renderText)

    bulletsUI(bulletsCount)

    expected_text = "R = " + str(bulletsCount)
    assert mock_renderText.called
    args = mock_renderText.args
    assert args[0:] == (SCREEN, FONT, expected_text, 25, "White", (135, 790))
