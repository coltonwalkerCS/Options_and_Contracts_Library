from OptionsClass import option


# Spread
class Spreads:
    def __init__(self, options_data):
        self.options_data = options_data


# class Straddles(Spreads):
#     def __init__(self, option_data, straddle_range):
#         Spreads.__init__(self, option_data)
#         self.stradde_range = straddle_range
#
#
#     def getAllStraddles(self, straddle_range):

    # def __init__(self, spread_name, call_options, put_options, num_calls, num_puts):
    #     self.spread_name = spread_name
    #     self.call_options = call_options
    #     self.put_options = put_options
    #
    #     # Find delta
    #     for call_op in call_options:
    #         self.delta += call_op.delta
    #     for put_op in put_options:
    #         self.delta += put_op.detla

