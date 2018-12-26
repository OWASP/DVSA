# LESSON #9: Vulnerable Dependencies

DVSA has multiple dependencies. 

The function that is triggered by the REST API calls uses two vulnerable libraries:
(1) node-serialize
(2) node-jose

Here are the vulnerabilities with the highest risk. 

```
┌───────────────┬──────────────────────────────────────────────────────────────┐
│ High          │ Invalid Curve Attack                                         │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ Package       │ node-jose                                                    │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ Dependency of │ node-jose                                                    │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ Path          │ node-jose                                                    │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ More info     │ https://nodesecurity.io/advisories/324                       │
└───────────────┴──────────────────────────────────────────────────────────────┘

┌───────────────┬──────────────────────────────────────────────────────────────┐
│ High          │ Regular Expression Denial of Service                         │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ Package       │ minimatch                                                    │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ Dependency of │ node-jose                                                    │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ Path          │ node-jose > browserify > glob > minimatch                    │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ More info     │ https://nodesecurity.io/advisories/118                       │
└───────────────┴──────────────────────────────────────────────────────────────┘

┌───────────────┬──────────────────────────────────────────────────────────────┐
│ Critical      │ Potential Command Injection                                  │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ Package       │ shell-quote                                                  │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ Dependency of │ node-jose                                                    │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ Path          │ node-jose > browserify > shell-quote                         │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ More info     │ https://nodesecurity.io/advisories/117                       │
└───────────────┴──────────────────────────────────────────────────────────────┘

┌───────────────┬──────────────────────────────────────────────────────────────┐
│ Critical      │ Code Execution through IIFE                                  │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ Package       │ node-serialize                                               │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ Patched in    │ No patch available                                           │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ Dependency of │ node-serialize                                               │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ Path          │ node-serialize                                               │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ More info     │ https://nodesecurity.io/advisories/311                       │
└───────────────┴──────────────────────────────────────────────────────────────┘
```

You can refer to [Lesson #1: Code Injection](../LESSONS/LESSON_01.md), as a practical exploit of the **node-serialize** library.

- - -
[ToC](../LESSONS/README.md) | [1](../LESSONS/LESSON_01.md) | [2](../LESSONS/LESSON_02.md) | [3](../LESSONS/LESSON_03.md) | [4](../LESSONS/LESSON_04.md) | [5](../LESSONS/LESSON_05.md) | [6](../LESSONS/LESSON_06.md) | [7](../LESSONS/LESSON_07.md) | [8](../LESSONS/LESSON_08.md) | [9](../LESSONS/LESSON_09.md) | [10](../LESSONS/LESSON_10.md)
