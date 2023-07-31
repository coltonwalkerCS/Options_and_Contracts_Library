import pandas as pd
from PyOptionClasses.OptionsClass import option_data
from PyOptionClasses.SpreadsClass import Straddle


# Desc: Find Straddle Spreads for a given option data set including calls and puts
# Input Options data (option_data class format)
# Output: A list of straddle spreads (straddle class format)
def getStraddleSpreads(ops_data):
    call_ops = ops_data.options_calls
    put_ops = ops_data.options_puts

    # Assert length and values before generating straddles
    assert(len(call_ops) == len(put_ops))
    assert(call_ops[0].strike_price == put_ops[0].strike_price)

    straddles = []

    for i in range(0, len(call_ops)):
        # Get both sides long & short
        new_call_op_long = call_ops[i].create_option_trade('Bought')
        new_put_op_long = put_ops[i].create_option_trade('Bought')
        new_straddle_long = Straddle(call_ops[i].strike_price, new_call_op_long, new_put_op_long,
                                     ops_data.expiration_date)
        straddles.append(new_straddle_long)

        new_call_op_short = call_ops[i].create_option_trade('Sold')
        new_put_op_short = put_ops[i].create_option_trade('Sold')
        new_straddle_short = Straddle(call_ops[i].strike_price, new_call_op_short, new_put_op_short,
                                      ops_data.expiration_date)
        straddles.append(new_straddle_short)

    return straddles
