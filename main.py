from src.config import processor_option
from src.models_charged.Qwen2_2B import Qwen2_2B_run
from src.models_charged.Salesforce import salesforce_run
from src.shell_question import ProcessorOption

print("Model ready\n")

def main():
   if processor_option == ProcessorOption.Qwen2_2B:
      Qwen2_2B_run()
   elif processor_option == ProcessorOption.Salesforce:
      salesforce_run()
   else:
      print("Woops! Invalid option.")

if __name__ == "__main__":
   main()