#for child proccess
proc = None

#for queue
q = None


#for reading thread
def enqueue_output(out, queue):
    while True:
        line = out.readline()
        if line == 'Stop\n':
            out.close()
            return
        if line[:7] == 'COMMAND':
            queue.put(line[7:])