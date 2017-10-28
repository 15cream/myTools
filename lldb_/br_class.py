import lldb
import re
from OCclass import OCClass


def set_brs(class_name):
    interpreter = lldb.debugger.GetCommandInterpreter()
    returnObject = lldb.SBCommandReturnObject()
    cmd = "po [{} _shortMethodDescription]".format(class_name)
    interpreter.HandleCommand(cmd, returnObject)
    classes = re.split(r"in ", returnObject.GetOutput())
    for i in range(1, len(classes)):
        cls = OCClass()
        cls.class_analyze(classes[i])
        funcs = cls.instance_methods
        for func, addr in funcs.items():
            interpreter.HandleCommand("br s -a {}".format(addr), returnObject)
            # Or there's no need to specify the breakpoint, because if no breakpoint is specified,
            # the lldb driver adds the commands to the last created breakpoint.
            id = re.match(r"Breakpoint (\d+):", returnObject.GetOutput()).group(1)
            interpreter.HandleCommand("br command add --script-type python -F br_class.show_detail {}".format(id),
                                      returnObject)
            breakpoints[id] = cls.class_name + func


def bc(debugger, command, result, internal_dict):
    if not command:
        print >> result, 'Input Class name'
        return
    set_brs(command)


def show_detail(frame, bp_loc, dict):
    global breakpoints
    print 'Here!!!!' + bp_loc.__str__() + bp_loc.GetAddress().__hex__()
    print breakpoints[bp_loc.__str__().split('.')[0]]


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add bc -f br_class.bc')
    print 'bc installed'

breakpoints = dict()


