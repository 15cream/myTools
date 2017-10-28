__author__ = 'gjy'

# frame : lldb.SBFrame Type. The current stack frame where the breakpoint got hit;
# bp_loc : lldb.SBBreakpointLocation Type. One breakpoint<lldb.SBBreakpoint> can have one or more locations.
# dict : The python session dictionary as a standard python dict object.

# return : False => don't stop at the breakpoint
#          Others => stop at the breakpoint


def breakpoint_function_wrapper(frame, bp_loc, dict):
    pass

