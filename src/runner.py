import subprocess

def execute_command(command_string):
    try:
        # Execute the command in the shell, capture output
        result = subprocess.run(command_string, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Decode the output bytes to string
        output = result.stdout.decode('utf-8')
        error = result.stderr.decode('utf-8')
        
        # Print output and error, if any
        if output:
            print("Output:")
            print(output)
        if error:
            print("Error:")
            print(error)
            
    except subprocess.CalledProcessError as e:
        # Handle errors
        print(f"Error executing command '{command_string}': {e}")

# First command - compile the main program
command1 = "g++ -o main src/main.cpp"
execute_command(command1)

# Second command - run the simulator with example files
command2 = "main examples/tests/cells.lib examples/tests/2.cir examples/tests/1.stim"
execute_command(command2)

# Third command - open the simulation output file
command3 = "code src/Graphing/output.sim"
execute_command(command3)
