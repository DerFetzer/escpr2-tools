use std::{
    error::Error,
    net::UdpSocket,
    sync::{Arc, Mutex},
    time::Duration,
};

use argh::FromArgs;

#[derive(FromArgs)]
/// Forward SNMP packets to printer and responses back
struct Cli {
    #[argh(positional)]
    printer_address: String,
    #[argh(positional)]
    local_address: String,
}

fn main() -> Result<(), Box<dyn Error>> {
    let args: Cli = argh::from_env();

    let listen_socket = UdpSocket::bind(format!("{}:161", args.local_address))?;
    let listen_socket2 = listen_socket.try_clone()?;
    let forward_socket = UdpSocket::bind(format!("{}:5954", args.local_address))?;
    let forward_socket2 = forward_socket.try_clone()?;

    let addr = Arc::new(Mutex::new(None));
    let addr2 = addr.clone();

    std::thread::spawn(move || {
        let mut buf = [0; 2048];
        loop {
            let (amt, current_addr) = listen_socket.recv_from(&mut buf).unwrap();
            *addr.lock().unwrap() = Some(current_addr);
            forward_socket
                .send_to(&buf[..amt], format!("{}:161", args.printer_address))
                .unwrap();
        }
    });

    std::thread::spawn(move || {
        let mut buf = [0; 2048];
        loop {
            let (amt, _current_addr) = forward_socket2.recv_from(&mut buf).unwrap();
            let addr = addr2.lock().unwrap();
            if let Some(addr) = *addr {
                listen_socket2.send_to(&buf[..amt], addr).unwrap();
            }
        }
    });
    println!("Started threads");
    loop {
        std::thread::sleep(Duration::from_secs(1));
    }
}
