__author__ = 'gjy'

# debugger : lldb.SBDebugger. The current debugger object.
# command : A python string containing all arguments for your command.
# exe_ctx : lldb.SBExecutionContext. An execution context object carrying around information on the inferior process's
#           context in which the command is expected to act.
# result : lldb.SBCommandReturnObject. A return object which encapsulates success/failure information for the command
#          and output text that needs to be printed as a result of the command.
# internal_dict : The dictionary for the current embedded script session which contains all variables and functions.


def command_function(debugger, command, result, internal_dict):
    pass

