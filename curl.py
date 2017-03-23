#!/usr/bin/env python

import lldb

def process(debugger, command, result, internal_dict):
    lldb.debugger.HandleCommand("""
expr -l swift --
func $process(URLRequest: NSURLRequest) {
    func curl(URLRequest: NSURLRequest) -> String {
        guard let URLString = URLRequest.URL?.absoluteString else {
            return "$ curl command could not be created"
        }

        var components = ["$ curl -i \\"\\(URLString)\\""]

        if let HTTPMethod = URLRequest.HTTPMethod where HTTPMethod != "GET" {
            components.append("-X \\(HTTPMethod)")
        }

        if let headerFields = URLRequest.allHTTPHeaderFields {
            for (field, value) in headerFields {
                switch field {
                case "Cookie":
                    continue
                default:
                    components.append("-H \\"\\(field): \\(value)\\"")
                }
            }
        }

        if let
            HTTPBodyData = URLRequest.HTTPBody,
            HTTPBody = String(data: HTTPBodyData, encoding: NSUTF8StringEncoding) {
            let escapedBody = HTTPBody.stringByReplacingOccurrencesOfString("\\"", withString: "\\\\\\"")
            components.append("-d \\"\\(escapedBody)\\"")
        }

        return components.joinWithSeparator(" \\\\\\n\\t")
    }

    Swift.print(curl(URLRequest))
}
    """.strip())
    lldb.debugger.HandleCommand('expr -l swift -- $process(' + command + ')')

def __lldb_init_module(debugger,internal_dict):
    debugger.HandleCommand("command script add -f curl.process curl")
    print "curl command enabled."
