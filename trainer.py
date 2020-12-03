import json


class Trainer:
    def __init__(self):
        with open("intents.json") as file:
            self.data = json.load(file)

    # function to add to JSON
    def write_json(self, data_json, filename='intents.json'):
        with open(filename, 'w') as f:
            json.dump(data_json, f, indent=4)

    def add_new_response(self, tag_resp, resps):
        with open('intents.json') as json_file:
            data_json = json.load(json_file)
            for i, tg in enumerate(self.data["intents"]):
                if tg['tag'] == tag_resp:
                    resp_json = tg["responses"]
                    for resp in resps:
                        resp_json.append(resp)
                    data_json["intents"][i]["responses"] = resp_json
                    break
        self.write_json(data_json)

    def add_new_patterns(self, tag_resp, pats):
        with open('intents.json') as json_file:
            data_json = json.load(json_file)
            for i, tg in enumerate(self.data["intents"]):
                if tg['tag'] == tag_resp:
                    resp_json = tg["patterns"]
                    for pat in pats:
                        resp_json.append(pat)
                    data_json["intents"][i]["patterns"] = resp_json
                    break
        self.write_json(data_json)

    def add_new_intent(self, tag, pattern, response):
        with open('intents.json') as json_file:
            data_json = json.load(json_file)
            temp = data_json['intents']
            # python object to be appended
            y = {
                "tag": "" + tag + "",
                "patterns": pattern,
                "responses": response,
                "context": "none"
            }
            temp.append(y)
        self.write_json(data_json)

    def get_array_sentences(self):
        inputs = []
        while True:
            inp = input("      (done to end) >>> ")
            if inp.lower() == "done":
                break
            inputs.append(inp.lower())
        return inputs

    def get_alike_tag(self, statement):
        print("is this the closest intent : " + statement["tag"])
        continue_update = input("      (y/n) >>> ")
        if continue_update == "y":
            print("What is the updated pattern ?")
            new_pattern = self.get_array_sentences()
            self.add_new_patterns(statement["tag"], new_pattern)
            print("Done. Your intent has been updated.")
            return 1
        elif continue_update == "n":
            return 0
