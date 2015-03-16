
class Derivatives():

    def __init__(self):
        pass

    def __run_cmds(self):
        
        try:
            process = subprocess.check_call(self.cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        except Exception as e:
            print e

        finally:
            if process==0:
                print "Derivative created at {0}".format(self.output_basename)

            else:
                print process 