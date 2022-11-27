use web_server::ThreadPool;
use std::io::prelude::*;
use std::net::TcpListener;
use std::net::TcpStream;
use std::thread;
use std::time::Duration;

fn main() {
    let threaded_flag = std::env::args().nth(1);
    let count = std::env::args().nth(2);
    if threaded_flag == Option::from(String::from("-t")) {
        let mut thread_count:usize = 4;
        if threaded_flag != Option::None {
            thread_count = count.unwrap().parse::<usize>().unwrap();
        }
        println!("Using {} threads", thread_count);
        handle_with_thread_pool(thread_count);
    } else {
        handle_with_single_thread();
    }
    
    println!("Shutting down.");
}

fn handle_with_thread_pool(count: usize) {
    // let together = format!("{}{}{}", addr,String::from(":"),port);
    let listener = TcpListener::bind("127.0.0.1:8080").unwrap();
    let pool = ThreadPool::new(count);

    for stream in listener.incoming() {
        // pool.workers.
        let stream = stream.unwrap();

        pool.execute(|| {
            handle_connection(stream);
        });
    }

    println!("Shutting down.");

}
fn handle_with_single_thread() {
    // let together = format!("{}{}{}", addr,String::from(":"),port);
    let listener = TcpListener::bind("127.0.0.1:8080").unwrap();

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        handle_connection(stream);
    }

}
fn handle_connection(mut stream: TcpStream) {
    let mut buffer = [0; 1024];
    stream.read(&mut buffer).unwrap();

    let get = b"GET / HTTP/1.1\r\n";
    let sleep = b"GET /sleep HTTP/1.1\r\n";

    let (status_line, filename) = if buffer.starts_with(get) {
        ("HTTP/1.1 200 OK", hello_html())
    } else if buffer.starts_with(sleep) {
        thread::sleep(Duration::from_millis(1000));
        ("HTTP/1.1 200 OK", sleep_html())
    } else {
        ("HTTP/1.1 404 NOT FOUND", error_html())
    };

    let contents = filename;

    let response = format!(
        "{}\r\nContent-Length: {}\r\n\r\n{}",
        status_line,
        contents.len(),
        contents
    );

    stream.write_all(response.as_bytes()).unwrap();
    stream.flush().unwrap();
}

fn hello_html() -> String {
    let hello = r#"<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Hello!</title></head><body><h1>Hello!</h1><p>Hi from Rust</p></body></html>"#;
    return String::from(hello);
}
fn sleep_html() -> String {
    let sleep = r#"<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Hello!</title></head><body><h1>SLEEP</h1><p>Hi from Rust, but I am sleeping</p></body></html>"#; 
    return String::from(sleep);
}
fn error_html() -> String{
    let error = r#"<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Hello!</title></head><body><h1>Hello!</h1><p>Hi from Rust</p></body></html>"#;
    return String::from(error);
}