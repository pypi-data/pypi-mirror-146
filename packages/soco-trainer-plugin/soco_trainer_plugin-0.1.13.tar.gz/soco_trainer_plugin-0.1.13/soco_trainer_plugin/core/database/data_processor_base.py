from soco_trainer_plugin.core.database.mongo_api import Database


class ProcessorBase(object):
    def __init__(self, mongo_url):
        self.db = Database(mongo_url=mongo_url)

    def get_sample(self, filename):
        query = []
        for name in filename.strip().split(" "):
            query.append({"name": name})
        input_data = self.db.client["trainer"]["train_data"].find_one({"$or": query})
        return input_data


    def get_train_examples(self, filename):
        query = []
        for name in filename.strip().split(" "):
            query.append({"name": name})
        input_data = self.db.client["trainer"]["train_data"].find({"$or": query})
        return input_data

    def get_dev_examples(self, filename):
        query = []
        for name in filename.strip().split(" "):
            query.append({"name": name})
        input_data = self.db.client["trainer"]["dev_data"].find({"$or": query})
        return input_data


if __name__ == "__main__":
    X = ProcessorBase("mongodb://68.77.252.175:32000/trainer")
    z = X.get_train_examples("example-v1.json")
