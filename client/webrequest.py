from flask import request, Flask
from flask_restful import Api, Resource
from subprocess import Popen, PIPE

app = Flask(__name__)
api = Api(app)


class Request(Resource):

    def __init__(self):
        self.data = request.get_json()

    def cmd(self):
        process = Popen(['cmd', '/k', self.data["Command"]], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        return {"std_out": stdout.decode(), "std_err": stderr.decode(), "sys_rc": process.returncode}

    def powershell(self):
        process = Popen(['powershell.exe', '-nologo', self.data["Command"]], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        return {"std_out": stdout.decode(), "std_err": stderr.decode(), "sys_rc": process.returncode}

    def post(self, name):
        """ This Method will get the json posted to it, Executes it in the requested shell
            Usage :
                    URL : http://<Hostname>:1808/<requiredshell>
                    JSON : { "Command" : cmd to run }
            Response :
                    JSON : { "sys_rc": system_rc, "std_out": std_out "std_err": std_err }
        """
        if name == "cmd":
            return self.cmd()
        elif name == "ps":
            return self.powershell()
        else:
            return {"Error": "Method not found"}


api.add_resource(Request, "/<string:name>")
app.run(port=1808, debug=True)
