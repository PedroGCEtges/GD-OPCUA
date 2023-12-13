import os
import threading

def start_program(progam_name):
        os.system('python {}'.format(progam_name))

def main():# __name__ == "__main__":
        files = ["opcua_client_gd.py","middleware.py"]
        process = []

        for file in files:
                process.append(threading.Thread(target=start_program, args=(file,)))
        for p in process:
                p.start()
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