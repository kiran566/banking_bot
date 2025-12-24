import json

INPUT_FILE = "../data/bank_faqs.json"
OUTPUT_FILE = "../data/intents.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

intents = []

for category, qa_list in raw_data["bank"].items():
    patterns = []
    responses = []

    for qa in qa_list:
        question = qa[0].strip()
        answer = qa[1].strip()

        patterns.append(question)
        responses.append(answer)

    intents.append({
        "tag": f"{category}_faq",
        "patterns": patterns,
        "responses": list(set(responses))
    })

final_data = {"intents": intents}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(final_data, f, indent=2)

print(" intents.json created successfully")
