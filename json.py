#!/usr/bin/env python

import lldb

def process(debugger, command, result, internal_dict):
    lldb.debugger.HandleCommand("""
    expr -l swift --
    func $process(object: Any) {
        func json(object: Any) -> String {
            if let data = try? JSONSerialization.data(withJSONObject: object, options: .prettyPrinted) {
                return String(data: data, encoding: String.Encoding.utf8) ?? ""
            } else {
                return String(describing: object)
            }
        }

        Swift.print(json(object))
    }
    """.strip())
    lldb.debugger.HandleCommand('expr -l swift -- $process(' + command + ')')

def __lldb_init_module(debugger,internal_dict):
    debugger.HandleCommand("command script add -f json.process json")
    print "json command enabled."
