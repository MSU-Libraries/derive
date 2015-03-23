import subprocess

class Derivatives():

    def __init__(self):
        pass

    def run_cmds(self):
        process = 1
        try:
            process = subprocess.check_call(self.cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        except Exception as e:
            print e

        finally:
            if process==0:
                print "Derivative created at {0}".format(self.output_basename)

            else:
                print process
                
        return process
