from products_app.app import price_check
#have to have __init__.py in the subfolder


def test_price_check():
    result = price_check("2")
    assert result == False
