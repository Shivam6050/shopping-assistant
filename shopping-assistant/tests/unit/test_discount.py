from app.agent import DISCOUNT_CODES, redeem_discount_code


def test_redeem_discount_success() -> None:
    # Reset store
    DISCOUNT_CODES["WELCOME50"]["redeemed_by"] = None

    result = redeem_discount_code("WELCOME50", "user123")
    assert "Success" in result
    assert DISCOUNT_CODES["WELCOME50"]["redeemed_by"] == "user123"


def test_redeem_discount_already_redeemed() -> None:
    # Set store state
    DISCOUNT_CODES["WELCOME50"]["redeemed_by"] = "user123"

    result = redeem_discount_code("WELCOME50", "user456")
    assert "Error" in result
    assert "already been redeemed" in result


def test_redeem_discount_invalid_user() -> None:
    # Reset store
    DISCOUNT_CODES["WELCOME50"]["redeemed_by"] = None

    result = redeem_discount_code("WELCOME50", "unregistered_user")
    assert "Error" in result
    assert "not a registered user" in result


def test_redeem_discount_invalid_code() -> None:
    result = redeem_discount_code("NOT_A_CODE", "user123")
    assert "Error" in result
    assert "invalid" in result
