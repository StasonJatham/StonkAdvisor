def approximate_cost(
    in_text, out_text, in_token_price=0.00163, out_token_price=0.00551
):
    # price is per 1000 token
    # the padding is the chars i use for the actuall command
    in_tokens = (len(in_text) + 500) / 4
    out_tokens = len(out_text) / 4

    in_cost = (in_tokens / 1000) * in_token_price
    out_cost = (out_tokens / 1000) * out_token_price

    return {"in": in_cost, "out": out_cost, "total": in_cost + out_cost}
