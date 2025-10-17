use std::{
    collections::VecDeque,
    error::Error,
    net::UdpSocket,
    sync::{Arc, Mutex},
    time::Duration,
};

fn main() -> Result<(), Box<dyn Error>> {
    let listen_socket = UdpSocket::bind("192.168.178.42:161")?;
    let listen_socket2 = listen_socket.try_clone()?;
    let forward_socket = UdpSocket::bind("192.168.178.42:5954")?;
    let forward_socket2 = forward_socket.try_clone()?;

    let addr = Arc::new(Mutex::new(None));
    let addr2 = addr.clone();

    std::thread::spawn(move || {
        let mut buf = [0; 2048];
        loop {
            let (amt, current_addr) = listen_socket.recv_from(&mut buf).unwrap();
            *addr.lock().unwrap() = Some(current_addr);
            forward_socket
                .send_to(&buf[..amt], "192.168.178.197:161")
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
    loop {
        std::thread::sleep(Duration::from_secs(1));
    }
}
