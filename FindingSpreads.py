from PyOptionClasses.OptionsClass import option_data
from PyOptionClasses.SpreadsClass import Straddle, Strangle, Butterfly, Condor, IronCondor


# Desc: Find Straddle Spreads for a given option data set including calls and puts
# Input Options data (option_data class format)
# Output: A list of straddle spreads (straddle class format)
def getStraddleSpreads(ops_data):
    call_ops = ops_data.options_calls
    put_ops = ops_data.options_puts

    # Assert length and values before generating straddles
    assert (len(call_ops) == len(put_ops))
    assert (call_ops[0].strike_price == put_ops[0].strike_price)

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


def getStrangleSpreads(ops_data, strangle_range):

    call_ops = ops_data.options_calls
    put_ops = ops_data.options_puts

    # Assert length and values before generating straddles
    assert (len(call_ops) == len(put_ops))
    assert (call_ops[0].strike_price == put_ops[0].strike_price)

    # Assert the range is more than the dollar gap and make sure it can have the spread based on the dollar range
    # i.e. a spread of $3 is not possible when the $ range is $2: 2, 4, 6, 8 cannot have a $3 spread
    assert (strangle_range >= ops_data.data_spread)
    assert (strangle_range % ops_data.data_spread == 0)
    assert (strangle_range < ops_data.data_spread * len(ops_data.options_calls))

    strangles = []
    strike_dollar_gap = ops_data.data_spread

    # Get the number of possible strangles
    # Iterate through and generate strangles
    # To get num of strangles:
    # length of options - range / strike dollar gap
    option_data_gap = int(strangle_range / strike_dollar_gap)
    num_iter = int(len(call_ops) - option_data_gap)

    for i in range(0, num_iter):
        # Get long side
        # Get both calls and puts

        # Long strangle (put/call) bought

        new_put_op_long = put_ops[i].create_option_trade('Bought')
        new_long_op_long = call_ops[i + option_data_gap].create_option_trade('Bought')
        new_strangle_long = Strangle(strangle_range, new_put_op_long, new_long_op_long,
                                     ops_data.expiration_date)

        strangles.append(new_strangle_long)

        # Short strangle (put/call) sold

        new_put_op_short = put_ops[i].create_option_trade('Sold')
        new_long_op_short = call_ops[i + option_data_gap].create_option_trade('Sold')
        new_strangle_short = Strangle(strangle_range, new_put_op_short, new_long_op_short,
                                      ops_data.expiration_date)

        strangles.append(new_strangle_short)

    return strangles


def getButterflySpreads(ops_data, butterfly_range):
    call_ops = ops_data.options_calls
    put_ops = ops_data.options_puts

    # Assert the range is more than the dollar gap and make sure it can have the spread based on the dollar range
    # i.e. a spread of $3 is not possible when the $ range is $2: 2, 4, 6, 8 cannot have a $3 spread
    assert (butterfly_range >= ops_data.data_spread)
    assert (butterfly_range % ops_data.data_spread == 0)
    assert (butterfly_range * 2 < ops_data.data_spread * len(ops_data.options_calls))

    butterflies = []
    strike_dollar_gap = ops_data.data_spread

    # Get the number of possible butterflies
    # Iterate through and generate call and then put butterflies
    # To get num of butterflies:
    # length of options - 2 * range / strike dollar gap
    option_data_gap = int((2 * butterfly_range) / strike_dollar_gap)
    num_iter = int(len(call_ops) - option_data_gap)
    # Test for butterfly
    option_data_gap = int(option_data_gap / 2)

    for i in range(0, num_iter):
        # Get long side
        # Get both calls & puts

        # Butterfly long - Calls
        new_call_op_1_long = call_ops[i].create_option_trade('Bought')
        new_call_op_2_1_short = call_ops[i + option_data_gap].create_option_trade('Sold')
        new_call_op_2_2_short = call_ops[i + option_data_gap].create_option_trade('Sold')
        new_call_op_3_long = call_ops[i + (option_data_gap * 2)].create_option_trade('Bought')

        new_butterfly_long_calls = Butterfly(butterfly_range, new_call_op_1_long, new_call_op_2_1_short,
                                             new_call_op_2_2_short, new_call_op_3_long, ops_data.expiration_date)

        butterflies.append(new_butterfly_long_calls)

        # Butterfly long - Puts
        new_put_op_1_long = put_ops[i].create_option_trade('Bought')
        new_put_op_2_1_short = put_ops[i + option_data_gap].create_option_trade('Sold')
        new_put_op_2_2_short = put_ops[i + option_data_gap].create_option_trade('Sold')
        new_put_op_2_long = put_ops[i + (option_data_gap * 2)].create_option_trade('Bought')

        new_butterfly_long_puts = Butterfly(butterfly_range, new_put_op_1_long, new_put_op_2_1_short,
                                            new_put_op_2_2_short, new_put_op_2_long, ops_data.expiration_date)

        butterflies.append(new_butterfly_long_puts)

        # Butterfly short - Calls
        new_call_op_1_short = call_ops[i].create_option_trade('Sold')
        new_call_op_2_1_long = call_ops[i + option_data_gap].create_option_trade('Bought')
        new_call_op_2_2_long = call_ops[i + option_data_gap].create_option_trade('Bought')
        new_call_op_3_short = call_ops[i + (option_data_gap * 2)].create_option_trade('Sold')

        new_butterfly_short_calls = Butterfly(butterfly_range, new_call_op_1_short, new_call_op_2_1_long,
                                              new_call_op_2_2_long, new_call_op_3_short, ops_data.expiration_date)

        butterflies.append(new_butterfly_short_calls)

        # Butterfly short - Puts
        new_put_op_1_short = put_ops[i].create_option_trade('Sold')
        new_put_op_2_1_long = put_ops[i + option_data_gap].create_option_trade('Bought')
        new_put_op_2_2_long = put_ops[i + option_data_gap].create_option_trade('Bought')
        new_put_op_2_short = put_ops[i + (option_data_gap * 2)].create_option_trade('Sold')

        new_butterfly_short_puts = Butterfly(butterfly_range, new_put_op_1_short, new_put_op_2_1_long,
                                             new_put_op_2_2_long, new_put_op_2_short, ops_data.expiration_date)

        butterflies.append(new_butterfly_short_puts)

    return butterflies


def getCondorSpreads(ops_data, inner_range, outer_range):
    call_ops = ops_data.options_calls
    put_ops = ops_data.options_puts

    total_range = inner_range + (2 * outer_range)

    # Assert the range is more than the dollar gap and make sure it can have the spread based on the dollar range
    # i.e. a spread of $3 is not possible when the $ range is $2: 2, 4, 6, 8 cannot have a $3 spread
    assert (total_range >= ops_data.data_spread)
    assert (total_range % ops_data.data_spread == 0)
    assert (inner_range % ops_data.data_spread == 0)
    assert (outer_range % ops_data.data_spread == 0)
    assert (total_range < ops_data.data_spread * len(ops_data.options_calls))

    condors = []
    strike_dollar_gap = ops_data.data_spread

    # Get the number of possible condors
    # Iterate through and generate condors
    # To get num of condors:
    # length of options - (total_range / strike dollar gap)
    option_data_gap = int(total_range / strike_dollar_gap)
    num_iter = int(len(call_ops) - option_data_gap)

    option_2_gap = int(outer_range / strike_dollar_gap)
    option_3_gap = int((outer_range + inner_range) / strike_dollar_gap)
    option_4_gap = int(((2 * outer_range) + inner_range) / strike_dollar_gap)

    for i in range(0, num_iter):
        # Get long side
        # Get both calls & puts

        # Condor long - Calls
        new_call_op_1_long = call_ops[i].create_option_trade('Bought')
        new_call_op_2_short = call_ops[i + option_2_gap].create_option_trade('Sold')
        new_call_op_3_short = call_ops[i + option_3_gap].create_option_trade('Sold')
        new_call_op_4_long = call_ops[i + option_4_gap].create_option_trade('Bought')

        new_condor_long_calls = Condor(outer_range, inner_range, new_call_op_1_long, new_call_op_2_short,
                                       new_call_op_3_short, new_call_op_4_long, ops_data.expiration_date)

        condors.append(new_condor_long_calls)

        # Condor long - Puts
        new_put_op_1_long = put_ops[i].create_option_trade('Bought')
        new_put_op_2_short = put_ops[i + option_2_gap].create_option_trade('Sold')
        new_put_op_3_short = put_ops[i + option_3_gap].create_option_trade('Sold')
        new_put_op_4_long = put_ops[i + option_4_gap].create_option_trade('Bought')

        new_condor_long_puts = Condor(outer_range, inner_range, new_put_op_1_long, new_put_op_2_short,
                                      new_put_op_3_short, new_put_op_4_long, ops_data.expiration_date)

        condors.append(new_condor_long_puts)

        # Condor short - Calls
        new_call_op_1_short = call_ops[i].create_option_trade('Sold')
        new_call_op_2_long = call_ops[i + option_2_gap].create_option_trade('Bought')
        new_call_op_3_long = call_ops[i + option_3_gap].create_option_trade('Bought')
        new_call_op_4_short = call_ops[i + option_4_gap].create_option_trade('Sold')

        new_condor_short_calls = Condor(outer_range, inner_range, new_call_op_1_short, new_call_op_2_long,
                                        new_call_op_3_long, new_call_op_4_short, ops_data.expiration_date)

        condors.append(new_condor_short_calls)

        # Condor short - Puts
        new_put_op_1_short = put_ops[i].create_option_trade('Sold')
        new_put_op_2_long = put_ops[i + option_2_gap].create_option_trade('Bought')
        new_put_op_3_long = put_ops[i + option_3_gap].create_option_trade('Bought')
        new_put_op_4_short = put_ops[i + option_4_gap].create_option_trade('Sold')

        new_condor_short_puts = Condor(outer_range, inner_range, new_put_op_1_short, new_put_op_2_long,
                                       new_put_op_3_long, new_put_op_4_short, ops_data.expiration_date)

        condors.append(new_condor_short_puts)

    return condors


def getIronCondorSpreads(ops_data, inner_range, outer_range):
    call_ops = ops_data.options_calls
    put_ops = ops_data.options_puts

    total_range = inner_range + (2 * outer_range)

    # Assert the range is more than the dollar gap and make sure it can have the spread based on the dollar range
    # i.e. a spread of $3 is not possible when the $ range is $2: 2, 4, 6, 8 cannot have a $3 spread
    assert (total_range >= ops_data.data_spread)
    assert (total_range % ops_data.data_spread == 0)
    assert (inner_range % ops_data.data_spread == 0)
    assert (outer_range % ops_data.data_spread == 0)
    assert (total_range < ops_data.data_spread * len(ops_data.options_calls))

    iron_condors = []
    strike_dollar_gap = ops_data.data_spread

    # Get the number of possible condors
    # Iterate through and generate condors
    # To get num of condors:
    # length of options - (total_range / strike dollar gap)
    option_data_gap = int(total_range / strike_dollar_gap)
    num_iter = int(len(call_ops) - option_data_gap)

    option_2_gap = int(outer_range / strike_dollar_gap)
    option_3_gap = int((outer_range + inner_range) / strike_dollar_gap)
    option_4_gap = int(((2 * outer_range) + inner_range) / strike_dollar_gap)

    for i in range(0, num_iter):
        # Get long side
        # Get both calls & puts

        # Iron Condor long
        new_put_op_1_short = put_ops[i].create_option_trade('Sold')
        new_put_op_2_long = put_ops[i + option_2_gap].create_option_trade('Bought')
        new_call_op_3_long = call_ops[i + option_3_gap].create_option_trade('Bought')
        new_call_op_4_short = call_ops[i + option_4_gap].create_option_trade('Sold')

        new_iron_condor_long = IronCondor(outer_range, inner_range, new_put_op_1_short, new_put_op_2_long,
                                          new_call_op_3_long, new_call_op_4_short, ops_data.expiration_date)

        iron_condors.append(new_iron_condor_long)

        # Iron Condor short
        new_put_op_1_long = put_ops[i].create_option_trade('Bought')
        new_put_op_2_short = put_ops[i + option_2_gap].create_option_trade('Sold')
        new_call_op_3_short = call_ops[i + option_3_gap].create_option_trade('Sold')
        new_call_op_4_long = call_ops[i + option_4_gap].create_option_trade('Bought')

        new_iron_condor_short = IronCondor(outer_range, inner_range, new_put_op_1_long, new_put_op_2_short,
                                           new_call_op_3_short, new_call_op_4_long, ops_data.expiration_date)

        iron_condors.append(new_iron_condor_short)

    return iron_condors
