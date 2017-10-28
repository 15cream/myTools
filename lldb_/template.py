__author__ = 'gjy'

import lldb

if __name__ == '__main__':
    # Create a new debugger instance in your module if your module can be run form the command line.
    # When we run a script from the command line, we won't have any debugger object in lldb.debugger,
    # so we create it if it will be needed.
    lldb.debugger = lldb.SBDebugger.Create
elif lldb.debugger:
    # Module is being run inside the LLDB interpreter
    lldb.debugger.HandleCommand("")