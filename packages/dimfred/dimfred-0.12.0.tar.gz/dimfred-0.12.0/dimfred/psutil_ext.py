import psutil

def has_process(process_name):
    for p in psutil.process_iter():
        try:
            if process_name == p.name():
                return True
        except:
            pass

    return False

setattr(psutil, "has_process", has_process)

