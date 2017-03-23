#!/usr/bin/env python

import lldb

def process(debugger, command, result, internal_dict):
    lldb.debugger.HandleCommand("""
    expr -l swift --
    func $process(object: AnyObject) {
        func json(object: AnyObject) -> String {
            if let data = try? NSJSONSerialization.dataWithJSONObject(object, options: .PrettyPrinted) {
                return String(data: data, encoding: NSUTF8StringEncoding) ?? ""
            }
            else {
                return String(object)
            }
        }

        Swift.print(json(object))
    }
    """.strip())
    lldb.debugger.HandleCommand('expr -l swift -- $process(' + command + ')')

def __lldb_init_module(debugger,internal_dict):
    debugger.HandleCommand("command script add -f json.process json")
    print "json command enabled."
