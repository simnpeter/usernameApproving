# services/user_data_service.py
from models.username import Username
from config import THRESHOLD

def add_name_to_db(name, label):
    Username(username=name, label=label).save()
    
    new_data = Username.objects()
    new_names = [item.username for item in new_data]
    new_labels = [item.label for item in new_data]
    
    if len(new_names) >= THRESHOLD:
        # Itt jönne a modell frissítése, ha lenne modell
        Username.objects.delete()
        return {"message": "Model updated with new data"}, 200
    else:
        return {"message": "Name added, but not enough data to retrain"}, 200

def predict(name):
    # Itt jönne a predikciós logika, ha lenne modell
    return {"approved": True}, 200
