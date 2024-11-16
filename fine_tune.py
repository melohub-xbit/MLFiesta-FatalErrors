from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
from datasets import Dataset

# Step 1: Load GPT-2 and its tokenizer
model_name = "gpt2"  # You can also use 'gpt2-medium' or other variants
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = model.config.eos_token_id

# Step 2: Load text from a file
file_path = "sandalwood_data.txt"  # Replace with your file path
with open(file_path, "r", encoding="utf-8") as file:
    text_data = file.read()

# Convert plain text into a dataset
dataset = Dataset.from_dict({"text": [text_data]})

# Step 3: Tokenize the dataset
# Step 3: Tokenize the dataset
def tokenize_function(examples):
    tokenized = tokenizer(examples["text"], truncation=True, padding="max_length", max_length=512)
    tokenized["labels"] = tokenized["input_ids"].copy()
    return tokenized

tokenized_dataset = dataset.map(tokenize_function, batched=True)


# Step 4: Define training arguments
training_args = TrainingArguments(
    output_dir="./fine_tuned_gpt2",  # Directory to save model
    overwrite_output_dir=True,
    num_train_epochs=3,  # Number of epochs
    per_device_train_batch_size=2,  # Adjust based on your hardware
    save_steps=500,  # Save model every 500 steps
    save_total_limit=2,  # Limit the number of saved models
    logging_dir="./logs",  # Log directory
    logging_steps=100,  # Log every 100 steps
    evaluation_strategy="no",  # No evaluation for simple fine-tuning
)

# Step 5: Train the model
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

trainer.train()

# Step 6: Save the fine-tuned model
model.save_pretrained("./fine_tuned_gpt2")
tokenizer.save_pretrained("./fine_tuned_gpt2")

print("Model fine-tuned and saved at './fine_tuned_gpt2'")