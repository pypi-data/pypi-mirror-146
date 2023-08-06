import docker
import re


class Docker(object):
    def __init__(self, container_name='trainer-worker'):
        client = docker.from_env()
        self.container = client.containers.get(container_name)

    def clean_logs(self, total):
        new_total = []
        for j, t in enumerate(total):
            x = re.findall("[0-9]*%[^\]]*]", t)
            if len(x) > 0:
                t = x[-1].strip()
            if not j == 0 and len(re.findall("[0-9]*%[^\]]*]", total[j - 1])) > 0:
                if not t.strip() == "":
                    new_total[len(new_total) - 1] = t.strip()
            else:
                if not t.strip() == "":
                    new_total.append(t)
        return new_total

    def get_logs_by_op_id(self, op_id):
        text = self.container.logs(tail=300).decode('utf-8')
        total = text.strip().split("\n")
        total = [z.strip() for z in total if not z.strip() == ""]
        for j,t in enumerate(total):
            if t.endswith("###") and t.startswith("INFO:core.trainer:###"):
                cur_op_id = t.replace("INFO:core.trainer:###","").replace("###","")
                if op_id.strip() == cur_op_id.strip():
                    return self.clean_logs(total[j-1:])
        return ["*** the logs have been deleted ***"]

    def get_logs(self, n=100):
        text = self.container.logs(tail=n).decode('utf-8')
        total = text.strip().split("\n")
        pods = []

        total = [z.strip() for z in total if not z.strip() == ""]
        available = False
        new_total = []
        isgpu = False
        device_count = 0
        info_list = []

        if len(total) > 0 and "cuda" in total[0]:
            isgpu = True
        if len(total) > 2 and "device_count" in total[2]:
            device_count = int(total[2].strip().split(":")[-1])
        if len(total) > 3 and " ### " in total[3]:
            temp = total[3].replace("INFO:__main__:","").split(" ### ")
            for t in temp:
                info = {}
                for k in t.strip().split("|"):
                    key, value = k.split(":")
                    info[key.strip()] = value.strip()
                info_list.append(info)
        new_total = self.clean_logs(total)
        if "*** Listening on " in " ".join(total[-2:]) or "Result is kept for" in " ".join(total[-2:]):
            available = True
        pods.append({"logs":new_total,
                     "name":"docker-compose",
                     "total_lines":len(new_total),
                     "available":available,
                     "is_gpu":isgpu,
                     "device_count":device_count,
                     "info_list":info_list,
                     "node_name":"docker-compose"})
        return pods

    def delete_pod(self, name):
        try:
            return self.container.restart()
        except Exception as e:
            print(e)
            return {"error":e}

    def delete_pod_by_op_id(self, op_id):
        self.delete_pod("random")
        return False
