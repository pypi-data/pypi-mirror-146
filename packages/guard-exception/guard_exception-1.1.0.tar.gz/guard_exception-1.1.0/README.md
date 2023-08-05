# guard_exception
    - guard all exception for swift run python

## install
    - pip install guard-exception


## functions
    - guardExceptionWithOutParams: execute function without parameters
    - guardException: execute function with parameters
    - guardSearchKeyException: look for a key
    - guardSearchKeryRecursiveException: look for a key recursively
    - guardExceptionIsIterable: return 1 or 0, if exists key on dic

## example
```python
import guard_exception as ge

gg = ge.guard_exception()


def divide(a, b):
    return a / b


print(gg.guardException(divide, a=1, b=0))


# result cli
# {'data:': None, 'error': 'division by zero'}

```


## example on swift with PythonKit
```swift
import PythonKit
let hvac = Python.import("hvac")
let ge = Python.import("guard_exception")
let gg = ge.guard_exception()

let client = hvac.Client(url: "http://0.0.0.0:8200")

let user = "incorrect_user"
let params = Python.dict()
params["username"] = PythonObject(user)
params["password"] = PythonObject("incorrect_password")

print(gg.guardException(client.login, url: "v1/auth/userpass/login/\(user)", use_token: true, json: params))

// result: cli
//{'data': None, 'error': 'invalid username or password, on post http://0.0.0.0:8200/v1/auth/userpass/login/incorrect_user'}
```


## example complete on swift
```swift
// guardException
// guardSearchKeyException
// guardSearchKeryRecursiveException

import Vapor
import PythonKit
let hvac = Python.import("hvac")
let ge = Python.import("guard_exception")
let gg = ge.guard_exception()

// token structure for authentication
// Content: help resolve the api response -> json
public struct Token: Content {
    public var client_token: String!
    public var accessor: String!
    public var policies: [String]!
    public var token_policies: [String]!
}


// swift class for authentication
public class autentication  {
    // MARK: - Properties
    let client = hvac.Client(url: "http://0.0.0.0:8200")
    var token: Token?
    
    // MARK: - Initializers
    public init() { }

    public func login(user: String, password: String) -> Token {
        let params = Python.dict()
        params["username"] = PythonObject(user)
        params["password"] = PythonObject(password)

        let generated = Python.dict(gg.guardException(self.client.login, url: "v1/auth/userpass/login/\(user)", use_token: true, json: params))

        // result genereted
        /*
            {
                'data': 
                {
                    'request_id': '45464674xxxxxxxb', 
                    'lease_id': '', 
                    'renewable': False, 
                    'lease_duration': 0, 
                    'data': None, 
                    'wrap_info': None, 
                    'warnings': None, 
                    'auth': {
                        'client_token': 'hvs.CAESasdfasdfxxxxxxxxxxxxxxxxxxx', 
                        'accessor': 'TvExxxxxxxxxxxxxxx1ESqjW', 
                        'policies': ['default'], 
                        'token_policies': ['default'], 
                        'metadata': {'username': 'rafael'}, 
                        'lease_duration': 2764800, 
                        'renewable': True, 
                        'entity_id': 'dadxxxf8-xxxx-xxxxx-xxxxx-xxxxxxxxxxx', 
                        'token_type': 'service', 
                        'orphan': True, 
                        'mfa_requirement': None, 
                        'num_uses': 0
                    }
                }, 
                'error': None
            }
        */

        let auth = gg.guardExceptionIsIterable(generated, key:"data")

        if Int(auth["data"])! > 0 {

            let client_token = String(gg.guardSearchKeryRecursiveException(generated, key:["data", "auth", "client_token"])["data"])
            let accessor = String(gg.guardSearchKeryRecursiveException(generated, key:["data", "auth", "accessor"])["data"])
            let policies = [String](gg.guardSearchKeryRecursiveException(generated, key:["data", "auth", "policies"])["data"])!
            let token_policies = [String](gg.guardSearchKeryRecursiveException(generated, key:["data", "auth", "token_policies"])["data"])!

            if client_token != nil {
                self.token = Token(
                    client_token: client_token,
                    accessor: accessor,
                    policies: policies,
                    token_policies: token_policies
                )
            }
        }
        
        return self.token ?? Token(client_token: nil, accessor: nil, policies: [], token_policies: [])
    }

}
```
