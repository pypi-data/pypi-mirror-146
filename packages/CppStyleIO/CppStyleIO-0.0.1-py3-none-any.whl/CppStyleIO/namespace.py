def using(path, name):
    def runner(func):
        exit(func())

    return runner
