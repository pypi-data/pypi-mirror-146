from RedisQueue.multi_process import start

if __name__ == "__main__":
    import test_abc
    start("zzha529", test_abc.print_json, 4)
