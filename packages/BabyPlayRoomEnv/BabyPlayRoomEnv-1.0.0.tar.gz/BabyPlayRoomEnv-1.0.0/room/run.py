import os
def exec_full(filepath):
    global_namespace = {
        "__file__": filepath,
        "__name__": "__main__",
    }
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), global_namespace)

# # Execute the file.
path=os.path.dirname(os.path.abspath(__file__))
y = path.replace('\\room','')
exec_full(str(y)+"\\test\\code\\gui_control-main\\demo.py")


