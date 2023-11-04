import subprocess
import os
import signal

FILE_NAME = ".proc"
# path = os.getcwd() + "\\phishing\\web_server"
# cronloop_process = subprocess.Popen(
#     "python manage.py cronloop", creationflags=subprocess.CREATE_NEW_CONSOLE
# )
# print(cronloop_process.pid, "cronloop_process")


def start_process():
    text_file = open(FILE_NAME, "w")

    cronloop_process = subprocess.Popen(
        "python manage.py cronloop",
        shell=True,
    )

    text_file.write(str(cronloop_process.pid))
    print("cronloop_process", cronloop_process.pid)


def get_last_process_pid():
    try:
      text_file = open(FILE_NAME, "r")
      file_data = text_file.read()
      text_file.close()
      return file_data
    except:
      # Create if not exists
      create_if_not_exists = open(FILE_NAME, "w+")
      create_if_not_exists.close()

      text_file = open(FILE_NAME, "r")
      file_data = text_file.read()
      text_file.close()
      return file_data


def start_cronloop(last_process_pid):
    print("last_process_pid", last_process_pid)

    if last_process_pid == "":
        start_process()
    else:
        try:
            int_pid = int(last_process_pid)
            os.kill(int_pid, signal.SIGTERM)
            start_process()
        except:
            start_process()


if __name__ == "__main__":
    last_process_pid = get_last_process_pid()
    start_cronloop(last_process_pid)
