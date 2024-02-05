import os
import threading
import tkinter as tk
import subprocess
import json

def start_program(program_name):
        try:
                os.system('python {}'.format(program_name))
                # subprocess.run(['python', program_name], check=True)
        except subprocess.CalledProcessError as e:
                print(f"Error running {program_name}: {e}")
        # finally:
        #         os._exit(0)

def main():
        files = ["client_dist.py","client_pp.py","client_sort.py","middleware.py"]
        process = []
        try:
                for file in files:
                        p = threading.Thread(target=start_program, args=(file,))
                        process.append(p)
                        p.start()
                for p in process:
                        p.join()
        except Exception as e:
                for p in process:
                        p.join()
                os._exit(0)
        
if __name__ == "__main__":
    main()

# def main():
#     # task1 = asyncio.create_task(connect_to_gd_opcua())
#     # task2 = asyncio.create_task(watch_collection(mongo_client()["GD"]["Command"]))
#     # res = asyncio.run(asyncio.gather(watch_collection(mongo_client()["GD"]["Command"]), connect_to_gd_opcua()))
#     # await task1, #task2
#     # print(res)
#     # while True:
#         connect_to_gd_opcua()
#         # r2 = await watch_collection(mongo_client()["GD"]["Command"])

#         # if r2 == False:
#         #     print("Ola", r1)
#         #     break
#         # asyncio.sleep(1)