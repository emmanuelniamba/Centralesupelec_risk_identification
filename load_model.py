from transformers import AutoTokenizer, AutoModelForCausalLM
def load_model(model_name):
    try:
        # Load the tokenizer
        tokenizer=AutoTokenizer.from_pretrained(model_name)
        # Load the model
        model=AutoModelForCausalLM.from_pretrained(model_name)
        return tokenizer, {model_name}
    except Exception as e:
        print(f"Error loading model {model_name}: {e}")
        return None, None
    
    
