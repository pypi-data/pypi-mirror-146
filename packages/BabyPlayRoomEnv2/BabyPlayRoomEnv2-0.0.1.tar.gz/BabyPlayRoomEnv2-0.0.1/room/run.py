
def exec_full(filepath):
    global_namespace = {
        "__file__": filepath,
        "__name__": "__main__",
    }
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), global_namespace)

# # Execute the file.
# exec_full("C:\\Users\\duanj\\VPR\\room\\VPR\\test\\code\\gui_control-main\\demo.py")


