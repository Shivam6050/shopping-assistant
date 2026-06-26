from app.agent import DISCOUNT_CODES, redeem_discount_code, root_agent

# 1. Unit/Security boundaries tests for the tool logic directly


def test_tool_redeem_discount_success():
    """Verify that a registered user can successfully redeem a valid discount code."""
    # Reset store
    DISCOUNT_CODES["WELCOME50"]["redeemed_by"] = None

    result = redeem_discount_code("WELCOME50", "user123")
    assert "Success" in result
    assert DISCOUNT_CODES["WELCOME50"]["redeemed_by"] == "user123"


def test_tool_redeem_discount_single_use():
    """Verify that a code cannot be redeemed more than once."""
    # Reset and redeem once
    DISCOUNT_CODES["WELCOME50"]["redeemed_by"] = "user123"

    # Try to redeem again
    result = redeem_discount_code("WELCOME50", "user456")
    assert "Error" in result
    assert "already been redeemed" in result
    # Identity remains the first redeemer
    assert DISCOUNT_CODES["WELCOME50"]["redeemed_by"] == "user123"


def test_tool_redeem_discount_invalid_user():
    """Verify that unregistered user IDs are blocked from redeeming codes."""
    DISCOUNT_CODES["WELCOME50"]["redeemed_by"] = None

    result = redeem_discount_code("WELCOME50", "malicious_unregistered_user")
    assert "Error" in result
    assert "not a registered user" in result
    assert DISCOUNT_CODES["WELCOME50"]["redeemed_by"] is None


def test_tool_redeem_discount_invalid_code():
    """Verify that invalid discount codes are rejected."""
    result = redeem_discount_code("FAKECODE99", "user123")
    assert "Error" in result
    assert "invalid" in result


def test_tool_redeem_discount_case_insensitivity():
    """Verify that codes are normalized (e.g., upper-cased) and stripped of whitespace."""
    DISCOUNT_CODES["SUMMER20"]["redeemed_by"] = None

    result = redeem_discount_code("  summer20  ", "user123")
    assert "Success" in result
    assert DISCOUNT_CODES["SUMMER20"]["redeemed_by"] == "user123"


# 2. Agent structural/config security assertions


def test_agent_has_discount_tool():
    """Ensure that the root_agent has the discount redemption tool registered."""
    assert redeem_discount_code in root_agent.tools


def test_agent_instruction_contains_security_directives():
    """Ensure the agent's instructions contain security directives for user verification."""
    instruction = root_agent.instruction.lower()
    assert "registered user id" in instruction
    assert "redeem" in instruction
    assert "ask" in instruction
