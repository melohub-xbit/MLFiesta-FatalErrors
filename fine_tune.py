from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
from datasets import Dataset
import os
import glob

# Step 1: Load GPT-2 and its tokenizer
model_name = "gpt2"  # You can also use 'gpt2-medium' or other variants
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = model.config.eos_token_id

# Step 2: Load all text files from the folder
dataset_folder = "text_dataset"
text_files = glob.glob(os.path.join(dataset_folder, "*.txt"))
all_texts = []

for file_path in text_files:
    with open(file_path, "r", encoding="utf-8") as file:
        text_data = file.read()
        all_texts.append(text_data)

# Convert texts into a dataset
dataset = Dataset.from_dict({"text": all_texts})

# Step 3: Tokenize the dataset
def tokenize_function(examples):
    tokenized = tokenizer(examples["text"], truncation=True, padding="max_length", max_length=512)
    tokenized["labels"] = tokenized["input_ids"].copy()
    return tokenized

tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Step 4: Define training arguments
training_args = TrainingArguments(
    output_dir="./fine_tuned_gpt2_v2",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=2,
    save_steps=500,
    save_total_limit=2,
    logging_dir="./logs",
    logging_steps=100,
    evaluation_strategy="no",
)

# Step 5: Train the model
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

trainer.train()

# Step 6: Save the fine-tuned model
model.save_pretrained("./fine_tuned_gpt2_v2")
tokenizer.save_pretrained("./fine_tuned_gpt2_v2")

print(f"Model fine-tuned on {len(text_files)} files and saved at './fine_tuned_gpt2_v2'")
