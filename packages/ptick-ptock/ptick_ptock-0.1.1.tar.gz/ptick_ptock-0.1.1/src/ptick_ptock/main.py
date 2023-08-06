import datetime

class ptick_ptock:
    current_time = None 
    def ptick(self):
        self.current_time = datetime.datetime.now()
        return
    def datetime_ptock(self):
        elapsed = datetime.datetime.now() - self.current_time
        return elapsed
    def print_ptock(self):
        print(datetime.datetime.now() - self.current_time)


if __name__ == "__main__":
    obj = ptick_ptock()
    obj.ptick()
    print(obj.datetime_ptock())
    obj.print_ptock()