# pyforkexec

WARNING: Read the warning section before you use this program.

`pyforkexec` is a program to speed up the execution of a user script. it
optimizes the execution with the observation that, many user scripts can be
split into 2 sections: the *init* section and the *run* section:

-   the *init* section is responsible for importing libraries, creating
    necessary data structures and doing other kinds of initialization. once the
    initialization is done, the *init* section is no longer needed.

-   the *run* section is responsible for the concrete job which utilizes the
    libraries imported and the data structures created in the *init* section.

typically, the *init* section needs to be run only once, while the *run* section
may be run multiple times which all share the same context created by the *init*
section. therefore, if the *init* section takes a long time, then it's better to
run it once and cache the context for the following *run* sections. in this way,
the *run* section no longer suffers the overhead from the *init* section.

the implementation uses a client-server architecture in which communication is
done through a unix domain socket. the user runs a script using the client. but
instead of running the script directly, the client actually sends the script to
the server where it is actually run in a forked python vm. then the result is
sent back via the same socket and fed into stdout and stderr of the client.

## example

let's say we want to test if a str matches a regex.

    import os
    import re
    import setuptools
    import sys
    pattern = re.compile('he.*ld')
    print(pattern.match("helloworld"))

in my test, running this program directly takes about 300ms on a x86\_64 linux
box:

    # time python3 -c "$(cat examples/helloworld.py)"
    <_sre.SRE_Match object; span=(0, 10), match='helloworld'>

    real    0m0.300s
    user    0m0.271s
    sys     0m0.028s

note that this program can be split into:

-   *init* section:

        import os
        import re
        import setuptools
        import sys
        pattern = re.compile('he.*ld')

-   *run* section:

        print(pattern.match("helloworld"))

with `pyforkexec`, we can run it as:

-   server:

        # python3 server.py "$(cat examples/helloworld-init.py)"

-   client:

        # time python3 client.py "$(cat examples/helloworld-run.py)"
        <_sre.SRE_Match object; span=(0, 10), match='helloworld'>

        real    0m0.048s
        user    0m0.038s
        sys     0m0.007s

the execution time is reduced from 300ms to less than 50ms.

some people might ask why one has to import os, sys and setuptools for a regex
match. the answer is no we don't need those modules for a regex match. in this
simple example, they are fictional and simply used to demonstrate what kind of
problem `pyforkexec` can solve. however, this does not mean `pyforkexec` itself
is fictional. in real applications, the above situation can happen, for example,
when you need to use a library but have no control over its initialization, or
when your project is still under heavy development and optimizing these details
only has ephemeral effect and would negatively affect your development speed.

## limitation

currently, `pyforkexec` is in very early stage. we are not quite sure what is
right way to go next. and it has some limitations right now.

to give some examples of what should work:

-   `print("helloworld")`

-   `print("total: {}".format(2 + 3))`

-   `import re;m = re.match("\d+", "123");print(m)`

to give some examples of what won't work:

-   `import os;print(os.path.abspath("."))`

    returns server dir instead of client dir.

-   `import os;print(os.environ["foo"])`

    returns server env instead of client env.

-   `import sys;print(sys.argv[3])`

    no command-line arguments yet.

-   `a = input("name:")`

    no stdin yet.

it doesn't seem very difficult to resolve the above limitations, but it's hard
to make sure those resolutions are the proper way of handling them and there
aren't issues that are left out. therefore we prefer some discussions to show
the direction before we actually evolve this project. interested readers can
consult related threads on the `python-dev` and `python-ideas` mailing lists.

## warning

`pyforkexec` uses `exec()` which can run almost any statements, and if used
carelessly, can harm and even totally destroy your system. double check every
line of the program and understand what's happending before you use it. the
author assumes no warranty or liability at all for any kind of damage the
program may cause.

## license

The source code is licensed under the GNU General Public License v3.0.

Copyright (C) 2018 Cyker Way

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see http://www.gnu.org/licenses/.


