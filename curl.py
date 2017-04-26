#!/usr/bin/env python

import lldb

def process(debugger, command, result, internal_dict):
    lldb.debugger.HandleCommand("""
expr -l swift --
func $process(_ urlRequest: URLRequest) {
    func curl(_ urlRequest: URLRequest) -> String {
        var components = ["$ curl -i"]

        guard let urlString = urlRequest.url?.absoluteString else {
            return "$ curl command could not be created"
        }

        if let httpMethod = urlRequest.httpMethod, httpMethod != "GET" {
            components.append("-X \\(httpMethod)")
        }

        if let headerFields = urlRequest.allHTTPHeaderFields {
            for (field, value) in headerFields {
                switch field {
                case "Cookie":
                    continue
                default:
                    components.append("-H \\"\\(field): \\(value)\\"")
                }
            }
        }

        if let httpBodyData = urlRequest.httpBody,
            let httpBody = String(data: httpBodyData, encoding: String.Encoding.utf8) {
            let escapedBody = httpBody.replacingOccurrences(of: "\\"", with: "\\\\\\"")
            components.append("-d \\"\\(escapedBody)\\"")
        }

        components.append("\\"\\(urlString)\\"")

        return components.joined(separator: " \\\\\\n\\t")
    }

    Swift.print(curl(urlRequest))
}
    """.strip())
    expr = 'expr -l swift -- $process(' + command + ')'
    lldb.debugger.HandleCommand(expr)

def __lldb_init_module(debugger,internal_dict):
    debugger.HandleCommand("command script add -f curl.process curl")
    print "curl command enabled."
