import subprocess
def run_llama3(prompt):    
    command = f'ollama run llama3 Concisely Answer:"{prompt}"'
    try:     
        result = subprocess.run(command, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding='utf-8')       

        print("Result:")
        print(result.stdout.replace("failed to get console mode for stdout: The handle is invalid.","").replace("failed to get console mode for stderr: The handle is invalid.","").replace('"',"").strip())
       
    except Exception as e:
        print(f"An error occurred: {e}")

prompt = "write a instagram description for funny video"

run_llama3(prompt)