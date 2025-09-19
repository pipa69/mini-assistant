from .model_utils import load_model
import re
import datetime

class MiniAssistant:
    def __init__(self, model=None, name="MiniAsystent"):
        self.name = name
        self.model = model or load_model()
        self.context = {}

    def predict_intent(self, text: str):
        proba = None
        intent = None
        try:
            probs = self.model.predict_proba([text])[0]
            labels = self.model.classes_
            idx = probs.argmax()
            intent = labels[idx]
            proba = float(probs[idx])
        except AttributeError:
            intent = self.model.predict([text])[0]
            proba = 1.0
        return intent, proba

    def extract_entities(self, text: str):
        entities = {}
        m = re.search(r"(\d+)\s*(min|minut|sek)", text)
        if m:
            entities["number"] = int(m.group(1))
            entities["unit"] = m.group(2)
        m2 = re.search(r"pogod.* w ([A-Za-ząęćłńóśżźĄĘĆŁŃÓŚŻŹ\s]+)", text)
        if m2:
            entities["city"] = m2.group(1).strip()
        return entities

    async def handle(self, text: str, user_id: str = "anon"):
        intent, confidence = self.predict_intent(text)
        entities = self.extract_entities(text)
        user_ctx = self.context.setdefault(user_id, {})
        user_ctx["last_intent"] = intent

        if confidence < 0.4:
            return {"answer": "Nie jestem pewien, czy dobrze zrozumiałem. Możesz powtórzyć?", "intent": None, "confidence": confidence, "entities": entities}

        if intent == "greeting":
            return {"answer": "Cześć! W czym mogę pomóc?", "intent": intent, "confidence": confidence, "entities": entities}

        if intent == "goodbye":
            return {"answer": "Do zobaczenia!", "intent": intent, "confidence": confidence, "entities": entities}

        if intent == "time":
            now = datetime.datetime.now().strftime("%H:%M")
            return {"answer": f"Jest teraz {now}.", "intent": intent, "confidence": confidence, "entities": entities}

        if intent == "date":
            today = datetime.date.today().strftime("%d.%m.%Y")
            return {"answer": f"Dzisiejsza data to {today}.", "intent": intent, "confidence": confidence, "entities": entities}

        if intent == "weather":
            city = entities.get("city") or "Warszawa"
            return {"answer": f"Sprawdzę pogodę w {city} (wymaga klucza API).", "intent": intent, "confidence": confidence, "entities": {"city": city}}

        if intent == "joke":
            return {"answer": "Dlaczego komputerowi jest zimno? Bo zostawił swoje okno otwarte!", "intent": intent, "confidence": confidence, "entities": entities}

        if intent == "search":
            q = re.sub(r"^(szukaj|znajdź)\s*", "", text, flags=re.I)
            return {"answer": f"Oto wyniki wyszukiwania: https://www.google.com/search?q={q}", "intent": intent, "confidence": confidence, "entities": {"query": q}}

        return {"answer": "Przykro mi, nie rozumiem. Spróbuj sformułować inaczej.", "intent": intent, "confidence": confidence, "entities": entities}
