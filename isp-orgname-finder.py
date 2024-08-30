import sys
import subprocess
import threading
from queue import Queue

# Number of worker threads
num_threads = 8

# Queue to hold domains
queue = Queue()

# Function to process each domain
def lookup_isp():
    while not queue.empty():
        domain = queue.get()
        try:
            # Get the IP address of the domain
            ip = subprocess.check_output(["dig", "+short", domain]).decode().strip().split('\n')[-1]
            if ip:
                # Get the ISP name using whois
                whois_output = subprocess.check_output(["whois", ip]).decode().lower()
                if 'orgname' in whois_output:
                    isp = whois_output.split('orgname:')[1].split('\n')[0].strip()
                elif 'org-name' in whois_output:
                    isp = whois_output.split('org-name:')[1].split('\n')[0].strip()
                else:
                    isp = "ISP not found"

                output_line = f"{domain} - {isp}"
            else:
                output_line = f"{domain} - No IP found"

            print(output_line)

        except subprocess.CalledProcessError as e:
            print(f"Error processing {domain}: {e}")
        finally:
            queue.task_done()

# Main function to set up and run threads
def main(input_file):
    # Load domains into the queue
    with open(input_file, "r") as file:
        for line in file:
            queue.put(line.strip())

    # Start the threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=lookup_isp)
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("ISP lookup completed.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 isp_lookup.py <live_domains.txt>")
        sys.exit(1)

    input_file = sys.argv[1]

    # Run the main function
    main(input_file)
