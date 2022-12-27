import os
import gc


class static_files_not_loaded_error(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('static files not loaded', *args)


class static_directory_not_find(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('static directory not find', *args)


class static_files_not_find(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('static file not find', *args)


class static_files:

    def __init__(self, path):
        self.static_files = {}
        self.path = path
        self.loaded = False
        self.current_file = ''
        self.current_dictory = path

    def __get_list__(self):
        return list(self.static_files.keys())

    def __get_raw_list__(self):
        return self.static_files

    def __get_file__(self, file_name):
        if self.loaded:

            if file_name not in self.static_files:
                raise static_files_not_find

            self.current_file = file_name
            return self.static_files[file_name]

        else:
            raise static_files_not_loaded_error

    def __get_files__(self, file_names: list):
        if self.loaded:
            res = {}
            for file in file_names:

                if file not in self.static_files:
                    continue

                res[file] = self.static_files[file]
            return res

        else:
            raise static_files_not_loaded_error

    def __clear__(self):
        self.loaded = False
        self.static_files.clear()
        self.current_file = ''
        self.path = ''
        self.current_dictory = ''

    def __load__(self, path):
        if not os.path.isdir(path):
            raise static_directory_not_find
        self.path = path
        self.current_dictory = path
        for static_file_name in os.listdir(path):
            with open(path + '\\'+static_file_name, 'rb')as static_file:
                self.static_files[static_file_name] = static_file.read()
            self.loaded = True
        return self.static_files

    def __enter__(self):
        self.__load__(self.path)
        return self

    def __exit__(self, type, value, trace):
        del self
        gc.collect()
