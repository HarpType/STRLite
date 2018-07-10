#for child proccess
proc = None

#for queue
q = None

stop_bridge = False


#for reading thread
def enqueue_output(out, queue):
    global stop_bridge

    while True:
        if stop_bridge == True:
            return
        line = out.readline()
        # if line == 'Stop\n':
        #     out.close()
        #     return
        if line[:7] == 'COMMAND':
            queue.put(line[7:])
