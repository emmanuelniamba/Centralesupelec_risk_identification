from transformers import AutoTokenizer, AutoModelForCausalLM

# Chargement du modèle
model_name = "microsoft/Phi-4-Reasoning"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

print("✅ Modèle chargé")

# Texte d'entrée
prompt = "Parle-moi de la vie de l'abeille."
inputs = tokenizer(prompt, return_tensors="pt")
print("✅ Inputs encodés")

# Génération
outputs = model.generate(**inputs, max_new_tokens=50)
print("✅ Texte généré")

# Décodage
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("🔹 Réponse du modèle :")
print(response)
