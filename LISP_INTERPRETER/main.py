from fun import Scanner, EnvironmentBuilder, Parser, Env

#   list dialect scheme => https://en.wikipedia.org/wiki/Scheme_(programming_language)

if __name__ == '__main__':
    env = EnvironmentBuilder.build_env()
    local_env = Env()
    while 1:
        _input = input("LISP>")
        _input = Scanner.scan(_input)
        print(_input)
        result = Parser.parse(_input, env)
        if result is not None:
            print(result)
