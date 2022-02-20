import importlib.util


# bar = load_file(name)
# a = bar.Test(1, 2) # -- load Class method
# bar.test_function(3, 4) # -- load explicit method

def load_file(path):
    spec = importlib.util.spec_from_file_location(path.resolve().stem, path)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo
