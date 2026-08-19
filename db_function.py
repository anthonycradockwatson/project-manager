import pickle
import os

class ObjectStore:
    def __init__(self, filename):
        self.filename = filename
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        self.objects = self.load_all()

    def load_all(self):
        if os.path.exists(self.filename):
            with open(self.filename, "rb") as f:
                return pickle.load(f)
        return {}
    
    def save(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self.objects, f)

    def add(self, obj):
        self.objects[obj.uuid] = obj
        self.save()

    def update(self, obj):
        self.objects[obj.uuid] = obj
        self.save()

    def delete(self, obj_id):
        if obj_id in self.objects:
            del self.objects[obj_id]
            self.save()

    def get_item(self, obj_id):
        return self.objects.get(obj_id)

    def reload(self):
        self.objects = self.load_all()
        return self.objects
